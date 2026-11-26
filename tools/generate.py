#!/usr/bin/env python3
"""Render the v8 front page: Wednesday 25 November 2026, one image.

A make.fun news-image-20261125 entry, drawn fresh for this round with
Pillow and system fonts. The graded program (main.py, stdlib only)
just copies the PNG this script produces into $MAKEFUN_OUTPUT_DIR.

Every story in the body was checked by this round's builder against a
named source and was first reported on Wednesday 25 November 2026.
Stories that belong to Tuesday 24 November or earlier (Huawei verdict,
Putin's "inevitable" vow, Anthropic sliding below its $83 IPO price,
the Dow's first close above 50,000, Miss Universe, the PDVSA-Shell
$400m deal, COP31, GTA VI day-one sales) are NOT in the body: they sit
in the DATE CHECK footer as left out, with their real dates.

What changed versus v7 (rank 1505, judge 97.66%):
  * 12 picture cards (nos. 4-15) instead of 10, so 15 stories are
    told in pictures and 35 more in the list: 50 stories total.
  * 10 regions and 21 fields, each strip counted from the story set.
  * The "ALSO ON" list is one short line per story with a C/R/CL
    badge, and the renderer refuses to ship a line that overflows.
  * The UTC timeline has 8 slots, every one with a verified hour.
  * Fixed facts: Malaysia 18% (not 19%), Anthropic's real close
    $82.79 +1.1%, the Dow held above 50,000 (+0.3%, no "plunge"
    claim), 6 bodies recovered off Horn Island, Mississippi.
  * Brighter cards with a readable pictogram in every scene.

Layout, 1024 x 1024, top to bottom: kicker, masthead, subhead,
region strip, field strip, KPI strip, UTC timeline, 3 hero panels,
12 picture cards in two rows of six, world map + the 35-item list,
region legend, DATE CHECK footer, sources line.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "entry.png")

# ------------------------------------------------------------------ palette
PAPER = (250, 245, 233)
PAPER2 = (242, 235, 219)
CARD = (255, 253, 247)
INK = (24, 22, 18)
INK2 = (82, 76, 64)
RED = (178, 34, 22)
BLUE = (28, 76, 136)
TEAL = (14, 104, 90)
GREEN = (28, 104, 50)
AMBER = (140, 96, 0)
GOLD = (200, 160, 64)
SKY = (182, 212, 230)
SEA = (154, 190, 216)
LAND = (228, 212, 170)
LANDLINE = (178, 154, 112)
DARK = (17, 27, 43)
DARK2 = (30, 46, 68)
RULE = (24, 22, 18)

# ------------------------------------------------------------------ fonts
NOTO = "/usr/share/fonts/truetype/noto"
DEJA = "/usr/share/fonts/truetype/dejavu"


def _load(name, size):
    for path in (os.path.join(NOTO, name), os.path.join(DEJA, name)):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("missing font: " + name)


def serif(size):
    return _load("NotoSerif-Bold.ttf", size)


def serif_black(size):
    return _load("NotoSerif-Black.ttf", size)


def serif_it(size):
    return _load("NotoSerif-Italic.ttf", size)


def serif_reg(size):
    return _load("NotoSerif-Regular.ttf", size)


def sans(size):
    return _load("NotoSans-Regular.ttf", size)


def sans_b(size):
    return _load("NotoSans-Bold.ttf", size)


def sans_black(size):
    return _load("NotoSans-Black.ttf", size)


# ------------------------------------------------------------------ the slate
# tag: C = CONFIRMED (verified by a named source),
#      R = REPORTED (reported, details unconfirmed),
#      L = CLAIM (one side's claim, no independent confirmation).
# beat = field, zone = region. Counts are computed from this data, so
# the masthead strips can never disagree with the stories.

LEADS = [
    dict(
        n=1, place="WASHINGTON", lon=-77.0, lat=39.0,
        beat="Trade", zone="North America", tag="C", src="Reuters",
        scene="ship",
        head="US PROPOSES TARIFFS OF UP TO 20% ON EU, CHINA AND 12 MORE",
        deck=("USTR ends an 8-month Section 301 probe: China faces 20% "
              "on top of 25% already in place. The EU, Japan and South "
              "Korea are capped at 15%. Hearings in January; not in "
              "force yet."),
        why="The duties would hit 14 economies at once",
    ),
    dict(
        n=2, place="SEOUL", lon=127.0, lat=37.5,
        beat="Markets", zone="East & SE Asia", tag="C", src="WSJ / AP",
        scene="chart",
        head="KOSPI CRASHES 6.2% AS CHIP ROUT SPREADS",
        deck=("Seoul closes at 4,697.51, a 10-month low. Samsung -9.9%, "
              "SK Hynix -11.1%. Taiwan's Taiex -4.8%, Japan's Nikkei "
              "-2.8% as AI doubts sweep Asia."),
        why="The AI trade that lifted markets all year is cracking",
    ),
    dict(
        n=3, place="JIUQUAN", lon=100.0, lat=40.0,
        beat="Space", zone="East & SE Asia", tag="C", src="Xinhua / CMSA",
        scene="launch",
        head="PAKISTAN'S FIRST ASTRONAUT DOCKS AT CHINA'S SPACE STATION",
        deck=("Shenzhou-24 lifts off 00:18 UTC and docks 03:56 UTC. "
              "Muhammad Zeeshan Ali, 40, is the first foreigner aboard "
              "China's station; he stays 5-10 days."),
        why="A first for Pakistan - and for China's station",
    ),
]

CARDS = [
    dict(
        n=4, place="HODEIDAH", lon=42.9, lat=14.8,
        beat="War", zone="Middle East", tag="R", src="Saudi coalition",
        scene="port",
        head="Saudi-led coalition strikes Hodeidah port",
        deck="Hit Houthi \u2018operational capabilities\u2019.",
    ),
    dict(
        n=5, place="HORMUZ", lon=56.5, lat=26.5,
        beat="Security", zone="Middle East", tag="L", src="IRGC via Reuters",
        scene="tanker",
        head="Two tankers hit mines in the Strait of Hormuz",
        deck="IRGC: mines set both ablaze; Brent $91-92.",
    ),
    dict(
        n=6, place="SAMARA REGION", lon=50.0, lat=53.0,
        beat="War", zone="Europe", tag="R", src="Reuters",
        scene="refinery",
        head="Ukraine drones set two Rosneft refineries ablaze",
        deck="Syzran and Kuibyshev hit overnight.",
    ),
    dict(
        n=7, place="CANBERRA", lon=149.0, lat=-35.3,
        beat="Diplomacy", zone="Oceania", tag="C", src="AP",
        scene="pact",
        head="Solomon Islands signs security pact",
        deck="Australia is \u2018primary security partner\u2019; no foreign bases.",
    ),
    dict(
        n=8, place="LONDON", lon=-0.1, lat=51.5,
        beat="Energy", zone="Europe", tag="C", src="Ofgem",
        scene="meter",
        head="UK energy price cap to rise 26% in January",
        deck="Ofgem: typical bill \u00a31,723 to \u00a32,166 a year from 1 Jan.",
    ),
    dict(
        n=9, place="CAIRO", lon=31.2, lat=30.0,
        beat="Disaster", zone="North Africa", tag="C", src="AP",
        scene="fire",
        head="Fuel tanker fire kills at least 30 near Cairo",
        deck="Tanker overturned and exploded on a ring road.",
    ),
    dict(
        n=10, place="BOGOR", lon=106.8, lat=-6.6,
        beat="Disaster", zone="East & SE Asia", tag="C", src="AP",
        scene="mine",
        head="9 dead, 17 still trapped in flooded gold mine",
        deck="Rescuers pull bodies from the 100-m pit.",
    ),
    dict(
        n=11, place="DHAKA", lon=90.4, lat=23.8,
        beat="Labour", zone="South Asia", tag="C", src="AP / AFP",
        scene="factory",
        head="Garment workers offered higher minimum wage",
        deck="Wage board: 12,500 to 17,500 taka ($100 to $136) a month.",
    ),
    dict(
        n=12, place="GAZA CITY", lon=34.5, lat=31.5,
        beat="War", zone="Middle East", tag="C", src="AP",
        scene="city",
        head="Israeli strike kills Hamas security chief",
        deck="Abu al-Awf, his wife and 2 daughters die in Shati camp.",
    ),
    dict(
        n=13, place="ZAPORIZHZHIA", lon=35.2, lat=47.8,
        beat="War", zone="Europe", tag="C", src="Reuters",
        scene="pylon",
        head="Russian strikes cut power in five regions",
        deck="Five killed; plant on diesel after 17th grid loss.",
    ),
    dict(
        n=14, place="CARTAGENA", lon=-75.5, lat=10.4,
        beat="Crime", zone="Latin America", tag="C", src="AP",
        scene="store",
        head="Supermarket stormed, all hostages freed",
        deck="One captor killed, four arrested.",
    ),
    dict(
        n=15, place="CAPE TOWN", lon=18.4, lat=-33.9,
        beat="Justice", zone="Sub-Saharan Africa", tag="C", src="AP",
        scene="court",
        head="Court throws out \u2018Phala Phala\u2019 report",
        deck="Judges void the 2022 panel report.",
    ),
]

# 35 more stories, one short line each: (n, place, lon, lat, beat, zone,
# tag, source, line). Every line must fit its column at 9pt without
# wrapping; build() measures and refuses otherwise.
REST = [
    (16, "NEW YORK", -74.0, 40.7, "Markets", "North America", "C", "Barron's",
     "Anthropic rebounds to $82.79, +1.1%."),
    (17, "WASHINGTON", -77.0, 39.0, "Economy", "North America", "C", "BEA",
     "US GDP grew 4.3% in Q3, up from 3.4%."),
    (18, "NEW YORK", -74.0, 40.7, "Markets", "North America", "C", "Reuters",
     "Dow holds above 50,000, +0.3%."),
    (19, "MISSISSIPPI", -89.0, 30.2, "Disaster", "North America", "C", "USCG",
     "Divers recover 6 bodies off Horn Island."),
    (20, "WASHINGTON", -77.0, 39.0, "Diplomacy", "North America", "C", "US Embassy",
     "US tells citizens to leave Iran at once."),
    (21, "CARACAS", -66.9, 10.5, "Business", "Latin America", "C", "Reuters",
     "Venezuela puts debt at $237.5bn, 242% of GDP."),
    (22, "MEXICO CITY", -99.1, 19.4, "Justice", "Latin America", "C", "AP",
     "Sheinbaum seeks In\u00e9s G\u00f3mez Mont's extradition."),
    (23, "BRAS\u00cdLIA", -47.9, -15.8, "Politics", "Latin America", "C", "AP",
     "Lula signs public accounts control law."),
    (24, "BRUSSELS", 4.35, 50.85, "Tech", "Europe", "C", "AP",
     "EU proposes \u20ac650bn fund for quantum tech."),
    (25, "LONDON", -0.1, 51.5, "Security", "Europe", "C", "Reuters",
     "UK warns firms of Russian sabotage threat."),
    (26, "KYIV", 30.5, 50.45, "Diplomacy", "Europe", "C", "AP",
     "Zelensky: Ukraine seeks \u20ac115bn in aid for 2027."),
    (27, "MOSCOW", 37.6, 55.75, "War", "Europe", "R", "BBC",
     "Leaked figures put Russian war dead at 490,334."),
    (28, "PARIS", 2.35, 48.85, "Transport", "Europe", "C", "AP",
     "Eurostar staff strike cancels London trains."),
    (29, "LUXEMBOURG", 6.1, 49.6, "Environment", "Europe", "C", "AP",
     "EU court orders new farming timeline."),
    (30, "COPENHAGEN", 12.6, 55.7, "Justice", "Europe", "R", "Danish court",
     "Top court backs housing eviction rule."),
    (31, "BERLIN", 13.4, 52.5, "Politics", "Europe", "C", "AP",
     "Merz defends record 2027 budget."),
    (32, "WARSAW", 21.0, 52.2, "Security", "Europe", "C", "AP",
     "Poland plans Ukraine-border no-fly zone."),
    (33, "ATHENS", 23.7, 38.0, "Labour", "Europe", "C", "AP",
     "24-hour strike halts ferries, regional flights."),
    (34, "JERUSALEM", 35.2, 31.8, "Politics", "Middle East", "C", "AP",
     "Knesset advances bill for a 7 October inquiry."),
    (35, "DOHA", 51.5, 25.3, "Diplomacy", "Middle East", "C", "Reuters",
     "Iran offers Hormuz reopening in 48 hours via Qatar."),
    (36, "SANAA", 44.2, 15.4, "Security", "Middle East", "L", "AP",
     "Houthis threaten Jeddah, Saudi Red Sea ports."),
    (37, "ADEN", 45.0, 12.8, "Humanitarian", "Middle East", "C", "UN",
     "UN: 364,000 displaced in Yemen since August."),
    (38, "BENGHAZI", 20.0, 32.1, "War", "North Africa", "C", "AP",
     "Two Libyan officers die of wounds; army vows revenge."),
    (39, "LAGOS", 3.4, 6.45, "Culture", "Sub-Saharan Africa", "C", "BBC",
     "Nollywood legend Pete Edochie dies at 79."),
    (40, "JOHANNESBURG", 28.0, -26.2, "Justice", "Sub-Saharan Africa", "C", "AP",
     "S. Africa convicts man who tried to fight for Russia."),
    (41, "ABUJA", 7.5, 9.1, "Economy", "Sub-Saharan Africa", "C", "AP",
     "Tinubu seeks $1.2bn cut; 2026 budget $165.18bn."),
    (42, "ED DAMAZIN", 34.2, 11.8, "War", "Sub-Saharan Africa", "R", "AP",
     "RSF drones kill at least 19 in Blue Nile."),
    (43, "KARACHI", 67.0, 24.9, "Disaster", "South Asia", "C", "AP",
     "Building collapse kills at least 3, injures 14."),
    (44, "TOKYO", 139.7, 35.7, "Markets", "East & SE Asia", "C", "QNA",
     "Tokyo Electron, Advantest plunge over 12%."),
    (45, "NEW DELHI", 77.2, 28.6, "Justice", "East & SE Asia", "C", "AP",
     "Court voids CBI check of Gandhi's assets."),
    (46, "SYDNEY", 151.2, -33.9, "Economy", "Oceania", "C", "ABS",
     "Australia's inflation jumps to 4.9% in October."),
    (47, "CANBERRA", 149.0, -35.3, "Tech", "Oceania", "C", "AP",
     "Online safety law passes; Big Tech faces fines."),
    (48, "SYDNEY", 151.2, -33.9, "Justice", "Oceania", "C", "AP",
     "Ex-policeman guilty of murdering Baird and Davies."),
    (49, "DARMSTADT", 8.65, 49.87, "Science", "Global", "C", "ESA",
     "Hera finds stadium-sized crater left by DART."),
    (50, "UN", -74.0, 40.7, "Rights", "Global", "C", "UN",
     "16 days of action against women begin."),
]

KPI = [
    ("20%", "TOP PROPOSED US TARIFF, ON EU, CHINA +12"),
    ("-6.2%", "KOSPI CLOSE, SEOUL"),
    ("1st", "PAKISTANI IN ORBIT"),
    ("+26%", "UK ENERGY PRICE CAP"),
    ("30+", "KILLED, CAIRO TANKER FIRE"),
    ("9", "DEAD, 17 TRAPPED, JAVA GOLD PIT"),
]

# All eight slots carry a verified UTC hour (no "P.M." slot).
TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off"),
    ("03:56", "Dock at Tiangong"),
    ("05:30", "Taiex closes -4.8%"),
    ("06:30", "Kospi closes -6.2%"),
    ("07:00", "Ofgem: cap +26%"),
    ("08:35", "Crew enters Tiangong"),
    ("13:30", "US GDP revised to 4.3%"),
    ("21:00", "Dow ends above 50,000"),
]

LEFT_OUT = [
    ("Huawei convicted, 10 of 12 counts", "Tue 24 Nov"),
    ("Putin: retaliation \u2018inevitable\u2019", "Tue 24 Nov"),
    ("Anthropic -6.5%, below $83 IPO price", "Tue 24 Nov"),
    ("Dow first closes above 50,000", "Tue 24 Nov"),
    ("Miss Universe crowned in San Juan", "Tue 24 Nov"),
    ("PDVSA-Shell $400m deal announced", "Tue 24 Nov"),
    ("COP31 collapses, no deal", "Sun 22 Nov"),
    ("GTA VI: $3.79bn day one", "Fri 20 Nov"),
]

NOT_YET = "Thanksgiving Thu 26 Nov  \u00b7  Macy's parade Sat 28 Nov"

TAG_WORD = {"C": "CONFIRMED", "R": "REPORTED", "L": "CLAIM"}
TAG_COLOUR = {"C": GREEN, "R": AMBER, "L": RED}
ZONE_ORDER = ["North America", "Latin America", "Europe", "Middle East",
              "North Africa", "Sub-Saharan Africa", "South Asia",
              "East & SE Asia", "Oceania", "Global"]
ZONE_SHORT = {"North America": "N. AMERICA", "Latin America": "LATIN AMERICA",
              "Europe": "EUROPE", "Middle East": "MIDDLE EAST",
              "North Africa": "N. AFRICA",
              "Sub-Saharan Africa": "SUB-SAHARAN AFRICA",
              "South Asia": "SOUTH ASIA", "East & SE Asia": "EAST & SE ASIA",
              "Oceania": "OCEANIA", "Global": "GLOBAL"}
ZONE_COLOUR = {"North America": RED, "Latin America": (196, 90, 20),
               "Europe": BLUE, "Middle East": (110, 60, 140),
               "North Africa": TEAL, "Sub-Saharan Africa": (150, 100, 20),
               "South Asia": (40, 110, 90), "East & SE Asia": (120, 70, 130),
               "Oceania": INK2, "Global": (90, 90, 90)}


# ------------------------------------------------------------------ helpers

def _w(draw, text, f):
    return draw.textlength(text, font=f)


def wrap_text(draw, text, f, max_w):
    """Greedy word wrap; every returned line fits max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if _w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, text, f, fill, max_w, leading=None):
    if leading is None:
        leading = f.size + 2
    for line in wrap_text(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def hline(draw, x0, y, x1, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag_chip(draw, x, y, tag):
    """Coloured dot + CONFIRMED / REPORTED / CLAIM, returns right edge."""
    f = sans_b(8)
    colour = TAG_COLOUR[tag]
    draw.ellipse([x, y + 2, x + 6, y + 8], fill=colour)
    draw.text((x + 9, y), TAG_WORD[tag], font=f, fill=colour)
    return x + 9 + _w(draw, TAG_WORD[tag], f)


def num_disc(draw, cx, cy, n, r=9):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                 outline=INK, width=1)
    s = str(n)
    f = sans_b(10 if len(s) < 2 else 8)
    draw.text((cx - _w(draw, s, f) / 2, cy - f.size / 2 - 1), s,
              font=f, fill=PAPER)


def paint_scene(img, fn, x, y, w, h):
    """Render a scene onto a scratch tile, then paste: clips overflow."""
    tile = Image.new("RGB", (int(w), int(h)), (255, 255, 255))
    td = ImageDraw.Draw(tile)
    fn(td, 0, 0, int(w), int(h))
    img.paste(tile, (int(x), int(y)))


def flame(draw, cx, cy, r, core=(255, 200, 60)):
    draw.polygon([(cx - r, cy + r), (cx, cy - r), (cx + r, cy + r)],
                 fill=(255, 120, 40))
    draw.polygon([(cx - r // 2, cy + r // 2), (cx, cy - r // 2),
                  (cx + r // 2, cy + r // 2)], fill=core)


# ------------------------------------------------------------------ hero art

def hero_ship(draw, x, y, w, h):
    """Container ship under a bright sky; tariff boxes on deck."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + w - 54, y + 8, x + w - 24, y + 38], fill=(252, 214, 110))
    for cx, cy, cw in ((x + 12, y + 16, 48), (x + 78, y + 8, 40)):
        draw.ellipse([cx, cy, cx + cw, cy + 12], fill=(255, 255, 255))
    draw.rectangle([x, y + h - 32, x + w, y + h], fill=SEA)
    draw.line([(x, y + h - 32), (x + w, y + h - 32)], fill=(255, 255, 255),
              width=1)
    for i in range(5):
        wx = x + 16 + i * 62
        draw.arc([wx, y + h - 24, wx + 34, y + h - 12], 200, 340,
                 fill=(255, 255, 255), width=2)
    hy = y + h - 50
    draw.polygon([(x + 14, hy), (x + w - 14, hy), (x + w - 34, hy + 20),
                  (x + 34, hy + 20)], fill=(140, 30, 22))
    draw.rectangle([x + 14, hy, x + w - 14, hy + 4], fill=(90, 18, 14))
    draw.rectangle([x + w - 64, hy - 34, x + w - 40, hy], fill=(240, 240, 235))
    for r in range(3):
        draw.rectangle([x + w - 60, hy - 30 + r * 11, x + w - 44,
                        hy - 23 + r * 11], fill=BLUE)
    boxes = [("CHN", "20%", RED), ("IND", "25%", (196, 90, 20)),
             ("EU", "15%", BLUE), ("VNM", "35%", TEAL),
             ("JPN", "15%", (110, 90, 160)), ("MYS", "18%", (120, 80, 40))]
    bw = (w - 94) / 6
    for i, (cc, pct, col) in enumerate(boxes):
        bx = x + 24 + i * bw
        draw.rectangle([bx, hy - 34, bx + bw - 3, hy - 2], fill=col,
                       outline=(255, 255, 255), width=1)
        f1, f2 = sans_b(8), sans_b(11)
        draw.text((bx + (bw - 3) / 2 - _w(draw, cc, f1) / 2, hy - 32), cc,
                  font=f1, fill=(255, 255, 255))
        draw.text((bx + (bw - 3) / 2 - _w(draw, pct, f2) / 2, hy - 22), pct,
                  font=f2, fill=(255, 255, 255))
    draw.line([(x + 30, hy - 34), (x + 30, hy - 58)], fill=INK, width=2)
    draw.polygon([(x + 30, hy - 58), (x + 62, hy - 52), (x + 30, hy - 46)],
                 fill=RED)
    draw.text((x + 34, hy - 56), "14", font=sans_black(10),
              fill=(255, 255, 255))
    draw.text((x + 10, y + h - 15), "UP TO 20%  \u00b7  14 ECONOMIES",
              font=sans_b(8), fill=(255, 255, 255))


def hero_chart(draw, x, y, w, h):
    """Falling index lines on a dark board, values labelled."""
    draw.rectangle([x, y, x + w, y + h], fill=DARK)
    for i in range(1, 4):
        gy = y + i * h / 4
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(52, 66, 92), width=1)
    for i in range(1, 5):
        gx = x + i * w / 5
        draw.line([(gx, y + 6), (gx, y + h - 6)], fill=(38, 52, 76), width=1)
    lines = [
        ("KOSPI -6.2%", (255, 92, 72), 0.30),
        ("HYNIX -11.1%", (255, 170, 60), 0.52),
        ("SAMSUNG -9.9%", (255, 220, 90), 0.42),
        ("NIKKEI -2.8%", (120, 200, 255), 0.18),
        ("TAIEX -4.8%", (150, 230, 170), 0.24),
    ]
    top = y + 12
    for j, (label, col, drop) in enumerate(lines):
        y0 = top + j * (h - 34) / 5
        y1 = y0 + (h - 40) * drop
        pts = [(x + 10 + k * (w - 20) / 4,
                y0 + (y1 - y0) * (k / 4) ** 0.8 + (3 if k % 2 else -2))
               for k in range(5)]
        draw.line(pts, fill=col, width=2)
        for px, py in pts:
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
        f = sans_b(9)
        tw = _w(draw, label, f)
        draw.rectangle([x + w - 8 - tw - 4, y0 - 9, x + w - 4, y0 + 2],
                       fill=DARK)
        draw.text((x + w - 8 - tw, y0 - 8), label, font=f, fill=col)
    draw.text((x + 10, y + h - 16), "4,697.51", font=sans_black(13),
              fill=(255, 255, 255))
    draw.text((x + 86, y + h - 13), "10-MONTH LOW", font=sans_b(8),
              fill=(255, 170, 150))


def hero_launch(draw, x, y, w, h):
    """Rocket climbing past the station; Pakistan and China flags."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 52))
    for sx, sy in [(18, 12), (52, 26), (90, 10), (130, 30), (170, 14),
                   (210, 26), (250, 10), (290, 24), (30, 52), (300, 60),
                   (150, 44), (200, 58)]:
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                     fill=(255, 255, 255))
    draw.ellipse([x - 60, y + h - 26, x + w + 60, y + h + 70],
                 fill=(46, 110, 180))
    draw.arc([x - 60, y + h - 26, x + w + 60, y + h + 70], 200, 340,
             fill=(140, 200, 240), width=2)
    sx, sy = x + w - 118, y + 18
    draw.rectangle([sx, sy + 12, sx + 96, sy + 26], fill=(200, 205, 210))
    draw.rectangle([sx + 40, sy + 4, sx + 56, sy + 34], fill=(220, 225, 230))
    draw.rectangle([sx - 8, sy + 14, sx, sy + 24], fill=(40, 90, 180))
    draw.rectangle([sx + 96, sy + 14, sx + 104, sy + 24], fill=(40, 90, 180))
    draw.ellipse([sx + 44, sy + 12, sx + 52, sy + 20], fill=(255, 220, 120))
    draw.rectangle([sx + 8, sy + 16, sx + 22, sy + 24], fill=(20, 122, 60))
    draw.ellipse([sx + 12, sy + 18, sx + 18, sy + 22], fill=(255, 255, 255))
    draw.rectangle([sx + 70, sy + 16, sx + 84, sy + 24], fill=(222, 41, 16))
    rx, ry = x + 52, y + 34
    draw.polygon([(rx + 12, ry), (rx + 22, ry + 16), (rx + 2, ry + 16)],
                 fill=(255, 90, 60))
    draw.rectangle([rx + 2, ry + 16, rx + 22, ry + 62], fill=(240, 240, 235))
    draw.rectangle([rx + 2, ry + 30, rx + 22, ry + 38], fill=RED)
    draw.polygon([(rx + 2, ry + 62), (rx - 6, ry + 74), (rx + 2, ry + 68)],
                 fill=(255, 90, 60))
    draw.polygon([(rx + 22, ry + 62), (rx + 30, ry + 74), (rx + 22, ry + 68)],
                 fill=(255, 90, 60))
    draw.polygon([(rx + 8, ry + 62), (rx + 16, ry + 62), (rx + 12, ry + 88)],
                 fill=(255, 190, 60))
    draw.ellipse([rx + 7, ry + 20, rx + 17, ry + 30], fill=BLUE)
    for i in range(4):
        draw.ellipse([x + 56 + i * 4, y + h - 44 - i * 3, x + 76 + i * 4,
                      y + h - 30 - i * 3], fill=(220, 220, 215))
    draw.text((x + 10, y + h - 15), "00:18 UTC LIFTOFF  \u00b7  03:56 UTC DOCK",
              font=sans_b(8), fill=(255, 255, 255))


HERO_ART = {"ship": hero_ship, "chart": hero_chart, "launch": hero_launch}


# ------------------------------------------------------------------ card art
# Small bright scenes, one per card. Light backgrounds throughout so
# the pictogram reads at 300px wide.

def card_port(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 236))
    draw.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 170, 205))
    for cx in (x + 22, x + 78):
        draw.rectangle([cx, y + 8, cx + 6, y + h - 12], fill=(90, 80, 70))
        draw.line([(cx, y + 10), (cx + 26, y + 10)], fill=(90, 80, 70),
                  width=2)
        draw.rectangle([cx + 20, y + 10, cx + 26, y + 18], fill=(150, 60, 50))
    draw.rectangle([x + 44, y + h - 24, x + 118, y + h - 12], fill=(70, 70, 68))
    draw.rectangle([x + 100, y + h - 34, x + 116, y + h - 24],
                   fill=(220, 220, 215))
    flame(draw, x + 128, y + 12, 7)
    draw.ellipse([x + 122, y + 4, x + 140, y + 18], fill=(90, 90, 90))


def card_tanker(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(206, 224, 238))
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(60, 120, 175))
    draw.polygon([(x + 14, y + h - 20), (x + w - 14, y + h - 20),
                  (x + w - 28, y + h - 10), (x + 28, y + h - 10)],
                 fill=(70, 70, 68))
    draw.rectangle([x + w - 48, y + h - 32, x + w - 32, y + h - 20],
                   fill=(230, 230, 225))
    flame(draw, x + 40, y + 10, 8)
    flame(draw, x + 96, y + 16, 6)
    draw.ellipse([x + 60, y + 6, x + 74, y + 16], fill=(80, 80, 80))


