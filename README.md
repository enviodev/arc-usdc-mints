# USDC mints on Arc, with HyperSync

A small Python script that reads Arc with [Envio HyperSync](https://docs.envio.dev/docs/HyperSync/overview) to follow USDC minted and burned each week.

It pulls every `Transfer` of USDC to or from the zero address, then prints minted, burned and the running supply per week. It runs in about a minute, or longer on a free API token, because free tokens are rate limited.

There's nothing to install beyond Python 3.

## Run it

Get a free API token from the [HyperSync API tokens page](https://docs.envio.dev/docs/HyperSync/api-tokens), then:

```bash
export ENVIO_API_TOKEN=your-token
python3 weekly_mints.py
```

## Example output

On 30th Oct 2026, from the week mainnet launched:

```
week starting            minted          burned          supply
2026-09-14          750,478,286     130,309,717     624,560,098
2026-09-21          176,453,293     349,269,165     451,744,225
2026-09-28          525,312,863     470,955,873     506,101,215
2026-10-05          577,029,946     574,490,279     508,640,882
2026-10-12          755,228,749     602,416,786     661,452,845
2026-10-19        1,049,015,489     754,569,361     955,898,973
2026-10-26        1,228,069,021   1,113,060,446   1,070,907,548
```

Minted is gross, so it includes USDC that is later burned. It isn't new money.

## Use it with a coding agent

Paste this into Claude Code, Cursor or any coding agent from an empty folder:

```
Clone https://github.com/enviodev/arc-usdc-mints, read the README, then run weekly_mints.py with my ENVIO_API_TOKEN and explain the output. Then change it to show minted and burned per day for the last 14 days.
```

## Contract

USDC on Arc, from [Circle's docs](https://developers.circle.com/stablecoins/usdc-contract-addresses): `0x3600000000000000000000000000000000000000`
