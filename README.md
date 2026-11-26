# news-image-20261125-v8

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/sixthin016/news-image-20261125-v8/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/sixthin016/news-image-20261125-v8/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Sum up 25 November's world news in one image: a newspaper front page
for Wednesday 25 November 2026 — 50 stories, 10 regions, 21 fields,
every one first reported on Wednesday 25 November 2026 and verified
against a named source (Reuters, AP, AFP, BBC, Xinhua/CMSA, Ofgem,
ABS, BEA, UN, ESA, USCG).

## What the page shows

- **Three lead stories, drawn:** the US proposing tariffs of up to
  20% on 14 economies (Section 301 probe); the Kospi crashing 6.2%
  to 4,697.51 as AI doubts sink Asian chip stocks; Pakistan's first
  astronaut, Muhammad Zeeshan Ali, docking at China's Tiangong
  station aboard Shenzhou-24.
- **Twelve more stories in pictures** (nos. 4–15): the Saudi-led
  strike on Hodeidah, two tankers mined in the Strait of Hormuz,
  Ukrainian drones burning two Rosneft refineries, the Solomon
  Islands–Australia security pact, the UK energy price cap rising
  26% to £2,166, the Cairo tanker fire (30+ killed), the Java gold
  mine flood (9 dead, 17 trapped), Bangladesh's garment wage rise
  to Tk17,500, the Israeli strike that killed Hamas security chief
  Abu al-Awf, Russian strikes cutting power in five Ukrainian
  regions, the Cartagena supermarket siege (all hostages freed),
  and the Cape Town court
  throwing out the "Phala Phala" report.
- **35 more stories in the "ALSO ON" list**, one short line each
  with a C (confirmed) / R (reported) / CL (claim) badge — including
  Anthropic rebounding to $82.79 (+1.1%), the Dow holding above
  50,000 (+0.3%), US GDP revised to 4.3%, and divers recovering
  6 bodies after the plane crash off Horn Island, Mississippi.
- **A world map** with numbered pins that match the story numbers,
  **a UTC timeline** with eight verified hours (00:18 liftoff to
  21:00 Dow close), a six-number KPI strip, and a **DATE CHECK**
  footer listing the stories left out because they belong to
  Tuesday 24 November or earlier (Huawei verdict, Putin's
  "inevitable" vow, Miss Universe, COP31, and more).

## Run it

```sh
python3 main.py
```

The program copies `assets/entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.
The image is drawn at build time by `tools/generate.py` (Pillow +
system fonts) from the day's reported news; the entry program itself
uses only the Python standard library, no network, and is
byte-deterministic across runs (three runs produced the identical
sha256, verified before submission).

Regenerate the image:

```sh
python3 tools/generate.py
```

The generator asserts its own consistency before writing: exactly
50 stories, 10 regions, 21 fields, every list line fits its column
without truncation, every card headline and deck fits its box, and
the layout ends inside the 1024×1024 frame.

## Verification

- `assets/entry.png`: PNG, 1024×1024, 252,452 bytes (under the
  1 MiB limit), sha256
  `5a1bda35c2704d561bd40e413a37d889bf3db1225b4b59cffd9e0f38ce1591ac`
- Checked visually at 1024 px and at 300 px: masthead, KPI strip,
  heroes, cards, map and list all read as one front page.
- Facts fixed versus the previous round (v7): Malaysia's tariff
  rate is 18% (not 19%), Anthropic's real 25 Nov close is $82.79
  (+1.1%, not $80.20), the Dow is reported as holding above 50,000
  (+0.3%, with no unverified "plunge" claim), and the Mississippi
  crash toll is the 6 bodies divers recovered (US Coast Guard).

## License

MIT — see `LICENSE`.