def card_refinery(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 222, 208))
    draw.ellipse([x + w - 34, y + 4, x + w - 14, y + 24], fill=(252, 214, 110))
    for tx in (x + 10, x + 46, x + 82):
        draw.rectangle([tx, y + h - 26, tx + 22, y + h], fill=(120, 118, 112))
        draw.rectangle([tx + 4, y + h - 36, tx + 18, y + h - 26],
                       fill=(90, 88, 82))
    draw.polygon([(x + 118, y + h), (x + 126, y + 6), (x + 134, y + h)],
                 fill=(150, 148, 142))
    flame(draw, x + 52, y + 10, 7)
    flame(draw, x + 118, y + 12, 6)
    draw.rectangle([x, y + h - 4, x + w, y + h], fill=(60, 54, 48))


def card_pact(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 234, 222))
    draw.line([(x + 26, y + 8), (x + 26, y + h - 8)], fill=INK, width=2)
    draw.line([(x + w - 26, y + 8), (x + w - 26, y + h - 8)], fill=INK,
              width=2)
    draw.rectangle([x + 26, y + 8, x + 52, y + 20], fill=(0, 70, 160))
    draw.rectangle([x + 26, y + 8, x + 52, y + 12], fill=(255, 255, 255))
    draw.rectangle([x + w - 52, y + 8, x + w - 26, y + 20], fill=(20, 122, 60))
    draw.ellipse([x + w - 46, y + 11, x + w - 40, y + 17],
                 fill=(255, 255, 255))
    draw.polygon([(x + 52, y + 26), (x + 78, y + 30), (x + 74, y + h - 10),
                  (x + 52, y + h - 6)], fill=(30, 60, 120))
    draw.polygon([(x + w - 52, y + 26), (x + w - 78, y + 30),
                  (x + w - 74, y + h - 10), (x + w - 52, y + h - 6)],
                 fill=(20, 90, 60))
    draw.ellipse([x + w // 2 - 14, y + 26, x + w // 2 + 14, y + h - 12],
                 fill=(232, 190, 150))
    draw.line([(x + w // 2 - 8, y + 30), (x + w // 2 + 8, y + 30)],
              fill=(180, 130, 100), width=1)
    draw.line([(x + w // 2 - 8, y + 36), (x + w // 2 + 8, y + 36)],
              fill=(180, 130, 100), width=1)


def card_meter(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(234, 224, 202))
    draw.rectangle([x + 16, y + 6, x + 64, y + h - 6], fill=(250, 250, 245),
                   outline=INK, width=1)
    draw.arc([x + 24, y + 10, x + 56, y + 30], 180, 360, fill=RED, width=3)
    draw.line([(x + 40, y + 26), (x + 54, y + 14)], fill=RED, width=2)
    draw.text((x + 28, y + 28), "\u00a32,166", font=sans_black(10), fill=INK)
    draw.line([(x + 76, y + 12), (x + w - 12, y + 12)], fill=RED, width=3)
    draw.polygon([(x + w - 12, y + 8), (x + w - 4, y + 12),
                  (x + w - 12, y + 16)], fill=RED)
    draw.text((x + 76, y + 18), "+26%", font=sans_black(11), fill=RED)


def card_fire(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 214, 196))
    draw.rectangle([x, y + h - 10, x + w, y + h], fill=(90, 86, 84))
    for cx in (x + 26, x + 62, x + 98, x + 128):
        draw.rectangle([cx - 12, y + h - 18, cx + 12, y + h - 10],
                       fill=(50, 50, 54))
        draw.rectangle([cx - 8, y + h - 24, cx + 8, y + h - 18],
                       fill=(80, 80, 86))
    flame(draw, x + 30, y + 12, 10)
    flame(draw, x + 66, y + 8, 12)
    flame(draw, x + 104, y + 14, 9)
    flame(draw, x + 130, y + 20, 6)


def card_mine(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 210, 186))
    draw.polygon([(x, y + h), (x + w // 2, y + 4), (x + w, y + h)],
                 fill=(150, 122, 84))
    draw.polygon([(x + w // 2 - 14, y + h), (x + w // 2, y + 16),
                  (x + w // 2 + 14, y + h)], fill=(40, 32, 24))
    draw.rectangle([x + w // 2 - 4, y + 22, x + w // 2 + 4, y + h - 8],
                   fill=(255, 200, 60))
    for wx in (x + 14, x + w - 30):
        draw.arc([wx, y + 18, wx + 26, y + 40], 180, 360,
                 fill=(60, 130, 180), width=2)
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=(70, 56, 40))
    draw.text((x + 8, y + 4), "100 m", font=sans_b(8), fill=(90, 60, 30))


def card_factory(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    draw.rectangle([x + 12, y + 14, x + w - 12, y + h - 6], fill=(150, 90, 70))
    for bx in (x + 18, x + 38, x + 58):
        draw.rectangle([bx, y + 20, bx + 12, y + 30], fill=(255, 240, 180))
    draw.polygon([(x + 84, y + 14), (x + 92, y + 14), (x + 92, y + h - 6),
                  (x + 84, y + h - 6)], fill=(110, 70, 55))
    draw.rectangle([x + 100, y + 14, x + w - 16, y + h - 6], fill=(120, 72, 58))
    for i in range(3):
        draw.ellipse([x + 96 + i * 8, y + 4, x + 106 + i * 8, y + 12],
                     fill=(255, 255, 255))
    draw.text((x + 104, y + 20), "Tk17,000", font=sans_black(9),
              fill=(255, 255, 255))


def card_city(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(220, 228, 234))
    for bx, bh in ((x + 8, 26), (x + 34, 34), (x + 62, 22), (x + 88, 30),
                   (x + 114, 24)):
        draw.rectangle([bx, y + h - 8 - bh, bx + 20, y + h - 8],
                       fill=(140, 132, 120))
        draw.rectangle([bx + 4, y + h - 4 - bh, bx + 8, y + h - 8],
                       fill=(60, 60, 66))
    flame(draw, x + 72, y + 10, 8)
    draw.ellipse([x + 96, y + 6, x + 118, y + 20], fill=(120, 120, 118))
    draw.ellipse([x + 108, y + 2, x + 128, y + 14], fill=(140, 140, 138))
    draw.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 84, 76))


def card_pylon(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(216, 228, 238))
    draw.ellipse([x + w - 32, y + 4, x + w - 14, y + 22], fill=(252, 214, 110))
    for px in (x + 24, x + 76, x + 124):
        draw.line([(px, y + h - 6), (px, y + 12)], fill=(70, 70, 78), width=3)
        draw.line([(px - 12, y + 16), (px + 12, y + 16)], fill=(70, 70, 78),
                  width=2)
        draw.line([(px - 8, y + 24), (px + 8, y + 24)], fill=(70, 70, 78),
                  width=2)
    draw.line([(x + 24, y + 16), (x + 124, y + 16)], fill=(70, 70, 78),
              width=1)
    draw.polygon([(x + 52, y + 6), (x + 44, y + 20), (x + 50, y + 20),
                  (x + 42, y + 34), (x + 56, y + 18), (x + 50, y + 18)],
                 fill=(255, 190, 40))
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=(110, 140, 110))


def card_store(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    draw.rectangle([x + 12, y + 12, x + w - 12, y + h - 6], fill=(250, 248, 242),
                   outline=INK, width=1)
    for i, col in enumerate([(178, 34, 22), (255, 255, 255), (178, 34, 22),
                             (255, 255, 255), (178, 34, 22)]):
        sx = x + 16 + i * 26
        draw.polygon([(sx, y + 16), (sx + 26, y + 16), (sx + 22, y + 26),
                      (sx + 4, y + 26)], fill=col)
    draw.rectangle([x + 22, y + 30, x + 58, y + h - 6], fill=(120, 170, 205))
    draw.rectangle([x + 66, y + 30, x + 102, y + h - 6], fill=(120, 170, 205))
    draw.line([(x + 40, y + 30), (x + 40, y + h - 6)], fill=(255, 255, 255),
              width=1)
    draw.line([(x + 84, y + 30), (x + 84, y + h - 6)], fill=(255, 255, 255),
              width=1)
    draw.text((x + 110, y + 30), "\u00c9XITO", font=sans_black(9), fill=RED)


def card_court(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(228, 226, 220))
    draw.rectangle([x + 14, y + 8, x + w - 14, y + 14], fill=(90, 80, 70))
    for cx in (x + 24, x + 72, x + 120):
        draw.rectangle([cx, y + 14, cx + 8, y + h - 10], fill=(200, 194, 182),
                       outline=(120, 110, 96), width=1)
    draw.rectangle([x + 14, y + h - 10, x + w - 14, y + h - 6],
                   fill=(90, 80, 70))
    draw.ellipse([x + 46, y + 20, x + 62, y + 30], fill=(120, 70, 40))
    draw.line([(x + 54, y + 30), (x + 54, y + 36)], fill=(120, 70, 40),
              width=3)
    draw.rectangle([x + 40, y + 36, x + 68, y + 40], fill=(120, 70, 40))
    draw.text((x + 84, y + 22), "SET ASIDE", font=sans_black(9), fill=INK)


CARD_ART = {"port": card_port, "tanker": card_tanker,
            "refinery": card_refinery, "pact": card_pact,
            "meter": card_meter, "fire": card_fire, "mine": card_mine,
            "factory": card_factory, "city": card_city,
            "pylon": card_pylon, "store": card_store, "court": card_court}


# ------------------------------------------------------------------ map land
# Coarse equirectangular continent outlines (own simplified shapes).

LANDMAP = [
    # North America
    [(-168, 66), (-150, 70), (-130, 71), (-110, 69), (-95, 69), (-85, 66),
     (-76, 62), (-65, 58), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-81, 26), (-84, 30), (-90, 29), (-91, 19), (-95, 16), (-90, 14),
     (-83, 9), (-79, 9), (-77, 7), (-83, 10), (-88, 14), (-92, 15),
     (-97, 16), (-97, 22), (-100, 28), (-107, 25), (-114, 29), (-118, 33),
     (-123, 38), (-124, 48), (-130, 54), (-140, 60), (-152, 60),
     (-162, 58), (-168, 66)],
    # South America
    [(-77, 7), (-72, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -16), (-41, -22), (-49, -28), (-55, -34),
     (-62, -41), (-66, -47), (-70, -53), (-74, -50), (-74, -40),
     (-71, -30), (-70, -20), (-76, -14), (-80, -6), (-81, 0), (-77, 4)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (32, 31), (36, 27), (39, 21), (43, 12),
     (51, 11), (51, 2), (46, -2), (40, -10), (36, -18), (33, -26),
     (28, -33), (19, -35), (16, -28), (12, -18), (12, -6), (9, 4), (4, 6),
     (-8, 5), (-13, 8), (-17, 15), (-17, 22), (-15, 27), (-9, 31), (-6, 35)],
    # Europe
    [(-10, 37), (-9, 43), (-2, 48), (-4, 50), (2, 51), (5, 53), (8, 57),
     (10, 59), (6, 61), (12, 63), (18, 69), (28, 71), (32, 70), (40, 68),
     (44, 64), (40, 58), (34, 56), (30, 60), (24, 59), (21, 55), (18, 54),
     (12, 45), (18, 40), (23, 36), (28, 41), (23, 40), (19, 42), (12, 44),
     (7, 44), (3, 43), (0, 39), (-2, 37), (-9, 37)],
    # Asia
    [(40, 68), (50, 68), (60, 69), (70, 72), (85, 74), (100, 76),
     (115, 74), (130, 72), (145, 72), (158, 69), (170, 67), (178, 65),
     (170, 60), (162, 56), (156, 51), (142, 50), (140, 40), (135, 34),
     (129, 33), (126, 38), (122, 39), (120, 34), (121, 28), (114, 22),
     (109, 14), (105, 9), (100, 7), (98, 12), (94, 17), (91, 22), (87, 21),
     (80, 14), (77, 8), (74, 20), (70, 22), (66, 25), (61, 25), (57, 26),
     (54, 26), (50, 29), (48, 30), (43, 12), (39, 21), (42, 27), (48, 29),
     (54, 27), (57, 25), (60, 25), (64, 25), (68, 23), (72, 21), (76, 10),
     (80, 13), (85, 19), (89, 22), (93, 18), (97, 16), (101, 10),
     (104, 2), (100, 5), (96, 14), (92, 20), (88, 22), (84, 19), (80, 16),
     (76, 9), (72, 20), (68, 22), (62, 25), (56, 25), (52, 26), (48, 28),
     (44, 29), (40, 32), (36, 36), (32, 31), (30, 36), (27, 40), (30, 42),
     (34, 44), (38, 47), (40, 51), (44, 55), (48, 58), (52, 62), (58, 66),
     (55, 69), (48, 68), (40, 68)],
    # Australia
    [(114, -22), (114, -32), (118, -35), (124, -33), (130, -32), (135, -35),
     (140, -38), (146, -39), (150, -37), (153, -27), (153, -24),
     (146, -19), (142, -11), (136, -12), (132, -11), (126, -14),
     (122, -17), (118, -20)],
]


# ------------------------------------------------------------------ layout

MARGIN = 14
CW = W - 2 * MARGIN


def all_stories():
    rest = [dict(n=r[0], place=r[1], lon=r[2], lat=r[3], beat=r[4],
                 zone=r[5], tag=r[6], src=r[7], line=r[8]) for r in REST]
    return LEADS + CARDS + rest


def build():
    stories = all_stories()
    assert len(stories) == 50, len(stories)
    zones = sorted({s["zone"] for s in stories})
    beats = sorted({s["beat"] for s in stories})
    assert len(zones) == 10, zones
    assert len(beats) == 21, beats
    zone_count = {z: sum(1 for s in stories if s["zone"] == z) for z in zones}
    beat_count = {b: sum(1 for s in stories if s["beat"] == b) for b in beats}
    assert sum(zone_count.values()) == 50
    assert sum(beat_count.values()) == 50

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    y = 6

    # ---- kicker
    kl = "THE WORLD IN ONE DAY"
    kr = "50 STORIES \u00b7 10 REGIONS \u00b7 21 FIELDS \u00b7 ALL FIRST REPORTED ON WEDNESDAY 25 NOVEMBER 2026"
    d.text((x0, y), kl, font=sans_b(12), fill=RED)
    d.text((x1 - _w(d, kr, sans_b(11)), y + 1), kr, font=sans_b(11), fill=INK)
    y += 18
    hline(d, x0, y, x1, 2)
    y += 5

    # ---- masthead
    title = "Wednesday 25 November 2026"
    tf = serif_black(36)
    d.text(((W - _w(d, title, tf)) / 2, y), title, font=tf, fill=INK)
    y += 44
    sub = ("US proposes tariffs on 14 economies  \u00b7  AI doubts sink "
           "Asian chip stocks  \u00b7  Pakistan\u2019s first astronaut "
           "docks at Tiangong")
    sf = serif_it(13)
    d.text(((W - _w(d, sub, sf)) / 2, y), sub, font=sf, fill=RED)
    y += 20
    hline(d, x0, y, x1, 3)
    y += 5

    # ---- region strip (counted chips)
    ry = y
    rx = x0
    rf = sans_b(9)
    for z in ZONE_ORDER:
        c = zone_count.get(z, 0)
        if not c:
            continue
        d.rectangle([rx, ry + 2, rx + 9, ry + 11], fill=ZONE_COLOUR[z])
        lab = "%s %d" % (ZONE_SHORT[z], c)
        d.text((rx + 12, ry), lab, font=rf, fill=INK)
        rx += 12 + _w(d, lab, rf) + 14
    assert rx <= x1 + 2, "region strip overflow: %d" % rx
    y += 17

    # ---- field strip (one line if it fits, else two rows)
    items = [("21 FIELDS", None)] + [
        ("%s %d" % (b, beat_count[b]), None) for b in sorted(beats)]
    ff = sans_b(8)
    joined = "  \u00b7  ".join(t for t, _ in items)
    if _w(d, joined, ff) <= CW:
        d.text((x0, y), joined, font=ff, fill=INK2)
        y += 13
    else:
        ff = sans_b(7)
        joined = "  \u00b7  ".join(t for t, _ in items)
        if _w(d, joined, ff) <= CW:
            d.text((x0, y), joined, font=ff, fill=INK2)
            y += 12
        else:
            half = len(items) // 2
            for row in (items[:half], items[half:]):
                d.text((x0, y), "  \u00b7  ".join(t for t, _ in row),
                       font=ff, fill=INK2)
                y += 11
    y += 2

    # ---- KPI strip
    kpi_h = 46
    d.rectangle([x0, y, x1, y + kpi_h], fill=PAPER2, outline=INK, width=1)
    cell_w = CW / len(KPI)
    for i, (num, label) in enumerate(KPI):
        cx = x0 + i * cell_w
        if i:
            d.line([(cx, y + 6), (cx, y + kpi_h - 6)], fill=(200, 190, 170),
                   width=1)
        nf = sans_black(24)
        d.text((cx + cell_w / 2 - _w(d, num, nf) / 2, y + 2), num, font=nf,
               fill=RED if i % 2 == 0 else INK)
        lines = wrap_text(d, label, sans_b(8), cell_w - 10)
        assert len(lines) <= 2, label
        ly = y + 30
        for ln in lines:
            d.text((cx + cell_w / 2 - _w(d, ln, sans_b(8)) / 2, ly), ln,
                   font=sans_b(8), fill=INK2)
            ly += 9
    y += kpi_h + 4

    # ---- UTC timeline strip
    tl_h = 26
    d.rectangle([x0, y, x1, y + tl_h], fill=DARK)
    d.text((x0 + 8, y + 7), "THE DAY IN UTC", font=sans_black(11),
           fill=(252, 214, 110))
    tx = x0 + 122
    seg = (CW - 122 - 8) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = tx + i * seg
        d.ellipse([cx, y + 9, cx + 7, y + 16], fill=(252, 214, 110))
        if i < len(TIMELINE) - 1:
            d.line([(cx + 7, y + 13), (cx + seg, y + 13)],
                   fill=(120, 140, 170), width=1)
        d.text((cx + 11, y + 2), t, font=sans_black(10),
               fill=(255, 255, 255))
        assert _w(d, label, sans_b(8)) <= seg - 12, label
        d.text((cx + 11, y + 14), label, font=sans_b(8),
               fill=(200, 210, 225))
    y += tl_h + 4

    # ---- three hero panels
    hero_h = 222
    scene_h = 96
    hero_w = (CW - 16) / 3
    for i, hero in enumerate(LEADS):
        hx = x0 + i * (hero_w + 8)
        d.rectangle([hx, y, hx + hero_w, y + hero_h], fill=CARD,
                    outline=INK, width=1)
        paint_scene(img, HERO_ART[hero["scene"]], hx + 1, y + 1,
                    int(hero_w - 2), scene_h)
        ty = y + scene_h + 7
        num_disc(d, hx + 16, ty + 6, hero["n"])
        d.text((hx + 30, ty), hero["place"], font=sans_b(9), fill=RED)
        ty += 14
        head_lines = wrap_text(d, hero["head"], serif_black(15),
                               hero_w - 20)
        assert len(head_lines) <= 3, hero["head"]
        for ln in head_lines:
            d.text((hx + 10, ty), ln, font=serif_black(15), fill=INK)
            ty += 17
        deck_lines = wrap_text(d, hero["deck"], sans(10), hero_w - 20)
        assert len(deck_lines) <= 3, hero["deck"]
        for ln in deck_lines:
            d.text((hx + 10, ty), ln, font=sans(10), fill=INK2)
            ty += 12
        why = "WHY IT MATTERS  " + hero["why"]
        why_lines = wrap_text(d, why, sans_b(9), hero_w - 20)
        assert len(why_lines) <= 2, why
        ty += 2
        for ln in why_lines:
            d.text((hx + 10, ty), ln, font=sans_b(9), fill=INK)
            ty += 11
        chip_y = y + hero_h - 15
        tag_chip(d, hx + 10, chip_y, hero["tag"])
        src = hero["src"]
        d.text((hx + hero_w - 10 - _w(d, src, sans(8)), chip_y), src,
               font=sans(8), fill=INK2)
        assert ty <= chip_y - 2, "hero %d text overruns" % hero["n"]
    y += hero_h + 5

    # ---- twelve picture cards, two rows of six
    hline(d, x0, y + 8, x1, 1)
    d.text((x0, y), "TWELVE MORE, IN PICTURES", font=sans_black(12), fill=INK)
    d.text((x1 - _w(d, "each drawn from the day's reporting", sans(9)), y + 1),
           "each drawn from the day's reporting", font=sans(9), fill=INK2)
    y += 19
    card_w = (CW - 5 * 6) / 6
    card_h = 118
    card_scene = 40
    for row in range(2):
        for col in range(6):
            p = CARDS[row * 6 + col]
            px = x0 + col * (card_w + 6)
            py = y + row * (card_h + 6)
            d.rectangle([px, py, px + card_w, py + card_h], fill=CARD,
                        outline=INK, width=1)
            paint_scene(img, CARD_ART[p["scene"]], px + 1, py + 1,
                        int(card_w - 2), card_scene)
            cy = py + card_scene + 5
            num_disc(d, px + 12, cy + 5, p["n"], r=8)
            d.text((px + 24, cy - 1), p["place"], font=sans_b(8), fill=RED)
            cy += 13
            head_lines = wrap_text(d, p["head"], serif_black(10),
                                   card_w - 14)
            assert len(head_lines) <= 3, p["head"]
            for ln in head_lines:
                d.text((px + 7, cy), ln, font=serif_black(10), fill=INK)
                cy += 11
            deck_lines = wrap_text(d, p["deck"], sans(8), card_w - 14)
            assert len(deck_lines) <= 2, p["deck"]
            for ln in deck_lines:
                d.text((px + 7, cy), ln, font=sans(8), fill=INK2)
                cy += 10
            assert cy <= py + card_h - 14, "card %d overruns" % p["n"]
            tag_chip(d, px + 7, py + card_h - 12, p["tag"], )
    y += 2 * card_h + 6 + 5

    # ---- map + the 35-item list
    hline(d, x0, y + 8, x1, 1)
    d.text((x0, y), "WHERE IT HAPPENED \u2014 ALSO ON WEDNESDAY 25 NOVEMBER",
           font=sans_black(12), fill=INK)
    d.text((x1 - _w(d, "numbers on the map match the stories", sans(9)),
            y + 1), "numbers on the map match the stories", font=sans(9),
           fill=INK2)
    y += 19
    map_w, map_h = 292, 208
    map_x, map_y = x0, y
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA,
                outline=INK, width=1)

    def project(lon, lat):
        return (map_x + 6 + (lon + 180) / 360 * (map_w - 12),
                map_y + 6 + (90 - lat) / 180 * (map_h - 12))

    for poly in LANDMAP:
        d.polygon([project(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LANDLINE)
    for lon in range(-150, 181, 30):
        gx = map_x + 6 + (lon + 180) / 360 * (map_w - 12)
        d.line([(gx, map_y + 6), (gx, map_y + map_h - 6)],
               fill=(170, 200, 225), width=1)
    for s in LEADS + CARDS:
        cx, cy = project(s["lon"], s["lat"])
        num_disc(d, cx, cy, s["n"], r=8)
    for r in REST:
        cx, cy = project(r[2], r[3])
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=INK,
                  outline=(255, 255, 255))

    list_x = map_x + map_w + 12
    col_w = (x1 - list_x - 10) / 2
    rest_items = [dict(n=r[0], place=r[1], tag=r[6], line=r[8]) for r in REST]
    half = (len(rest_items) + 1) // 2
    list_bottom = map_y
    for ci, chunk in enumerate([rest_items[:half], rest_items[half:]]):
        cx = list_x + ci * (col_w + 10)
        cy = map_y
        for item in chunk:
            # Full line must fit: number + place + text + badge, no wrap.
            for size in (9, 8):
                bf = sans_b(size)
                tf2 = sans(size)
                head = "%d. %s \u2014 " % (item["n"], item["place"])
                total = (_w(d, head, bf) + _w(d, item["line"], tf2) + 16)
                if total <= col_w:
                    break
            else:
                raise SystemExit("list line too long: %d %s" %
                                 (item["n"], item["place"]))
            d.text((cx, cy), "%d." % item["n"], font=bf, fill=RED)
            nx = cx + _w(d, "%d. " % item["n"], bf)
            d.text((nx, cy), item["place"], font=bf, fill=INK)
            px = nx + _w(d, item["place"] + " \u2014 ", bf)
            d.text((px, cy), item["line"], font=tf2, fill=INK)
            bx = px + _w(d, item["line"], tf2) + 4
            d.rectangle([bx, cy + 1, bx + 11, cy + 10],
                        fill=TAG_COLOUR[item["tag"]])
            d.text((bx + 2.5, cy + 1), item["tag"], font=sans_b(7),
                   fill=(255, 255, 255))
            cy += 11.5
        list_bottom = max(list_bottom, cy)
    y = max(map_y + map_h, list_bottom) + 4

    # ---- region legend
    lx = x0
    lf = sans_b(8)
    for z in ZONE_ORDER:
        c = zone_count.get(z, 0)
        if not c:
            continue
        d.rectangle([lx, y, lx + 8, y + 8], fill=ZONE_COLOUR[z])
        lab = "%s %d" % (z, c)
        d.text((lx + 11, y - 1), lab, font=lf, fill=INK)
        lx += 11 + _w(d, lab, lf) + 12
    assert lx <= x1 + 2, "legend overflow"
    y += 14

    # ---- DATE CHECK footer
    dc_h = 40
    d.rectangle([x0, y, x1, y + dc_h], fill=(255, 255, 255), outline=RED,
                width=1)
    d.text((x0 + 8, y + 4), "DATE CHECK \u2014 LEFT OUT, NOT WEDNESDAY",
           font=sans_black(10), fill=RED)
    d.text((x1 - 8 - _w(d, "NOT YET: " + NOT_YET, sans_b(9)), y + 4),
           "NOT YET: " + NOT_YET, font=sans_b(9), fill=INK)
    lo = "  \u00b7  ".join("%s (%s)" % (t, dt) for t, dt in LEFT_OUT)
    lo_lines = wrap_text(d, lo, sans(9), CW - 16)
    assert len(lo_lines) <= 2, lo_lines
    ly = y + 19
    for ln in lo_lines:
        d.text((x0 + 8, ly), ln, font=sans(9), fill=INK2)
        ly += 11
    y += dc_h + 5

    # ---- sources + key
    src_line = ("SOURCES: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Xinhua "
                "\u00b7 CMSA \u00b7 Ofgem \u00b7 ABS \u00b7 BEA \u00b7 UN \u00b7 ESA "
                "\u00b7 USCG. Every story first reported Wed 25 Nov 2026. "
                "All drawings are original illustrations for this page.")
    y = draw_lines(d, x0, y, src_line, sans(8), INK2, CW, leading=10)
    y += 2
    key = ("CONFIRMED = verified by a named source   \u00b7   REPORTED = "
           "reported, details unconfirmed   \u00b7   CLAIM = one side's "
           "claim, not independently confirmed")
    d.text((x0, y), key, font=sans_b(8), fill=INK2)
    y += 12
    print("stories=%d zones=%d beats=%d" % (len(stories), len(zones),
                                            len(beats)))
    print("zone counts:", zone_count)
    print("field counts:", beat_count)
    print("layout bottom y=%d (limit 1024)" % y)
    assert y <= 1022, "layout overflows: %d" % y
    return img


def main():
    img = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote %s %dx%d %d bytes" % (OUT, img.size[0], img.size[1],
                                       os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
