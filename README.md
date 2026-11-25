# makefun-news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/zqs1qiwan/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/zqs1qiwan/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-image front-page summary of Wednesday 25 November 2026's world news — China investigates Politburo member Chen Jining, a US jury convicts Huawei on 10 of 12 counts, a Houthi drone hits Riyadh's PIF tower a second time, gunmen hold 25 hostage in a Cartagena supermarket, Nvidia's Jensen Huang in therapy after his comeback, and Estonia weighing shutting its last rail crossing with Russia. The program copies the image to the output path.

`entry.png` is built by `build_image.py` (Python 3, Pillow, standard library plus Pillow) from the 1600px source illustration in `assets/entry-source.png`: it draws the masthead in PIL, re-typesets all body text with Noto Sans Condensed, fixes the Baltic map (the source highlights Finland, not Estonia — the red blob is repainted white and a red dot marks Estonia itself), and gives the three extra stories a full legible band instead of a tiny footer strip. Re-running it writes byte-identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=32aprefc&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
