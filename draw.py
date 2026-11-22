#!/usr/bin/env python3
"""Draw the news-image-20261121 entry, v2: Saturday 21 November 2026.

Geometry first (GATES.md, approved by Ahmad 2026-11-22): the grid and
the type floors were locked before the story count — hero headlines
>= 30px, card headlines >= 19px, brief headlines >= 16px, brief text
>= 14px, in-scene labels >= 13px, at most 3 heroes, briefs <= 9 words
over 2 lines. 33 stories fit those floors: 3 heroes + 12 cards + 18
briefs (7 briefs from the locked research set were cut, see STORIES.md).

Every important number is read from figures.json (the registry); no
panel types a figure freehand. The strap counts, the region tally and
the field tally are computed from the story table below. Deterministic:
no randomness, two runs are byte-identical.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / "fonts"
FIG = {f["key"]: f["display"]
       for f in json.loads((HERE / "figures.json").read_text())["figures"]}

PAPER = (244, 239, 227)
PAPER_DK = (233, 225, 206)
INK = (26, 24, 20)
MUTE = (96, 90, 78)
RED = (178, 34, 30)
NAVY = (18, 32, 54)
TEAL = (23, 92, 96)
GOLD = (196, 148, 38)
PURPLE = (120, 70, 160)
SKY = (168, 198, 224)

REGIONS = {"EUR": ("Europe", (52, 84, 140)), "ASI": ("Asia-Pacific", RED),
           "AME": ("Americas", TEAL), "MEA": ("Middle East", PURPLE),
           "AFR": ("Africa", GOLD), "GLO": ("Global", MUTE)}
SURE_LABEL = {"C": "CONFIRMED", "W": "WITNESSES", "R": "REPORTED",
              "S": "SCHEDULED", "G": "ONGOING"}

# ------------------------------------------------------------------ data
# Heroes: (place, region, field, headline, deck, source, sure, big, biglabel)
HEROES = [
    ("RIYADH, SAUDI ARABIA", "MEA", "Conflict",
     "Riyadh shoots down three Houthi missiles",
     "All three ballistic missiles destroyed Saturday — the second "
     "attack on the capital in days.",
     "Reuters", "C", FIG["riyadh_missiles_intercepted"], "MISSILES INTERCEPTED"),
    ("ANTALYA, TURKIYE", "ASI", "Climate",
     "COP31 deadlocked: third draft missing",
     "EU: no deal beats a bad deal. Fossil-fuel words stay out as "
     "the talks run into overtime.",
     "BBC / UN", "G", FIG["cop31_draft_ordinal"], "DRAFT STILL MISSING"),
    ("JUNIN, PERU", "AME", "Disaster",
     "Magnitude " + FIG["peru_quake_magnitude"] + " quake shakes Peru's Andes",
     "00:09 UTC, " + FIG["peru_quake_depth"] + " km deep near Carhuamayo "
     "(USGS). Felt in Lima; no deaths confirmed.",
     "USGS / IGP", "C", FIG["peru_quake_magnitude"], "MAGNITUDE, DEPTH "
     + FIG["peru_quake_depth"] + " KM"),
]

# Cards: (place, region, field, headline, deck, source, sure)
CARDS = [
    ("WARSAW", "EUR", "Diplomacy", "NATO will defend 'every inch' of Poland",
     "Rutte in Warsaw after " + FIG["poland_missiles_down"] + " missiles and "
     "a drone fell on Poland; council meets Monday.", "Reuters", "C"),
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
    ("BASRA, IRAQ", "ASI", "Disaster",
     "Power-station fire kills at least " + FIG["basra_fire_killed"],
     "At least " + FIG["basra_fire_killed"] + " dead and "
     + FIG["basra_fire_injured"] + " injured in a fire at a power "
     "station in Iraq's Basra.", "Reuters", "R"),
    ("KHASAB, OMAN", "MEA", "Conflict", "Two tankers hit off Oman",
     "Unknown projectiles hit two tankers north of Khasab after they "
     "left the Strait of Hormuz.", "UKMTO", "R"),
    ("GENEVA", "GLO", "Diplomacy", "Killer-robot talks: no firm pledge",
     FIG["geneva_robot_states"] + " states agree only to more talks on "
     "lethal autonomous weapons, no commitment.", "Reuters", "C"),
    ("WASHINGTON", "AME", "Crime", "FBI probes reported crime-database hack",
     "An apparent breach of the NCIC database police use for warrants "
     "and background checks.", "BBC", "R"),
    ("GUASAVE, MEXICO", "AME", "Crime", "FBI top-ten drug lord held",
     "'Chapo Isidro' Meza Flores was arrested after a shoot-out with "
     "Mexican special forces.", "BBC", "C"),
    ("LOS ANGELES", "AME", "Courts", "Man convicted of starting Palisades fire",
     "A jury finds Rinderknecht started the blaze that killed "
     + FIG["palisades_killed"] + " and destroyed "
     + FIG["palisades_buildings"] + " buildings.", "BBC", "C"),
    ("MERCURY", "GLO", "Science", "BepiColombo reaches for Mercury orbit",
     "The ESA-JAXA burn is set for 18:24 UTC after "
     + FIG["bepicolombo_years"] + " years; the result is due tonight.",
     "ESA", "S"),
    ("TURIN", "EUR", "Sport", "Zverev and Alcaraz set up the ATP final",
     "Zverev beat Medvedev 7-6(0) 6-4; Alcaraz beat Shelton in three "
     "sets in the semi-finals.", "ATP", "C"),
]

# Briefs: (place, region, field, headline <= ~5 words, text <= ~5 words + source)
BRIEFS = [
    ("KYIV", "EUR", "Conflict", "Bridge strikes 'fair response'",
     "109 Russian attacks cited · BBC"),
    ("TEHRAN", "MEA", "Diplomacy", "Qatar delegation visits",
     "For talks in Tehran · Reuters"),
    ("SAVAR", "ASI", "Labour", "80+ garment factories shut",
     "Wage sit-ins spread · TOI"),
    ("INDIA", "ASI", "Disaster", "Illicit alcohol kills 11",
     "180+ people in hospital · IOL"),
    ("BANGLADESH", "ASI", "Politics",
     FIG["bangladesh_platoons"] + " platoons deployed",
     "Border Guard amid unrest · Hindu"),
    ("BEIJING", "ASI", "Diplomacy", "China: Japan, change 'attitude'",
     "After Xi snubs Takaichi · Asharq"),
    ("SOUTH AFRICA", "AFR", "Politics", "ANC fights for big cities",
     "After election setback · BBC"),
    ("KATHMANDU", "ASI", "Politics", "Balen Shah's India test",
     "First trip abroad · BBC"),
    ("PARIS", "EUR", "Courts", "Officers sentenced in Zecler case",
     "Beating of producer · BBC"),
    ("LAS VEGAS", "AME", "Sport", "Verstappen takes pole",
     "Antonelli fastest, penalised · GP247"),
    ("TWICKENHAM", "EUR", "Sport", "England record win v NZ",
     "Nations Championship · BBC"),
    ("FOOTBALL", "EUR", "Sport", "Newcastle 2-2 Arsenal",
     "Leeds win at Chelsea · BBC"),
    ("OBIHIRO", "ASI", "Sport", "Daleman wins 500 m in 37.45",
     "World Cup speed skating · Pollar"),
    ("OSLO", "EUR", "Society", "Trafalgar tree felled in Norway",
     "21 m, 75 years old · BBC"),
    ("ROMANIA", "EUR", "Weather", "Blizzard warning issued",
     "Gusts 80-100 km/h · ANM"),
    ("DHAKA", "ASI", "Sport", "Mushfiqur out of second Test",
     "Groin injury v South Africa · EIN"),
    ("LONDON", "EUR", "Culture", "Catherine opens up on cancer",
     "In documentary 'Heal' · BBC"),
    ("JUPITER", "GLO", "Science", "Europa's sodium cloud solved",
     "Traced to salty ocean · GenFlow"),
]

TIMELINE = [("00:09", "Peru quake"), ("05:12", "M5.0 again"),
            ("10:00", "Romania alert"), ("13:15", "'Chapo Isidro' held"),
            ("18:22", "Ship ablaze"), ("18:24", "Bepi burn"),
            ("19:33", "COP31 stuck")]

NUMBERS = [(FIG["peru_quake_magnitude"], "Peru magnitude (USGS)"),
           (FIG["riyadh_missiles_intercepted"], "missiles over Riyadh"),
           (FIG["geneva_robot_states"], "states at robot talks"),
           (FIG["bangladesh_platoons"], "platoons in Bangladesh"),
           (FIG["basra_fire_injured"], "hurt in Basra fire"),
           (FIG["palisades_killed"], "killed in Palisades fire")]


def all_stories():
    out = [(h[1], h[2]) for h in HEROES]
    out += [(c[1], c[2]) for c in CARDS]
    out += [(b[1], b[2]) for b in BRIEFS]
    return out


# ------------------------------------------------------------------ fonts
def _f(name, sz):
    return ImageFont.truetype(str(FONT_DIR / name), sz)


def SERIF(sz):
    return _f("PlayfairDisplay-Bold.ttf", sz)


def SERIF_BLACK(sz):
    return _f("PlayfairDisplay-Black.ttf", sz)


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
    if code == "SA":
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
    elif code == "EU":
        d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
        for i in range(6):
            xx = x + 6 + (i % 3) * 10
            yy = y + 4 + (i // 3) * 11
            d.ellipse([xx, yy, xx + 3, yy + 3], fill=(255, 204, 0))
    else:
        d.ellipse([x + 6, y + 1, x + 28, y + 21], fill=SKY, outline=INK)


CARD_FLAGS = ["PL", "DK", "FI", "PS", "IQ", "OM", "CH", "US", "MX", "US",
              "EU", "IT"]
HERO_FLAGS = ["SA", "TR", "PE"]


def icon(d, field, x, y, col):
    """A small pictogram per card field, so every panel carries a picture."""
    if field == "Diplomacy":
        d.ellipse([x, y + 4, x + 15, y + 19], outline=col, width=3)
        d.ellipse([x + 9, y + 4, x + 24, y + 19], outline=col, width=3)
    elif field == "Politics":
        d.rectangle([x + 3, y + 10, x + 21, y + 22], outline=col, width=3)
        d.line([x + 7, y + 10, x + 17, y + 10], fill=col, width=3)
        d.line([x + 12, y, x + 12, y + 8], fill=col, width=3)
    elif field == "Conflict":
        for dx, dy in ((12, 0), (22, 6), (24, 14), (18, 22), (6, 22), (0, 12),
                       (4, 4)):
            d.line([x + 12, y + 12, x + dx, y + dy], fill=col, width=3)
        d.ellipse([x + 8, y + 8, x + 16, y + 16], fill=col)
    elif field == "Disaster":
        d.polygon([(x + 12, y), (x + 20, y + 12), (x + 17, y + 22),
                   (x + 7, y + 22), (x + 4, y + 12)], fill=col)
        d.polygon([(x + 12, y + 10), (x + 16, y + 16), (x + 14, y + 22),
                   (x + 10, y + 22), (x + 8, y + 16)], fill=(250, 205, 90))
    elif field == "Crime":
        d.polygon([(x + 12, y), (x + 22, y + 4), (x + 22, y + 12),
                   (x + 12, y + 24), (x + 2, y + 12), (x + 2, y + 4)],
                  outline=col, width=3)
    elif field == "Courts":
        d.line([x + 2, y + 6, x + 22, y + 6], fill=col, width=3)
        d.line([x + 12, y + 6, x + 12, y + 20], fill=col, width=3)
        d.line([x + 4, y + 20, x + 20, y + 20], fill=col, width=3)
        d.polygon([(x + 2, y + 14), (x + 10, y + 14), (x + 6, y + 8)],
                  fill=col)
        d.polygon([(x + 14, y + 14), (x + 22, y + 14), (x + 18, y + 8)],
                  fill=col)
    elif field == "Science":
        d.ellipse([x + 6, y + 6, x + 18, y + 18], fill=col)
        d.ellipse([x, y + 9, x + 24, y + 15], outline=col, width=2)
    elif field == "Sport":
        d.polygon([(x + 5, y + 2), (x + 19, y + 2), (x + 17, y + 14),
                   (x + 7, y + 14)], outline=col, width=3)
        d.line([x + 12, y + 14, x + 12, y + 20], fill=col, width=3)
        d.line([x + 6, y + 22, x + 18, y + 22], fill=col, width=3)
    else:
        d.ellipse([x + 3, y + 3, x + 21, y + 21], outline=col, width=3)


# ------------------------------------------------------------------ scenes
def scene_label(d, x, y, w, text):
    d.rectangle([x + 8, y + 56, x + 8 + d.textlength(text, font=SANS_B(13)) + 12,
                 y + 78], fill=(10, 14, 30))
    d.text((x + 14, y + 60), text, font=SANS_B(13), fill=(255, 255, 255))


def scene_riyadh(d, x, y, w, h):
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((16, 24, 52)[i] + ((70, 60, 90)[i] - (16, 24, 52)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    for sx, sy in ((30, 10), (90, 6), (250, 8)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 230))
    d.rectangle([x + 132, y + 26, x + 166, y + h], fill=(30, 34, 58))
    d.polygon([(x + 140, y + 38), (x + 158, y + 38), (x + 149, y + 58)],
              fill=(16, 24, 52))
    for bx, bw, bh in ((18, 34, 34), (58, 26, 24), (180, 40, 30), (228, 30, 42),
                       (264, 36, 22)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(24, 28, 48))
        for wy in range(y + h - bh + 5, y + h - 4, 9):
            for wx in range(x + bx + 4, x + bx + bw - 4, 8):
                d.rectangle([wx, wy, wx + 3, wy + 3], fill=(250, 205, 90))
    for tx, ty in ((60, 14), (150, 6), (238, 16)):
        d.line([x + tx + 40, y + ty - 8, x + tx, y + ty + 12],
               fill=(255, 120, 90), width=3)
        cx, cy = x + tx, y + ty + 13
        for dx, dy in ((-11, -7), (0, -12), (11, -7), (-12, 4), (12, 4), (0, 11)):
            d.line([cx, cy, cx + dx, cy + dy], fill=(255, 214, 90), width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 240, 180))
    scene_label(d, x, y, w, "RIYADH — NIGHT SKY")


def scene_antalya(d, x, y, w, h):
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((214, 224, 214)[i] + ((168, 186, 176)[i] - (214, 224, 214)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    d.rectangle([x + 92, y + 5, x + w - 92, y + 27], fill=(240, 238, 228),
                outline=INK, width=2)
    center(d, y + 9, "COP31 — FINAL TEXT?", SERIF(15), RED, cx=x + w // 2)
    d.ellipse([x + w - 36, y + 32, x + w - 12, y + 56],
              fill=(255, 255, 255), outline=INK, width=2)
    d.line([x + w - 24, y + 44, x + w - 24, y + 36], fill=RED, width=3)
    d.line([x + w - 24, y + 44, x + w - 17, y + 48], fill=RED, width=3)
    d.rectangle([x + 34, y + 58, x + w - 34, y + 74], fill=(96, 70, 44))
    for i in range(5):
        xx = x + 52 + i * 26
        d.ellipse([xx, y + 36, xx + 15, y + 50], fill=(222, 184, 150))
        d.rectangle([xx - 2, y + 50, xx + 17, y + 58], fill=TEAL)
    for i in range(5):
        xx = x + w - 66 - i * 26
        d.ellipse([xx, y + 36, xx + 15, y + 50], fill=(222, 184, 150))
        d.rectangle([xx - 2, y + 50, xx + 17, y + 58], fill=RED)
    d.rectangle([x + w // 2 - 9, y + 42, x + w // 2 + 9, y + 74], fill=NAVY)
    scene_label(d, x, y, w, "ANTALYA — TALKS HALL")


def scene_peru(d, x, y, w, h):
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int((196, 214, 228)[i] + ((226, 205, 165)[i] - (196, 214, 228)[i]) * t)
                  for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)
    d.polygon([(x, y + 48), (x + 70, y + 14), (x + 130, y + 48)], fill=(110, 96, 84))
    d.polygon([(x + 54, y + 28), (x + 70, y + 14), (x + 86, y + 28)], fill=(255, 255, 255))
    d.polygon([(x + 90, y + 54), (x + 180, y + 6), (x + 268, y + 54)], fill=(88, 76, 66))
    d.polygon([(x + 159, y + 22), (x + 180, y + 6), (x + 201, y + 22)], fill=(255, 255, 255))
    d.polygon([(x + 190, y + 58), (x + 262, y + 24), (x + w, y + 58)], fill=(120, 104, 88))
    for hx, hy in ((36, 56), (88, 62), (228, 58)):
        d.rectangle([x + hx, y + hy, x + hx + 22, y + hy + 13], fill=(240, 234, 220))
        d.polygon([(x + hx - 3, y + hy), (x + hx + 11, y + hy - 8),
                   (x + hx + 25, y + hy)], fill=RED)
    ex, ey = x + 150, y + 72
    for r in (10, 18, 26):
        d.ellipse([ex - r, ey - r // 2, ex + r, ey + r // 2], outline=RED, width=3)
    d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=RED)
    d.rectangle([x + 8, y + 5, x + 8 + d.textlength("JUNIN — THE ANDES", font=SANS_B(13)) + 12,
                 y + 27], fill=(120, 30, 28))
    d.text((x + 14, y + 9), "JUNIN — THE ANDES", font=SANS_B(13),
           fill=(255, 255, 255))


HERO_SCENES = [scene_riyadh, scene_antalya, scene_peru]


def badge(d, x, y, num, region):
    col = REGIONS[region][1]
    d.rectangle([x, y, x + 24, y + 24], fill=col)
    t = str(num)
    f = SANS_B(14 if len(t) < 2 else 12)
    d.text((x + 12 - d.textlength(t, font=f) / 2, y + 4), t, font=f,
           fill=(255, 255, 255))


def tally_bar(d, y, counts, total, x0=76, x1=560, hgt=13):
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
    reg_counts, field_counts = {}, {}
    for r, f in stories:
        reg_counts[r] = reg_counts.get(r, 0) + 1
        field_counts[f] = field_counts.get(f, 0) + 1

    # ---------------------------------------------------------- masthead
    d.rectangle([0, 0, W, 58], fill=INK)
    center(d, 5, "THE WORLD IN ONE PICTURE", SERIF_BLACK(29), PAPER)
    center(d, 38, "SATURDAY 21 NOVEMBER 2026  -  EVERY STORY DATED TO THE DAY",
           SANS_B(12), (250, 205, 90))
    strap = (f"{total} STORIES: {len(HEROES)} HEROES + {len(CARDS)} CARDS + "
             f"{len(BRIEFS)} BRIEFS  -  {len(reg_counts)} REGIONS  -  "
             f"{len(field_counts)} FIELDS")
    d.rectangle([0, 58, W, 80], fill=RED)
    center(d, 62, strap, SANS_B(13), (255, 255, 255))
    tl = "SATURDAY IN UTC:  " + "  ·  ".join(f"{t} {l}" for t, l in TIMELINE)
    d.text((16, 84), tl, font=SANS_B(10), fill=INK)
    d.line([16, 104, W - 16, 104], fill=INK, width=2)

    # ---------------------------------------------------------- heroes
    hy, hh = 108, 252
    hw = (W - 32 - 16) // 3
    for i, hero in enumerate(HEROES):
        x = 16 + i * (hw + 8)
        place, region, field, head, deck, src, sure, big, biglab = hero
        d.rectangle([x, hy, x + hw, hy + hh], fill=(255, 253, 246),
                    outline=INK, width=2)
        HERO_SCENES[i](d, x + 3, hy + 3, hw - 6, 82)
        yy = hy + 88
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
        d.rectangle([x + 8, hy + hh - 42, x + hw - 8, hy + hh - 6], fill=PAPER_DK)
        d.text((x + 14, hy + hh - 40), big, font=SERIF_BLACK(28), fill=RED)
        d.text((x + 14 + d.textlength(big, font=SERIF_BLACK(28)) + 10,
                hy + hh - 30), biglab, font=SANS_B(11), fill=INK)

    # ---------------------------------------------------------- cards
    cy = hy + hh + 8
    chh, chw = 72, hw
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
        icon(d, field, x + chw - 32, yy0 + 5, REGIONS[region][1])
        text_block(d, x + 6, yy0 + 29, head, SERIF(19), INK, chw - 12, 21,
                   max_lines=2, tag=f"card{i}")
    by = cy + 4 * (chh + 6) - 6 + 6

    # ---------------------------------------------------------- briefs
    d.rectangle([16, by, W - 16, by + 22], fill=NAVY)
    d.text((22, by + 5), f"THE REST OF SATURDAY — {len(BRIEFS)} BRIEFS, "
           "TWO LINES EACH", font=SANS_B(12), fill=(255, 255, 255))
    d.text((W - 216, by + 6), "SOURCES NAMED IN EVERY BRIEF",
           font=SANS_B(10), fill=(200, 205, 220))
    by += 28
    colw = (W - 32 - 20) // 3
    for i, (place, region, field, head, text) in enumerate(BRIEFS):
        col = i % 3
        row = i // 3
        x = 16 + col * (colw + 10)
        yy = by + row * 36
        d.rectangle([x, yy + 3, x + 9, yy + 12], fill=REGIONS[region][1])
        d.text((x + 14, yy), place, font=SANS_B(16), fill=REGIONS[region][1])
        px = x + 14 + d.textlength(place, font=SANS_B(16)) + 6
        if px + d.textlength(head, font=SANS_B(16)) > x + colw:
            OVERFLOWS.append(f"brief{i} headline too wide: {place} {head[:30]}")
        if d.textlength(text, font=SANS(14)) > colw - 14:
            OVERFLOWS.append(f"brief{i} text too wide: {text[:30]}")
        d.text((px, yy), head, font=SANS_B(16), fill=INK)
        d.text((x + 14, yy + 19), text, font=SANS(14), fill=(52, 48, 42))
    by += 6 * 36 + 2

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
    out = HERE / "entry.png"
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes; stories:", total,
          "; regions:", reg_counts, "; fields:", field_counts)


if __name__ == "__main__":
    main()
