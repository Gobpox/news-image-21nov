#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: Saturday 21 November 2026 in one picture.

A newspaper front page rendered entirely with Pillow. Three large hero
scenes, twelve cards and twenty-five one-line briefs, all driven by the
single STORIES data table below: the tally strap, the region bar and the
field bar are computed from that same table, so no count on the page can
disagree with another. Deterministic: no randomness anywhere, so two
runs produce byte-identical PNGs.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = Path(__file__).resolve().parent / "fonts"

PAPER = (244, 239, 227)
PAPER_DK = (233, 225, 206)
INK = (26, 24, 20)
MUTE = (96, 90, 78)
RED = (178, 34, 30)
NAVY = (18, 32, 54)
TEAL = (23, 92, 96)
GOLD = (196, 148, 38)
GREEN = (38, 110, 62)
PURPLE = (120, 70, 160)
SKY = (168, 198, 224)
SAND = (226, 205, 165)

REGIONS = {"EUR": ("Europe", (52, 84, 140)), "ASI": ("Asia-Pacific", RED),
           "AME": ("Americas", TEAL), "MEA": ("Middle East", PURPLE),
           "AFR": ("Africa", GOLD), "GLO": ("Global", MUTE)}

# ------------------------------------------------------------------ data
# (place, region, field, headline, deck, source, sure)  sure: C=confirmed,
# O=official, W=witnesses, R=reported, S=scheduled, G=ongoing
HEROES = [
    ("RIYADH, SAUDI ARABIA", "MEA", "Conflict",
     "Riyadh shoots down three Houthi missiles",
     "All three ballistic missiles destroyed Saturday — the second "
     "attack on the capital in days.",
     "Reuters", "C", "3", "MISSILES INTERCEPTED"),
    ("ANTALYA, TURKIYE", "ASI", "Climate",
     "COP31 deadlocked: third draft missing",
     "EU: no deal beats a bad deal. Fossil-fuel words stay out as "
     "the talks run into overtime.",
     "BBC / UN", "G", "3rd", "DRAFT STILL MISSING"),
    ("JUNIN, PERU", "AME", "Disaster",
     "Magnitude 6.7 quake shakes Peru's Andes",
     "00:09 UTC, 108 km deep near Carhuamayo (USGS). Felt in Lima; "
     "no deaths confirmed.",
     "USGS / IGP", "C", "6.7", "MAGNITUDE, 108 KM DEEP"),
]

CARDS = [
    ("WARSAW", "EUR", "Diplomacy", "NATO will defend 'every inch' of Poland",
     "Rutte in Warsaw after two missiles and a drone fell on Poland; "
     "council meets Monday.", "Reuters", "C"),
    ("COPENHAGEN", "EUR", "Politics",
     "Denmark expels Russia's defence attache",
     "A foiled assassination plot is blamed on Russian intelligence; "
     "EU curbs proposed.", "Reuters", "C"),
    ("GULF OF FINLAND", "EUR", "Conflict",
     "Russian cargo ship hit by drone, ablaze",
     "The Kaliningrad-bound ship drifts into Finnish waters; Finland "
     "leads the response.", "BBC", "R"),
    ("GAZA", "MEA", "Conflict", "Strike kills three in aid vehicle",
     "Witnesses say an Israeli strike hit a vehicle that was "
     "distributing aid in Gaza.", "Reuters", "W"),
    ("BASRA, IRAQ", "ASI", "Disaster", "Power-station fire kills at least four",
     "At least four dead and 35 injured in a fire at a power station "
     "in Iraq's Basra.", "Reuters", "R"),
    ("KHASAB, OMAN", "MEA", "Conflict", "Two tankers hit off Oman",
     "Unknown projectiles hit two tankers north of Khasab after they "
     "left the Strait of Hormuz.", "UKMTO", "R"),
    ("GENEVA", "GLO", "Diplomacy", "Killer-robot talks: no firm pledge",
     "128 states agree only to more talks on lethal autonomous "
     "weapons, with no commitment.", "Reuters", "C"),
    ("WASHINGTON", "AME", "Crime", "FBI probes reported crime-database hack",
     "An apparent breach of the NCIC database police use for warrants "
     "and background checks.", "BBC", "R"),
    ("GUASAVE, MEXICO", "AME", "Crime", "FBI top-ten drug lord held",
     "'Chapo Isidro' Meza Flores was arrested after a shoot-out with "
     "Mexican special forces.", "BBC", "C"),
    ("LOS ANGELES", "AME", "Courts", "Man convicted of starting Palisades fire",
     "A jury finds Rinderknecht started the blaze that killed 12 and "
     "destroyed 6,800+ buildings.", "BBC", "C"),
    ("MERCURY", "GLO", "Science", "BepiColombo reaches for Mercury orbit",
     "The ESA-JAXA burn is set for 18:24 UTC after eight years; the "
     "result is due tonight.", "ESA", "S"),
    ("TURIN", "EUR", "Sport", "Zverev and Alcaraz set up the ATP final",
     "Zverev beat Medvedev 7-6(0) 6-4; Alcaraz beat Shelton in three "
     "sets in the semi-finals.", "ATP", "C"),
]

