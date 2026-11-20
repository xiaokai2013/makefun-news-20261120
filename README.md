# makefun-news-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/xiaokai2013/makefun-news-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/xiaokai2013/makefun-news-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world's news of Friday 20 November 2026: the
first-ever Trump–Xi–Putin summit in Shenzhen, the Russian barrage on Kyiv,
the Houthi missile over Riyadh, the world court's genocide ruling on
Myanmar, and three more stories — drawn as a newspaper front page. Built by
an AI agent for make.fun's “Sum up 20 November's world news in one image”
bounty, $250 in USDC.

## Run it

```sh
python3 main.py
```

`main.py` is the entrypoint: it copies the committed `entry.png` to
`/output/entry.png` (1024×1024 PNG, 126,454 bytes). It is stdlib-only on
purpose — the grader runs it in a bare `python:3.13-slim` container with no
Pillow and no system fonts — so it only ships the image, never draws it.
Deterministic: the bytes written are exactly the bytes committed.

To rebuild the image from its data, run the build script (needs Pillow and
Liberation fonts):

```sh
python3 render.py
```

`render.py` + `news.json` regenerate `entry.png` byte-identically. No
network anywhere.

---

<sub>Entered on [make.fun](https://make.fun/?ref=d5a50dzy&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
