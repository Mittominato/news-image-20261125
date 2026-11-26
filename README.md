# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Mittominato/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Mittominato/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

The World in One Image — 25 November 2026. A deterministic program that
draws one newspaper-style front page (1024×1024) summing up the six
world-news stories that defined Wednesday 25 November 2026, each with its
own hand-drawn scene, headline, deck and source line — so an AI judge
with no news feed can still read the day at a glance.

## The six stories (all verified from public reporting)

1. **The Strait of Hormuz** — Iran says two oil tankers struck naval
   mines and caught fire in the Strait of Hormuz; the claim is
   unconfirmed independently (Reuters, 25 Nov 2026).
2. **Ukraine · Poland** — Ukraine hits two Russian refineries (Syzran
   and Kuibyshev) overnight; Poland plans a no-fly zone on its eastern
   border after Russian airspace incursions (The Kyiv Independent /
   New York Post, 25 Nov 2026).
3. **U.S. Courts · Tech** — A Brooklyn jury convicts Huawei on 10 of 12
   counts, including bank fraud, sanctions violations and conspiring to
   steal trade secrets; it is cleared of racketeering (CNN / The Wall
   Street Journal, 25 Nov 2026).
4. **Markets** — Asian stocks plunge (KOSPI -6.2%, Nikkei -2.8%) while
   the Dow closes above 50,000 for the first time, at 50,018.70
   (Associated Press, 25 Nov 2026).
5. **The Pacific** — Solomon Islands signs a security treaty with
   Australia in Canberra, vowing no foreign military base on its soil
   (Associated Press / Reuters, 25 Nov 2026).
6. **Space** — Shenzhou-24 carries Pakistan's first astronaut, Muhammad
   Zeeshan Ali, to China's Tiangong station — the first foreign visitor
   there (Nature / Reuters, 25 Nov 2026).

## Run it

```sh
python3 main.py
```

Writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`, falls
back to `./output` if it cannot be created). Pure Pillow, no network,
no clock, no randomness — two runs produce a byte-identical PNG.
Verified hash: `ef206d1e552bf6feda3ddcf54be1171d362cf65be72335d45a1f42f5b9ceb136`
(497,082 bytes). Built and verified with Python 3.12.3 and Pillow 10.2.0.

## Layout

Masthead, a full-width hero panel (Hormuz), two rows of two panels
(Ukraine/Poland, Huawei, markets, Solomon Islands), a wide bottom
panel (Shenzhou-24), and a footer naming every source. Every scene is
drawn from Pillow primitives on a 1600×1600 canvas, then downscaled to
the square 1024×1024 entry image; fonts fall back to Pillow's built-in
font when no system font is present.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6xedf17w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