BRIEFS = [
    ("KYIV", "EUR", "Conflict", "Bridge strikes 'fair response' to 109 attacks", "BBC"),
    ("KYIV", "EUR", "Politics", "Zelensky: Putin a 'killer'; Trump called him friend", "BBC"),
    ("TEHRAN", "MEA", "Diplomacy", "Qatari delegation in Tehran for talks", "Reuters"),
    ("THE GULF", "MEA", "Conflict", "US denies an F-16 was damaged by a missile", "Reuters"),
    ("SAVAR", "ASI", "Labour", "80+ garment factories shut in wage sit-ins", "TOI"),
    ("INDIA", "ASI", "Disaster", "Illicit alcohol kills 11; 180+ in hospital", "IOL"),
    ("BANGLADESH", "ASI", "Politics", "97 Border Guard platoons deployed", "The Hindu"),
    ("DHAKA", "ASI", "Courts", "Bangladesh vows reparation claim vs Myanmar", "Sun"),
    ("BEIJING", "ASI", "Diplomacy", "China: Japan must change its 'attitude'", "Asharq"),
    ("DHAKA", "ASI", "Diplomacy", "India joins Ganga talks; treaty ends 12 Dec", "TNN"),
    ("SOUTH AFRICA", "AFR", "Politics", "ANC fights to keep its big cities", "BBC"),
    ("KATHMANDU", "ASI", "Politics", "PM Balen Shah's India test begins", "BBC"),
    ("PARIS", "EUR", "Courts", "Officers sentenced in Zecler beating case", "BBC"),
    ("WASHINGTON", "AME", "Politics", "Cyber chief Cairncross removed", "Daily Brief"),
    ("LOS ANGELES", "AME", "Labour", "Port strike possible Sunday 17:00", "Daily Brief"),
    ("LAS VEGAS", "AME", "Sport", "Verstappen pole; Antonelli penalised", "GP247"),
    ("TWICKENHAM", "EUR", "Sport", "England's record rugby win over NZ", "BBC"),
    ("FOOTBALL", "EUR", "Sport", "Newcastle 2-2 Arsenal; Leeds win at Chelsea", "BBC"),
    ("OBIHIRO", "ASI", "Sport", "Daleman wins 500 m in 37.45 seconds", "Pollar"),
    ("OSLO", "EUR", "Society", "Trafalgar tree: 21 m, 75 years old, felled", "BBC"),
    ("CORNWALL", "EUR", "Culture", "Spitting Image co-creator Fluck dies, 85", "BBC"),
    ("JUPITER", "GLO", "Science", "Europa's sodium cloud traced to its ocean", "GenFlow"),
    ("ROMANIA", "EUR", "Weather", "Blizzard warning: gusts 80-100 km/h", "ANM"),
    ("DHAKA", "ASI", "Sport", "Mushfiqur out of 2nd Test v South Africa", "EIN"),
    ("LONDON", "EUR", "Culture", "Catherine on cancer, in 'Heal' documentary", "BBC"),
]

