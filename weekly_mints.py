"""
USDC minted and burned on Arc per week, and the running supply, using Envio HyperSync.

Usage:
    export ENVIO_API_TOKEN=...          # free token: https://docs.envio.dev/docs/HyperSync/api-tokens
    python3 weekly_mints.py
"""
import json, os, time, urllib.error, urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone

USDC = "0x3600000000000000000000000000000000000000"  # USDC on Arc, from Circle's docs
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ZERO = "0x" + "0" * 64

def hypersync(body):
    req = urllib.request.Request("https://arc.hypersync.xyz/query", json.dumps(body).encode(),
        {"Authorization": f"Bearer {os.environ['ENVIO_API_TOKEN']}", "Content-Type": "application/json"})
    for attempt in range(10):
        try:
            return json.load(urllib.request.urlopen(req, timeout=180))
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(6 * (attempt + 1))  # free tokens are rate limited, so wait and retry
    raise SystemExit("Still rate limited after 10 tries, run it again in a few minutes")

# A mint is a Transfer from the zero address, a burn is a Transfer to it
minted, burned = Counter(), Counter()
query = {"from_block": 0, "logs": [{"address": [USDC], "topics": [[TRANSFER], [ZERO]]}, {"address": [USDC], "topics": [[TRANSFER], [], [ZERO]]}],
         "field_selection": {"block": ["number", "timestamp"], "log": ["block_number", "address", "topic0", "topic1", "topic2", "data"]}}
while True:
    res = hypersync(query)
    for batch in res["data"]:
        times = {b["number"]: (int(b["timestamp"], 16) if isinstance(b["timestamp"], str) else b["timestamp"]) for b in batch.get("blocks", [])}
        for log in batch.get("logs", []):
            if log["address"].lower() != USDC or log["topic0"] != TRANSFER: continue
            day = datetime.fromtimestamp(times[log["block_number"]], timezone.utc)
            week = (day - timedelta(days=day.weekday())).strftime("%Y-%m-%d")
            amount = int(log["data"], 16) / 1e6
            if log["topic1"] == ZERO: minted[week] += amount
            if log["topic2"] == ZERO: burned[week] += amount
    if res["next_block"] >= res["archive_height"]: break
    query["from_block"] = res["next_block"]

supply = 0
print(f"\n{'week starting':<15}{'minted':>16}{'burned':>16}{'supply':>16}")
for week in sorted(set(minted) | set(burned)):
    supply += minted[week] - burned[week]
    print(f"{week:<15}{minted[week]:>16,.0f}{burned[week]:>16,.0f}{supply:>16,.0f}")