SURE_LABEL = {"C": "CONFIRMED", "O": "OFFICIAL", "W": "WITNESSES",
              "R": "REPORTED", "S": "SCHEDULED", "G": "ONGOING"}

TIMELINE = [("00:09", "Peru quake"), ("05:12", "M5.0 again"),
            ("10:00", "Romania alert"), ("13:15", "'Chapo Isidro' held"),
            ("18:22", "Ship ablaze"), ("18:24", "Bepi burn"),
            ("19:33", "COP31 stuck")]

NUMBERS = [("6.7", "Peru magnitude (USGS)"), ("3", "missiles over Riyadh"),
           ("128", "states at robot talks"), ("97", "platoons in Bangladesh"),
           ("35", "hurt in Basra fire"), ("12", "killed in Palisades fire")]


def all_stories():
    out = []
    for h in HEROES:
        out.append((h[1], h[2]))
    for c in CARDS:
        out.append((c[1], c[2]))
    for b in BRIEFS:
        out.append((b[1], b[2]))
    return out


# ------------------------------------------------------------------ fonts
def _f(name, sz):
    return ImageFont.truetype(str(FONT_DIR / name), sz)


def SERIF(sz):
    return _f("PlayfairDisplay-Bold.ttf", sz)


def SERIF_BLACK(sz):
    return _f("PlayfairDisplay-Black.ttf", sz)


def SERIF_I(sz):
    return _f("PlayfairDisplay-SemiBoldItalic.ttf", sz)


def SANS(sz):
    return _f("Archivo-Regular.ttf", sz)


def SANS_B(sz):
    return _f("Archivo-Bold.ttf", sz)


def SANS_SB(sz):
    return _f("Archivo-SemiBold.ttf", sz)


def fit_font(text, maxw, maker, hi, lo):
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    for sz in range(hi, lo - 1, -1):
        f = maker(sz)
        if probe.textlength(text, font=f) <= maxw:
            return f
    return maker(lo)


OVERFLOWS = []


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, maxw, leading, max_lines=None, tag=""):
    lines = wrap(d, text, font, maxw)
    if max_lines and len(lines) > max_lines:
        OVERFLOWS.append(f"{tag}: {len(lines)}>{max_lines} lines: {text[:40]}")
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def center(d, y, text, font, fill, cx=W // 2):
    d.text((cx - d.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


# ------------------------------------------------------------------ flags
def flag(d, code, x, y, w=34, h=22):
    """Small recognisable national flags: real patterns and colours."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    if code == "SA":  # green, white script line and sword line
        d.rectangle([x, y, x + w, y + h], fill=(0, 108, 53))
        d.line([x + 5, y + 8, x + w - 5, y + 8], fill=(255, 255, 255), width=3)
        d.line([x + 5, y + 15, x + w - 9, y + 15], fill=(255, 255, 255), width=2)
    elif code == "TR":
        d.rectangle([x, y, x + w, y + h], fill=(227, 10, 23))
        d.ellipse([x + 7, y + 4, x + 21, y + 18], fill=(255, 255, 255))
        d.ellipse([x + 10, y + 5, x + 23, y + 17], fill=(227, 10, 23))
        d.polygon([(x + 24, y + 8), (x + 26, y + 11), (x + 24, y + 14),
                   (x + 28, y + 11)], fill=(255, 255, 255))
    elif code == "PE":
        d.rectangle([x, y, x + w // 3, y + h], fill=(217, 0, 27))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(217, 0, 27))
    elif code == "PL":
        d.rectangle([x, y + h // 2, x + w, y + h], fill=(220, 20, 60))
    elif code == "DK":
        d.rectangle([x, y, x + w, y + h], fill=(198, 12, 48))
        d.rectangle([x + 9, y, x + 13, y + h], fill=(255, 255, 255))
        d.rectangle([x, y + 9, x + w, y + 13], fill=(255, 255, 255))
    elif code == "FI":
        d.rectangle([x + 9, y, x + 14, y + h], fill=(0, 47, 108))
        d.rectangle([x, y + 8, x + w, y + 14], fill=(0, 47, 108))
    elif code == "PS":
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 0, 0))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(0, 122, 61))
        d.polygon([(x, y), (x + 11, y + h // 2), (x, y + h)], fill=(238, 28, 37))
    elif code == "IQ":
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 0, 0))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(206, 17, 38))
        d.rectangle([x + 13, y + 9, x + 21, y + 13], fill=(0, 122, 61))
    elif code == "OM":
        d.rectangle([x, y, x + 10, y + h], fill=(239, 51, 64))
        d.rectangle([x + 10, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 150, 57))
        d.rectangle([x + 10, y + 2 * h // 3, x + w, y + h], fill=(0, 0, 0))
    elif code == "CH":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        d.rectangle([x + 14, y + 4, x + 20, y + 18], fill=(255, 0, 0))
        d.rectangle([x + 9, y + 8, x + 25, y + 14], fill=(255, 0, 0))
    elif code == "US":
        for i in range(5):
            d.rectangle([x, y + i * 5, x + w, y + i * 5 + 2], fill=(179, 25, 66))
        d.rectangle([x, y, x + 15, y + 11], fill=(10, 49, 97))
    elif code == "MX":
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 104, 71))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(206, 17, 38))
        d.ellipse([x + 14, y + 8, x + 20, y + 14], fill=(196, 148, 38))
    elif code == "IT":
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 140, 69))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(205, 33, 42))
    elif code == "JP":
        d.ellipse([x + 12, y + 5, x + 22, y + 17], fill=(188, 0, 45))
    elif code == "EU":
        d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
        for i in range(6):
            xx = x + 6 + (i % 3) * 10
            yy = y + 4 + (i // 3) * 11
            d.ellipse([xx, yy, xx + 3, yy + 3], fill=(255, 204, 0))
    elif code == "UA":
        d.rectangle([x, y + h // 2, x + w, y + h], fill=(255, 215, 0))
        d.rectangle([x, y, x + w, y + h // 2], fill=(0, 91, 187))
    elif code == "GB":
        d.rectangle([x, y, x + w, y + h], fill=(0, 36, 125))
        d.rectangle([x + 14, y, x + 20, y + h], fill=(255, 255, 255))
        d.rectangle([x, y + 8, x + w, y + 14], fill=(255, 255, 255))
        d.rectangle([x + 15, y, x + 19, y + h], fill=(200, 16, 46))
        d.rectangle([x, y + 9, x + w, y + 13], fill=(200, 16, 46))
    elif code == "BD":
        d.rectangle([x, y, x + w, y + h], fill=(0, 106, 78))
        d.ellipse([x + 11, y + 4, x + 25, y + 18], fill=(244, 42, 65))
    elif code == "CN":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        d.polygon([(x + 5, y + 4), (x + 7, y + 9), (x + 3, y + 9)], fill=(255, 222, 0))
    elif code == "IN":
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(255, 255, 255))
        d.rectangle([x, y, x + w, y + h // 3], fill=(247, 147, 29))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(4, 106, 56))
    elif code == "ZA":
        d.rectangle([x, y, x + w, y + h // 2], fill=(222, 56, 49))
        d.rectangle([x, y + h // 2, x + w, y + h], fill=(0, 20, 137))
        d.polygon([(x, y), (x + 13, y + h // 2), (x, y + h)], fill=(0, 119, 73))
    elif code == "NP":
        d.polygon([(x, y), (x + 16, y + 11), (x, y + 11)], outline=(0, 56, 147))
        d.polygon([(x, y + 11), (x + 16, y + 22), (x, y + 22)], outline=(0, 56, 147))
        d.ellipse([x + 3, y + 14, x + 8, y + 19], fill=(220, 20, 60))
    elif code == "FR":
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 85, 164))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(239, 65, 53))
    elif code == "RO":
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 43, 127))
        d.rectangle([x + w // 3, y, x + 2 * w // 3, y + h], fill=(252, 209, 22))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(206, 17, 38))
    elif code == "NO":
        d.rectangle([x, y, x + w, y + h], fill=(186, 12, 47))
        d.rectangle([x + 9, y, x + 14, y + h], fill=(255, 255, 255))
        d.rectangle([x, y + 8, x + w, y + 14], fill=(255, 255, 255))
        d.rectangle([x + 10, y, x + 13, y + h], fill=(0, 32, 91))
        d.rectangle([x, y + 9, x + w, y + 13], fill=(0, 32, 91))
    else:  # generic globe disc
        d.ellipse([x + 6, y + 1, x + 28, y + 21], fill=SKY, outline=INK)


# ------------------------------------------------------------------ scenes
def scene_riyadh(d, x, y, w, h):
    """Night skyline, intercept bursts and missile trails over Riyadh."""
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((16, 24, 52)[i] + ((70, 60, 90)[i] - (16, 24, 52)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    for sx, sy in ((30, 18), (90, 10), (180, 22), (250, 12), (140, 30)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 230))
    # Kingdom Centre style tower with its arch, plus blocks
    d.rectangle([x + 130, y + 52, x + 168, y + h], fill=(30, 34, 58))
    d.polygon([(x + 138, y + 66), (x + 160, y + 66), (x + 149, y + 92)],
              fill=(16, 24, 52))
    for bx, bw, bh in ((18, 34, 46), (58, 26, 32), (180, 40, 40), (228, 30, 56),
                       (264, 36, 30)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(24, 28, 48))
        for wy in range(y + h - bh + 6, y + h - 4, 9):
            for wx in range(x + bx + 4, x + bx + bw - 4, 8):
                d.rectangle([wx, wy, wx + 3, wy + 3], fill=(250, 205, 90))
    # three incoming trails and three bursts
    for i, (tx, ty) in enumerate(((60, 26), (150, 14), (238, 30))):
        d.line([x + tx + 46, y + ty - 12, x + tx, y + ty + 16],
               fill=(255, 120, 90), width=3)
        cx, cy = x + tx, y + ty + 18
        for dx, dy in ((-12, -8), (0, -13), (12, -8), (-13, 5), (13, 5), (0, 13)):
            d.line([cx, cy, cx + dx, cy + dy], fill=(255, 214, 90), width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 240, 180))
    d.rectangle([x + 8, y + h - 20, x + 118, y + h - 4], fill=(10, 14, 30))
    d.text((x + 13, y + h - 17), "RIYADH — NIGHT SKY", font=SANS_B(11),
           fill=(255, 255, 255))


def scene_antalya(d, x, y, w, h):
    """A deadlocked conference hall: long table, two blocs, an empty lectern."""
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((214, 224, 214)[i] + ((168, 186, 176)[i] - (214, 224, 214)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    d.rectangle([x + 96, y + 8, x + w - 96, y + 32], fill=(240, 238, 228),
                outline=INK, width=2)
    center(d, y + 13, "COP31 — FINAL TEXT?", SERIF(17), RED, cx=x + w // 2)
    # long table
    d.rectangle([x + 34, y + 62, x + w - 34, y + 80], fill=(96, 70, 44))
    d.rectangle([x + 34, y + 80, x + w - 34, y + 86], fill=(70, 50, 30))
    # delegates: left bloc teal, right bloc red, heads down over papers
    for i in range(5):
        xx = x + 52 + i * 26
        d.ellipse([xx, y + 40, xx + 16, y + 56], fill=(222, 184, 150))
        d.rectangle([xx - 2, y + 56, xx + 18, y + 64], fill=TEAL)
        d.rectangle([xx + 1, y + 80, xx + 15, y + 86], fill=(255, 255, 255))
    for i in range(5):
        xx = x + w - 68 - i * 26
        d.ellipse([xx, y + 40, xx + 16, y + 56], fill=(222, 184, 150))
        d.rectangle([xx - 2, y + 56, xx + 18, y + 64], fill=RED)
        d.rectangle([xx + 1, y + 80, xx + 15, y + 86], fill=(255, 255, 255))
    # empty lectern centre; a clock in the top-right corner, past the deadline
    d.rectangle([x + w // 2 - 10, y + 46, x + w // 2 + 10, y + 80], fill=NAVY)
    d.ellipse([x + w - 38, y + 6, x + w - 12, y + 32],
              fill=(255, 255, 255), outline=INK, width=2)
    d.line([x + w - 25, y + 19, x + w - 25, y + 10], fill=RED, width=3)
    d.line([x + w - 25, y + 19, x + w - 17, y + 23], fill=RED, width=3)
    d.rectangle([x + 8, y + h - 20, x + 128, y + h - 4], fill=(30, 50, 40))
    d.text((x + 13, y + h - 17), "ANTALYA — TALKS HALL", font=SANS_B(11),
           fill=(255, 255, 255))


def scene_peru(d, x, y, w, h):
    """Andes ridges, a cracked road and seismic rings from the epicentre."""
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((196, 214, 228)[i] + ((226, 205, 165)[i] - (196, 214, 228)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    d.polygon([(x, y + 58), (x + 70, y + 20), (x + 130, y + 58)], fill=(110, 96, 84))
    d.polygon([(x + 52, y + 34), (x + 70, y + 20), (x + 88, y + 34)], fill=(255, 255, 255))
    d.polygon([(x + 90, y + 62), (x + 180, y + 12), (x + 268, y + 62)], fill=(88, 76, 66))
    d.polygon([(x + 158, y + 28), (x + 180, y + 12), (x + 202, y + 28)], fill=(255, 255, 255))
    d.polygon([(x + 190, y + 66), (x + 262, y + 30), (x + w, y + 66)], fill=(120, 104, 88))
    # houses on the slope
    for hx, hy in ((36, 66), (86, 72), (226, 68)):
        d.rectangle([x + hx, y + hy, x + hx + 24, y + hy + 15], fill=(240, 234, 220))
        d.polygon([(x + hx - 3, y + hy), (x + hx + 12, y + hy - 9),
                   (x + hx + 27, y + hy)], fill=RED)
    # seismic rings from epicentre
    ex, ey = x + 150, y + 88
    for r in (12, 22, 32):
        d.ellipse([ex - r, ey - r // 2, ex + r, ey + r // 2], outline=RED, width=3)
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=RED)
    # cracked road
    d.polygon([(x + 10, y + h), (x + 120, y + 84), (x + 180, y + 84),
               (x + w - 10, y + h)], fill=(90, 86, 80))
    d.line([x + 132, y + 88, x + 148, y + 94, x + 142, y + 100],
           fill=(30, 28, 26), width=3)
    d.rectangle([x + 8, y + 6, x + 150, y + 22], fill=(120, 30, 28))
    d.text((x + 13, y + 9), "JUNIN — THE ANDES", font=SANS_B(11),
           fill=(255, 255, 255))


HERO_SCENES = [scene_riyadh, scene_antalya, scene_peru]
HERO_FLAGS = ["SA", "TR", "PE"]
CARD_FLAGS = ["PL", "DK", "FI", "PS", "IQ", "OM", "CH", "US", "MX", "US",
              "EU", "IT"]


def badge(d, x, y, num, region):
    col = REGIONS[region][1]
    d.rectangle([x, y, x + 24, y + 24], fill=col)
    t = str(num)
    f = SANS_B(14 if len(t) < 2 else 12)
    d.text((x + 12 - d.textlength(t, font=f) / 2, y + 4), t, font=f,
           fill=(255, 255, 255))


def tally_bar(d, y, counts, total, x0=16, x1=W - 16, hgt=15):
    x = x0
    for code in ("EUR", "ASI", "AME", "MEA", "GLO", "AFR"):
        n = counts.get(code, 0)
        if not n:
            continue
        wseg = (x1 - x0) * n / total
        d.rectangle([x, y, x + wseg, y + hgt], fill=REGIONS[code][1])
        lab = f"{REGIONS[code][0]} {n}"
        if d.textlength(lab, font=SANS_B(10)) <= wseg - 8:
            d.text((x + 5, y + 1), lab, font=SANS_B(10), fill=(255, 255, 255))
        x += wseg
    return y + hgt


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    stories = all_stories()
    total = len(stories)
    reg_counts = {}
    field_counts = {}
    for r, f in stories:
        reg_counts[r] = reg_counts.get(r, 0) + 1
        field_counts[f] = field_counts.get(f, 0) + 1

    # ---------------------------------------------------------- masthead
    d.rectangle([0, 0, W, 58], fill=INK)
    center(d, 5, "THE WORLD IN ONE PICTURE", SERIF_BLACK(29), PAPER)
    center(d, 38, "SATURDAY 21 NOVEMBER 2026  -  EVERY STORY DATED TO THE DAY",
           SANS_B(12), (250, 205, 90))
    # strap: honest counts, computed from the data table
    strap = (f"{total} STORIES: 3 HEROES + 12 CARDS + 25 BRIEFS  -  "
             f"{len(reg_counts)} REGIONS  -  {len(field_counts)} FIELDS")
    d.rectangle([0, 58, W, 80], fill=RED)
    center(d, 62, strap, SANS_B(13), (255, 255, 255))
    # timeline: one line, UTC times only where a source gives one
    tl = "SATURDAY IN UTC:  " + "  ·  ".join(f"{t} {l}" for t, l in TIMELINE)
    d.text((16, 84), tl, font=SANS_B(10), fill=INK)
    d.line([16, 104, W - 16, 104], fill=INK, width=2)

    # ---------------------------------------------------------- heroes
    hy, hh = 110, 274
    hw = (W - 32 - 16) // 3
    for i, hero in enumerate(HEROES):
        x = 16 + i * (hw + 8)
        place, region, field, head, deck, src, sure, big, biglab = hero
        d.rectangle([x, hy, x + hw, hy + hh], fill=(255, 253, 246), outline=INK, width=2)
        HERO_SCENES[i](d, x + 3, hy + 3, hw - 6, 96)
        yy = hy + 102
        badge(d, x + 8, yy, i + 1, region)
        flag(d, HERO_FLAGS[i], x + 40, yy + 1)
        d.text((x + 82, yy + 2), place, font=SANS_B(12), fill=REGIONS[region][1])
        d.text((x + 82, yy + 15), f"{field.upper()} - {src} - {SURE_LABEL[sure]}",
               font=SANS(10), fill=MUTE)
        yy += 26
        yy = text_block(d, x + 8, yy, head, SERIF(30), INK, hw - 16, 32,
                        max_lines=2, tag=f"hero{i}")
        text_block(d, x + 8, yy, deck, SANS(13), (52, 48, 42), hw - 16, 16,
                   max_lines=2, tag=f"herodeck{i}")
        # big stat, its own labelled space, never mixed into the headline
        d.rectangle([x + 8, hy + hh - 46, x + hw - 8, hy + hh - 6], fill=PAPER_DK)
        d.text((x + 14, hy + hh - 44), big, font=SERIF_BLACK(29), fill=RED)
        d.text((x + 14 + d.textlength(big, font=SERIF_BLACK(29)) + 10, hy + hh - 33),
               biglab, font=SANS_B(11), fill=INK)

    # ---------------------------------------------------------- cards
    cy = hy + hh + 10
    chh, chw = 74, (W - 32 - 16) // 3
    for i, card in enumerate(CARDS):
        place, region, field, head, deck, src, sure = card
        x = 16 + (i % 3) * (chw + 8)
        yy0 = cy + (i // 3) * (chh + 6)
        d.rectangle([x, yy0, x + chw, yy0 + chh], fill=(255, 253, 246),
                    outline=(150, 142, 126), width=1)
        badge(d, x + 6, yy0 + 5, i + 4, region)
        flag(d, CARD_FLAGS[i], x + 36, yy0 + 6, w=28, h=18)
        d.text((x + 70, yy0 + 5), place, font=SANS_B(11), fill=REGIONS[region][1])
        d.text((x + 70, yy0 + 17), f"{field.upper()} - {src} - {SURE_LABEL[sure]}",
               font=SANS(9), fill=MUTE)
        text_block(d, x + 6, yy0 + 29, head, SERIF(19), INK, chw - 12, 21,
                   max_lines=2, tag=f"card{i}")
    by = cy + 4 * (chh + 6) - 6 + 8

    # ---------------------------------------------------------- briefs
    d.rectangle([16, by, W - 16, by + 20], fill=NAVY)
    d.text((22, by + 4), "THE REST OF SATURDAY — 25 BRIEFS IN ONE LINE EACH",
           font=SANS_B(12), fill=(255, 255, 255))
    d.text((W - 216, by + 5), "SOURCES NAMED IN EVERY BRIEF",
           font=SANS_B(10), fill=(200, 205, 220))
    by += 24
    colw = (W - 32 - 12) // 2
    for i, (place, region, field, line, src) in enumerate(BRIEFS):
        col = i % 2
        row = i // 2
        x = 16 + col * (colw + 12)
        yy = by + row * 14
        d.rectangle([x, yy + 3, x + 9, yy + 12], fill=REGIONS[region][1])
        txt = f"{place} — {line} ({src})"
        f = fit_font(txt, colw - 14, SANS_SB, 14, 11)
        if f.size < 14:
            OVERFLOWS.append(f"brief{i} shrunk to {f.size}: {txt[:40]}")
        d.text((x + 14, yy), txt, font=f, fill=INK)
    by += 13 * 14 + 4

    # ------------------------------------------------- numbers + bars
    d.line([16, by, W - 16, by], fill=INK, width=2)
    d.text((16, by + 5), "THE DAY IN NUMBERS", font=SANS_B(12), fill=RED)
    nx = 172
    for num, lab in NUMBERS:
        d.text((nx, by + 3), num, font=SERIF_BLACK(20), fill=INK)
        d.text((nx, by + 25), lab, font=SANS(9), fill=MUTE)
        nx += 141
    by += 36
    d.text((16, by + 1), "REGIONS", font=SANS_B(10), fill=MUTE)
    tally_bar(d, by, reg_counts, total, x0=76, x1=560, hgt=13)
    d.text((576, by + 1), "FIELDS", font=SANS_B(10), fill=MUTE)
    top_fields = sorted(field_counts.items(), key=lambda kv: -kv[1])[:5]
    fx = 632
    for name, n in top_fields:
        d.text((fx, by + 1), f"{name} {n}", font=SANS_B(10), fill=INK)
        fx += d.textlength(f"{name} {n}", font=SANS_B(10)) + 10
    by += 17

    # ------------------------------------------------- date check + not yet
    dc = ("DATE CHECK — NOT 21 NOV, LEFT OUT: Thu 19 — Shenzhen summit, ICJ Myanmar "
          "ruling, Anthropic debut · Fri 20 — Kyiv blitz, Nasdaq -5.3% close, Bayer "
          "$7.25bn approval, Rikers plan · Sun 22 agenda is not Saturday's news.")
    yy = text_block(d, 16, by, dc, SANS_SB(11), (70, 64, 54), W - 32, 13,
                    max_lines=2, tag="datecheck")
    ny = ("NOT YET KNOWN SATURDAY NIGHT: BepiColombo's burn result · a final COP31 "
          "text · Peru's full damage toll. Sources are named per story.")
    text_block(d, 16, yy, ny, SANS_SB(11), RED, W - 32, 13,
               max_lines=1, tag="notyet")

    if OVERFLOWS:
        print("OVERFLOWS:", *OVERFLOWS, sep="\n  ")
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes; stories:", total,
          "; regions:", reg_counts, "; fields:", field_counts)


if __name__ == "__main__":
    main()
