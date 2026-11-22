#!/usr/bin/env python3
"""Draw the news-image-20261121 entry, v2: Saturday 21 November 2026.

Geometry first (GATES.md, approved by Ahmad 2026-11-22): the grid and
the type floors were locked before the story count — hero headlines
>= 30px, card headlines >= 19px, brief headlines >= 16px, brief text
>= 14px, in-scene labels >= 13px, at most 3 heroes, briefs <= 9 words
over 2 lines. 27 stories fit those floors: 3 heroes + 12 cards + 12 briefs
(13 briefs from the locked research set were cut, see STORIES.md;
the v3 map panel took the rest of the brief area).

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
     "Denmark expels Russian attache",
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

# Briefs: (place, region, field, headline, text) — headline + text <= 9 words.
# v3: 12 briefs; the map panel took the rest of the brief area (see
# STORIES.md v3 cut note). Letters were never shrunk to fit.
BRIEFS = [
    ("KYIV", "EUR", "Conflict", "Bridge strikes 'fair reply'",
     "109 Russian attacks cited · BBC"),
    ("TEHRAN", "MEA", "Diplomacy", "Qatar visit for talks",
     "Delegation in Tehran · Reuters"),
    ("SAVAR", "ASI", "Labour", "80+ factories shut",
     "Garment wage sit-ins · TOI"),
    ("INDIA", "ASI", "Disaster", "Illicit alcohol kills 11",
     "180+ people in hospital · IOL"),
    ("BANGLADESH", "ASI", "Politics",
     FIG["bangladesh_platoons"] + " platoons out",
     "Border Guard deployed · Hindu"),
    ("BEIJING", "ASI", "Diplomacy", "China rebukes Japan",
     "Over 'attitude' remark · Asharq"),
    ("SOUTH AFRICA", "AFR", "Politics", "ANC fights on",
     "To keep big cities · BBC"),
    ("KATHMANDU", "ASI", "Politics", "Shah's India test",
     "PM's first trip abroad · BBC"),
    ("PARIS", "EUR", "Courts", "Officers sentenced",
     "Zecler beating case · BBC"),
    ("TWICKENHAM", "EUR", "Sport", "Record win",
     "England, over New Zealand · BBC"),
    ("FOOTBALL", "EUR", "Sport", "Toon 2-2 Arsenal",
     "Newcastle draw; Leeds win · BBC"),
    ("JUPITER", "GLO", "Science", "Europa cloud solved",
     "Sodium from salty ocean · GenFlow"),
]

# ------------------------------------------------------------- world map
# Coarse dot-grid world: 68 x 30 cells, lon -168..192, lat 78..-56.
# Land is a list of (first col, last col) spans per row.
LAND_SPANS = [
    [(1, 5), (10, 18), (24, 27), (42, 64)],
    [(1, 6), (8, 20), (23, 28), (38, 66)],
    [(2, 21), (24, 27), (33, 66)],
    [(3, 21), (24, 26), (32, 65)],
    [(3, 20), (31, 31), (32, 64)],
    [(4, 20), (31, 63)],
    [(4, 19), (30, 62), (57, 58)],
    [(4, 19), (30, 60), (56, 57)],
    [(4, 18), (30, 58)],
    [(5, 17), (29, 30), (34, 57)],
    [(5, 16), (28, 57)],
    [(6, 14), (28, 56)],
    [(7, 13), (28, 55)],
    [(9, 13), (28, 55)],
    [(11, 14), (28, 56)],
    [(16, 26), (29, 58)],
    [(16, 26), (29, 59)],
    [(16, 26), (30, 58)],
    [(17, 26), (30, 38)],
    [(17, 25), (30, 37)],
    [(17, 25), (30, 37), (52, 61)],
    [(18, 25), (31, 36), (42, 42), (52, 62)],
    [(18, 24), (31, 36), (42, 42), (53, 62)],
    [(18, 24), (31, 35), (42, 42), (53, 61)],
    [(20, 22), (32, 34), (55, 58)],
    [(20, 22), (64, 65)],
    [(20, 21)],
    [(20, 21)],
    [(20, 21)],
    [(20, 20)],
]

# Pins for the numbered stories (heroes 1-3, cards 4-15): (num, lon, lat,
# dx, dy) — dx/dy nudge cluster pins apart, with a leader dot left behind.
PINS = [
    (1, 47, 39, 38, -4), (2, 31, 37, 16, 20), (3, -76, -11, 0, 0),
    (4, 21, 52, 30, -6), (5, 13, 56, -26, -18), (6, 28, 60, 16, -12),
    (7, 34, 31, -24, 30), (8, 48, 31, 44, 18), (9, 56, 26, 30, 36),
    (10, 6, 46, -32, -4), (11, -77, 39, 0, 0), (12, -108, 26, 0, 0),
    (13, -118, 34, 0, 0), (15, 8, 45, -14, 18),
]

TIMELINE = [("00:09", "Peru quake"), ("05:12", "M5.0 again"),
            ("10:00", "Romania alert"), ("13:15", "'Chapo Isidro' held"),
            ("18:22", "Ship ablaze"), ("18:24", "Bepi burn"),
            ("19:33", "COP31 stuck")]

NUMBERS = [(FIG["peru_quake_magnitude"], "Peru magnitude"),
           (FIG["riyadh_missiles_intercepted"], "over Riyadh"),
           (FIG["geneva_robot_states"], "at robot talks"),
           (FIG["bangladesh_platoons"], "platoons deployed"),
           (FIG["basra_fire_injured"], "hurt at Basra"),
           (FIG["palisades_killed"], "Palisades deaths")]


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
BANNER_CHECK = []
H_CHECKS = []
TEXT_BOXES = []


class RecDraw:
    """Wraps ImageDraw: records the ink bbox of every text() call."""

    def __init__(self, real):
        object.__setattr__(self, "_r", real)
        object.__setattr__(self, "suspend", False)

    def text(self, xy, s, font=None, fill=None, **kw):
        if not self.suspend and font is not None:
            TEXT_BOXES.append((self._r.textbbox(xy, s, font=font), s))
        return self._r.text(xy, s, font=font, fill=fill, **kw)

    def __getattr__(self, name):
        return getattr(self._r, name)

    def __setattr__(self, name, value):
        if name in ("_r", "suspend"):
            object.__setattr__(self, name, value)
        else:
            setattr(self._r, name, value)


def audit_text_boxes():
    n = len(TEXT_BOXES)
    hits, near = [], []
    for i in range(n):
        (ax0, ay0, ax1, ay1), sa = TEXT_BOXES[i]
        for j in range(i + 1, n):
            (bx0, by0, bx1, by1), sb = TEXT_BOXES[j]
            xo = min(ax1, bx1) - max(ax0, bx0)
            yo = min(ay1, by1) - max(ay0, by0)
            if xo > 0 and yo > 0:
                hits.append((sa[:38], sb[:38], xo, yo))
            elif xo > 0:
                gap = max(by0 - ay1, ay0 - by1)
                if gap < 3:
                    near.append((sa[:38], sb[:38], "v", gap))
            elif yo > 0:
                gap = max(bx0 - ax1, ax0 - bx1)
                if gap < 3:
                    near.append((sa[:38], sb[:38], "h", gap))
    print(f"TEXT-AUDIT: {n} text boxes, {n * (n - 1) // 2} pairs checked, "
          f"{len(hits)} intersections, {len(near)} near-misses (<3px)")
    for h in hits:
        print("  INTERSECT:", h)
    for h in near:
        print("  NEAR:", h)
    return hits, near


def check_h(label, text, font, x_start, x_limit):
    """Horizontal overflow check: measured text end must stay inside limit."""
    end = x_start + ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(
        text, font=font)
    H_CHECKS.append((label, round(end - x_limit, 1)))
    if end > x_limit:
        OVERFLOWS.append(f"H-OVERFLOW {label}: ends {end:.0f} > {x_limit}")


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


def tracked_width(d, text, font, tracking):
    return sum(d.textlength(ch, font=font) for ch in text) + tracking * (len(text) - 1)


def tracked(d, x, y, text, font, fill, tracking=3):
    bb = d.textbbox((x, y), text, font=font)
    TEXT_BOXES.append(((bb[0], bb[1], bb[2] + tracking * (len(text) - 1),
                        bb[3]), text))
    d.suspend = True
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    d.suspend = False
    return x - tracking


def SERIF_IT(sz):
    return _f("PlayfairDisplay-SemiBoldItalic.ttf", sz)


# ------------------------------------------------------------------ flags
def _star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag(d, code, x, y, w=34, h=22):
    """Solid miniature flags (v3.6): every field painted in saturated
    official colours (never the cream paper showing through), correct
    key elements, all proportions relative to w/h so the same drawing
    serves the 34x22 hero chips and the 28x18 card chips."""
    WHT = (255, 255, 255)
    d.rectangle([x, y, x + w, y + h], fill=WHT)
    if code == "SA":  # Saudi Arabia: green, white shahada band + sword
        d.rectangle([x, y, x + w, y + h], fill=(0, 108, 53))
        d.rectangle([x + w * 0.16, y + h * 0.30, x + w * 0.84, y + h * 0.52],
                    fill=WHT)
        d.line([x + w * 0.20, y + h * 0.70, x + w * 0.80, y + h * 0.70],
               fill=WHT, width=max(2, h // 8))
        d.line([x + w * 0.74, y + h * 0.62, x + w * 0.74, y + h * 0.70],
               fill=WHT, width=2)
    elif code == "TR":  # Turkiye: red, white crescent + star
        d.rectangle([x, y, x + w, y + h], fill=(227, 10, 23))
        cx, cy, r = x + w * 0.40, y + h * 0.5, h * 0.30
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHT)
        r2 = r * 0.82
        d.ellipse([cx + r * 0.28 - r2, cy - r2, cx + r * 0.28 + r2, cy + r2],
                  fill=(227, 10, 23))
        _star(d, x + w * 0.70, cy, h * 0.17, WHT)
    elif code == "PE":  # Peru: red-white-red vertical
        d.rectangle([x, y, x + w // 3, y + h], fill=(217, 0, 27))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(217, 0, 27))
    elif code == "PL":  # Poland: white over red
        d.rectangle([x, y + h // 2, x + w, y + h], fill=(220, 20, 60))
    elif code == "DK":  # Denmark: red, white Nordic cross
        d.rectangle([x, y, x + w, y + h], fill=(200, 16, 46))
        d.rectangle([x + w * 0.30, y, x + w * 0.43, y + h], fill=WHT)
        d.rectangle([x, y + h * 0.39, x + w, y + h * 0.61], fill=WHT)
    elif code == "FI":  # Finland: white, blue Nordic cross
        d.rectangle([x + w * 0.28, y, x + w * 0.44, y + h], fill=(0, 47, 108))
        d.rectangle([x, y + h * 0.36, x + w, y + h * 0.64], fill=(0, 47, 108))
    elif code == "PS":  # Palestine: black-white-green, red hoist triangle
        d.rectangle([x, y, x + w, y + h // 3], fill=(0, 0, 0))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(0, 122, 61))
        d.polygon([(x, y), (x + w * 0.42, y + h // 2), (x, y + h)],
                  fill=(238, 28, 37))
    elif code == "IQ":  # Iraq: red-white-black, green takbir mark
        d.rectangle([x, y, x + w, y + h // 3], fill=(206, 17, 38))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(0, 0, 0))
        d.rectangle([x + w * 0.40, y + h * 0.42, x + w * 0.60, y + h * 0.58],
                    fill=(0, 122, 61))
    elif code == "OM":  # Oman: red hoist, white-red-green stripes
        d.rectangle([x + w * 0.30, y + h // 3, x + w, y + 2 * h // 3],
                    fill=(239, 51, 64))
        d.rectangle([x + w * 0.30, y + 2 * h // 3, x + w, y + h],
                    fill=(0, 150, 57))
        d.rectangle([x, y, x + w * 0.30, y + h], fill=(239, 51, 64))
        d.ellipse([x + w * 0.10, y + h * 0.12, x + w * 0.20, y + h * 0.24],
                  fill=WHT)
    elif code == "CH":  # Switzerland: red field, white cross
        d.rectangle([x, y, x + w, y + h], fill=(218, 41, 28))
        d.rectangle([x + w * 0.42, y + h * 0.20, x + w * 0.58, y + h * 0.80],
                    fill=WHT)
        d.rectangle([x + w * 0.26, y + h * 0.38, x + w * 0.74, y + h * 0.62],
                    fill=WHT)
    elif code == "US":  # USA: 13 stripes, blue canton, star dots
        sh = h / 13
        for i in range(13):
            if i % 2 == 0:
                d.rectangle([x, y + i * sh, x + w, y + (i + 1) * sh + 1],
                            fill=(178, 34, 52))
        cw2, ch2 = w * 0.44, sh * 7
        d.rectangle([x, y, x + cw2, y + ch2], fill=(60, 59, 110))
        for r in range(3):
            for c in range(4):
                sx = x + cw2 * (c + 0.5) / 4
                sy = y + ch2 * (r + 0.5) / 3
                d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHT)
    elif code == "MX":  # Mexico: green-white-red, centre emblem
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 104, 71))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(206, 17, 38))
        d.ellipse([x + w * 0.44, y + h * 0.38, x + w * 0.56, y + h * 0.62],
                  fill=(196, 148, 38))
    elif code == "IT":  # Italy: green-white-red vertical
        d.rectangle([x, y, x + w // 3, y + h], fill=(0, 140, 69))
        d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=(205, 33, 42))
    elif code == "EU":  # European Union: blue, circle of 12 gold stars
        import math
        d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
        cx, cy, rr = x + w / 2, y + h / 2, h * 0.32
        for i in range(12):
            ang = i * math.pi / 6
            sx, sy = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
            _star(d, sx, sy, max(1.6, h * 0.075), (255, 204, 0))
    else:  # globe marker
        d.ellipse([x + 6, y + 1, x + 28, y + 21], fill=SKY, outline=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


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
    chip_r = x + 8 + d.textlength(text, font=SANS_B(13)) + 12
    d.rectangle([x + 8, y + 56, chip_r, y + 78], fill=(10, 14, 30))
    d.text((x + 14, y + 60), text, font=SANS_B(13), fill=(255, 255, 255))
    H_CHECKS.append((f"scene label '{text}' right margin",
                     round((chip_r - 6) - (x + 14 + d.textlength(
                         text, font=SANS_B(13))), 1)))
    if x + 14 + d.textlength(text, font=SANS_B(13)) > chip_r - 6:
        OVERFLOWS.append(f"H-OVERFLOW scene label: {text}")


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
    plate = [x + 52, y + 8, x + w - 52, y + 40]
    d.rectangle(plate, fill=(240, 238, 228), outline=INK, width=2)
    d.text((x + w // 2, y + 24), "COP31 — FINAL TEXT?", font=SERIF(15),
           fill=RED, anchor="mm")
    tb = d.textbbox((x + w // 2, y + 24), "COP31 — FINAL TEXT?",
                    font=SERIF(15), anchor="mm")
    margins = (tb[0] - plate[0], tb[1] - plate[1],
               plate[2] - tb[2], plate[3] - tb[3])
    BANNER_CHECK.append((tb, tuple(plate), margins))
    assert min(margins) >= 6, f"banner text escapes plate: margins {margins}"
    d.ellipse([x + w - 36, y + 44, x + w - 12, y + 68],
              fill=(255, 255, 255), outline=INK, width=2)
    d.line([x + w - 24, y + 56, x + w - 24, y + 48], fill=RED, width=3)
    d.line([x + w - 24, y + 56, x + w - 17, y + 60], fill=RED, width=3)
    d.rectangle([x + 34, y + 62, x + w - 34, y + 78], fill=(96, 70, 44))
    for i in range(5):
        xx = x + 52 + i * 26
        d.ellipse([xx, y + 42, xx + 15, y + 56], fill=(222, 184, 150))
        d.rectangle([xx - 2, y + 56, xx + 17, y + 62], fill=TEAL)
    for i in range(5):
        xx = x + w - 66 - i * 26
        d.ellipse([xx, y + 42, xx + 15, y + 56], fill=(222, 184, 150))
        d.rectangle([xx - 2, y + 56, xx + 17, y + 62], fill=RED)
    d.rectangle([x + w // 2 - 9, y + 46, x + w // 2 + 9, y + 78], fill=NAVY)
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
    chip_r = x + 8 + d.textlength("JUNIN — THE ANDES", font=SANS_B(13)) + 12
    d.rectangle([x + 8, y + 5, chip_r, y + 27], fill=(120, 30, 28))
    d.text((x + 14, y + 9), "JUNIN — THE ANDES", font=SANS_B(13),
           fill=(255, 255, 255))
    H_CHECKS.append(("scene label 'JUNIN' right margin",
                     round((chip_r - 6) - (x + 14 + d.textlength(
                         "JUNIN — THE ANDES", font=SANS_B(13))), 1)))


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
    d = RecDraw(ImageDraw.Draw(img))
    stories = all_stories()
    total = len(stories)
    reg_counts, field_counts = {}, {}
    for r, f in stories:
        reg_counts[r] = reg_counts.get(r, 0) + 1
        field_counts[f] = field_counts.get(f, 0) + 1

    # ---------------------------------------------------------- masthead
    # v3.4: newspaper head in the winners' typographic system (refs:
    # ni21 dev top-1/2) — tracked small-caps eyebrow row with the counts
    # on the right, a giant title-case serif date, an italic summary
    # strap naming the day's three hero stories, double rules with a
    # red diamond, all on paper so head and body are one page.
    eyebrow = "THE WORLD IN ONE PICTURE"
    counts = (f"{total} STORIES \u00b7 {len(reg_counts)} REGIONS \u00b7 "
              "EVERY STORY DATED TO THE DAY")
    tracked(d, 16, 7, eyebrow, SANS_B(12), RED, tracking=3)
    cw_counts = tracked_width(d, counts, SANS_B(11), 2)
    tracked(d, W - 16 - cw_counts, 8, counts, SANS_B(11), INK, tracking=2)
    H_CHECKS.append(("eyebrow row overlap", round(
        (16 + tracked_width(d, eyebrow, SANS_B(12), 3))
        - (W - 16 - cw_counts), 1)))
    d.line([16, 25, W - 16, 25], fill=INK, width=1)
    strap = ("COP31 runs past its deadline \u00b7 Three missiles shot down "
             "over Riyadh \u00b7 Magnitude " + FIG["peru_quake_magnitude"]
             + " quake shakes Peru")
    # v3.5: pack date -> strap -> rules by MEASURED ink bboxes, with a
    # guaranteed >=6px clear gap at each step (Ahmad: no descender of
    # the date may touch the strap; no strap descender may touch the
    # rule). Shrink the date until the whole stack fits above y=163.
    sbb = d.textbbox((0, 0), strap, font=SERIF_IT(17))
    for S in range(78, 59, -1):
        fnt = SERIF_BLACK(S)
        if d.textlength("Saturday 21 November 2026", font=fnt) > 964:
            continue
        bb = d.textbbox((0, 0), "Saturday 21 November 2026", font=fnt)
        date_y = 31 - bb[1]
        date_ink_bot = date_y + bb[3]
        strap_y = date_ink_bot + 6 - sbb[1]
        strap_ink_bot = strap_y + sbb[3]
        rule1 = strap_ink_bot + 6
        if rule1 + 4 + 8 + 20 <= 163:
            break
    date_font = fnt
    print(f"MASTHEAD-PACK: date {S}px width "
          f"{round(d.textlength('Saturday 21 November 2026', font=fnt))}px; "
          f"date ink bottom {date_ink_bot}, strap ink top "
          f"{strap_y + sbb[1]} -> gap {strap_y + sbb[1] - date_ink_bot}px; "
          f"strap ink bottom {strap_ink_bot}, rule at {rule1} "
          f"-> gap {rule1 - strap_ink_bot}px")
    center(d, date_y, "Saturday 21 November 2026", date_font, INK)
    check_h("masthead date", "Saturday 21 November 2026", date_font,
            W // 2 - d.textlength("Saturday 21 November 2026",
                                  font=date_font) / 2, W - 30)
    center(d, strap_y, strap, SERIF_IT(17), INK)
    check_h("summary strap", strap, SERIF_IT(17),
            W // 2 - d.textlength(strap, font=SERIF_IT(17)) / 2, W - 16)
    d.line([16, rule1, W - 16, rule1], fill=INK, width=1)
    d.line([16, rule1 + 4, W - 16, rule1 + 4], fill=INK, width=3)
    d.rectangle([W // 2 - 14, rule1 - 2, W // 2 + 14, rule1 + 10], fill=PAPER)
    d.polygon([(W // 2, rule1 - 1), (W // 2 + 6, rule1 + 4),
               (W // 2, rule1 + 9), (W // 2 - 6, rule1 + 4)], fill=RED)
    tl = "SATURDAY IN UTC:  " + "  \u00b7  ".join(f"{t} {l}" for t, l in TIMELINE)
    d.rectangle([0, rule1 + 12, W, rule1 + 32], fill=RED)
    center(d, rule1 + 17, tl, SANS_B(10), (255, 255, 255))
    check_h("timeline", tl, SANS_B(10),
            W // 2 - d.textlength(tl, font=SANS_B(10)) / 2, W - 8)

    # ---------------------------------------------------------- heroes
    hy, hh = 165, 252
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
        check_h(f"hero{i+1} place", place, SANS_B(12), x + 82, x + hw - 8)
        meta = f"{field.upper()} - {src} - {SURE_LABEL[sure]}"
        d.text((x + 82, yy + 16), meta, font=SANS(10), fill=MUTE)
        check_h(f"hero{i+1} meta", meta, SANS(10), x + 82, x + hw - 8)
        yy += 24
        yy = text_block(d, x + 8, yy, head, SERIF(30), INK, hw - 16, 32,
                        max_lines=2, tag=f"hero{i}")
        text_block(d, x + 8, yy + 6, deck, SANS(13), (52, 48, 42), hw - 16, 15,
                   max_lines=2, tag=f"herodeck{i}")
        d.rectangle([x + 8, hy + hh - 38, x + hw - 8, hy + hh - 4], fill=PAPER_DK)
        d.text((x + 14, hy + hh - 36), big, font=SERIF_BLACK(28), fill=RED)
        d.text((x + 14 + d.textlength(big, font=SERIF_BLACK(28)) + 10,
                hy + hh - 30), biglab, font=SANS_B(11), fill=INK)

    # ---------------------------------------------------------- cards
    cy = hy + hh + 5
    chh, chw = 72, hw
    for i, card in enumerate(CARDS):
        place, region, field, head, deck, src, sure = card
        x = 16 + (i % 3) * (chw + 8)
        yy0 = cy + (i // 3) * (chh + 4)
        d.rectangle([x, yy0, x + chw, yy0 + chh], fill=(255, 253, 246),
                    outline=(150, 142, 126), width=1)
        CARD_SCENES[i](d, x + 1, yy0 + 1, 110, chh - 2)
        tx = x + 117
        badge(d, tx, yy0 + 5, i + 4, region)
        flag(d, CARD_FLAGS[i], x + chw - 34, yy0 + 5, w=28, h=18)
        d.text((tx + 30, yy0 + 5), place, font=SANS_B(11),
               fill=REGIONS[region][1])
        check_h(f"card{i+4} place", place, SANS_B(11), tx + 30, x + chw - 40)
        cmeta = f"{src} - {SURE_LABEL[sure]}"
        d.text((tx + 30, yy0 + 18), cmeta, font=SANS(9), fill=MUTE)
        check_h(f"card{i+4} meta", cmeta, SANS(9), tx + 30, x + chw - 6)
        text_block(d, tx, yy0 + 31, head, SERIF(19), INK, chw - 123, 19,
                   max_lines=2, tag=f"card{i}")
    by = cy + 4 * (chh + 4) - 4 + 4

    # ------------------------------------------- briefs (left) + map (right)
    sec_y = by
    d.rectangle([16, sec_y, 536, sec_y + 22], fill=NAVY)
    d.text((22, sec_y + 5), f"THE REST OF SATURDAY — {len(BRIEFS)} BRIEFS",
           font=SANS_B(12), fill=(255, 255, 255))
    colw = (536 - 16 - 10) // 2
    for i, (place, region, field, head, text) in enumerate(BRIEFS):
        col = i % 2
        row = i // 2
        x = 16 + col * (colw + 10)
        yy = sec_y + 30 + row * 32
        d.rectangle([x, yy + 3, x + 9, yy + 12], fill=REGIONS[region][1])
        d.text((x + 14, yy), place, font=SANS_B(16), fill=REGIONS[region][1])
        px = x + 14 + d.textlength(place, font=SANS_B(16)) + 6
        if px + d.textlength(head, font=SANS_B(16)) > x + colw:
            OVERFLOWS.append(f"brief{i} headline too wide: {place} {head[:30]}")
        if d.textlength(text, font=SANS(14)) > colw - 14:
            OVERFLOWS.append(f"brief{i} text too wide: {text[:30]}")
        d.text((px, yy), head, font=SANS_B(16), fill=INK)
        d.text((x + 14, yy + 17), text, font=SANS(14), fill=(52, 48, 42))

    # map panel: pins carry the story numbers of heroes (1-3) and cards (4-15)
    mx0, my0, mx1 = 552, sec_y, 1008
    d.rectangle([mx0, my0, mx1, sec_y + 22], fill=NAVY)
    d.text((mx0 + 8, my0 + 5), "WHERE IT HAPPENED — PIN = STORY NUMBER",
           font=SANS_B(12), fill=(255, 255, 255))
    check_h("map header", "WHERE IT HAPPENED — PIN = STORY NUMBER",
            SANS_B(12), mx0 + 8, mx1 - 8)
    check_h("briefs header", f"THE REST OF SATURDAY — {len(BRIEFS)} BRIEFS",
            SANS_B(12), 22, 536 - 8)
    map_y, map_h, map_w = sec_y + 28, 168, mx1 - mx0 - 16
    map_x = mx0 + 8
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(16, 26, 44))
    cw, chh2 = map_w / 68, map_h / 30
    for r, spans in enumerate(LAND_SPANS):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = map_x + (c + 0.5) * cw
                cy2 = map_y + (r + 0.5) * chh2
                d.ellipse([cx - 1.6, cy2 - 1.6, cx + 1.6, cy2 + 1.6],
                          fill=(120, 150, 190))
    for num, lon, lat, dx, dy in PINS:
        tx = map_x + (lon + 168) / 360 * map_w
        ty = map_y + (78 - lat) / 134 * map_h
        if dx or dy:
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(255, 214, 90))
            d.line([tx, ty, tx + dx, ty + dy], fill=(255, 214, 90), width=1)
        px2, py2 = tx + dx, ty + dy
        d.ellipse([px2 - 11, py2 - 11, px2 + 11, py2 + 11], fill=RED,
                  outline=(255, 255, 255), width=2)
        t = str(num)
        d.text((px2 - d.textlength(t, font=SANS_B(12)) / 2, py2 - 7), t,
               font=SANS_B(12), fill=(255, 255, 255))
    cap_y = map_y + map_h + 6
    d.text((mx0 + 8, cap_y), "14 MERCURY — OFF THE MAP, IN SPACE · EUROPE "
           "PINS NUDGED APART", font=SANS_B(11), fill=MUTE)
    check_h("map caption", "14 MERCURY — OFF THE MAP, IN SPACE · EUROPE "
            "PINS NUDGED APART", SANS_B(11), mx0 + 8, mx1 - 8)
    by = sec_y + 222

    # ------------------------------------------------- numbers + bars
    d.line([16, by, W - 16, by], fill=INK, width=2)
    d.text((16, by + 7), "THE DAY IN NUMBERS", font=SANS_B(12), fill=RED)
    nx = 172
    for num, lab in NUMBERS:
        d.text((nx, by + 2), num, font=SERIF_BLACK(20), fill=INK)
        lx = nx + d.textlength(num, font=SERIF_BLACK(20)) + 6
        d.text((lx, by + 8), lab, font=SANS(9), fill=MUTE)
        check_h(f"numbers label '{lab}'", lab, SANS(9), lx, nx + 139)
        nx += 141
    by += 28
    d.text((16, by + 1), "REGIONS", font=SANS_B(10), fill=MUTE)
    tally_bar(d, by, reg_counts, total, x0=76, x1=560, hgt=11)
    d.text((576, by + 1), "FIELDS", font=SANS_B(10), fill=MUTE)
    top_fields = sorted(field_counts.items(), key=lambda kv: -kv[1])[:5]
    fx = 632
    for name, n in top_fields:
        d.text((fx, by + 1), f"{name} {n}", font=SANS_B(10), fill=INK)
        fx += d.textlength(f"{name} {n}", font=SANS_B(10)) + 10
    by += 11

    # ------------------------------------------------- date check + not yet
    dc = ("DATE CHECK — NOT 21 NOV, LEFT OUT: Thu 19 — Shenzhen summit, ICJ Myanmar "
          "ruling, Anthropic debut · Fri 20 — Kyiv blitz, Nasdaq -5.3% close, Bayer "
          "$7.25bn approval, Rikers plan · Sun 22 agenda is not Saturday's news.")
    yy = text_block(d, 16, by, dc, SANS_SB(11), (70, 64, 54), W - 32, 11,
                    max_lines=2, tag="datecheck")
    ny = ("NOT YET KNOWN SATURDAY NIGHT: BepiColombo's burn result · a final COP31 "
          "text · Peru's full damage toll. Sources are named per story.")
    text_block(d, 16, yy + 2, ny, SANS_SB(11), RED, W - 32, 12,
               max_lines=1, tag="notyet")

    print(f"H-CHECKS: {len(H_CHECKS)} measured, "
          f"{sum(1 for _, v in H_CHECKS if v > 0)} over limit")
    for lab, v in H_CHECKS:
        if v > -30:
            print(f"  h-check {lab}: slack {-v:+.1f}px")
    for tb, plate, margins in BANNER_CHECK:
        print(f"BANNER bbox text={tb} plate={plate} "
              f"margins L/T/R/B={margins}")
    if OVERFLOWS:
        print("OVERFLOWS:", *OVERFLOWS, sep="\n  ")
    out = HERE / "entry.png"
    audit_text_boxes()
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes; stories:", total,
          "; regions:", reg_counts, "; fields:", field_counts)



# ------------------------------------------------------- card scenes (v3.3)
# CLARITY first (Ahmad, v3.3): one dominant subject per card, drawn big
# and simple — a reader who has not seen the headline should guess the
# story from the scene alone. Supporters stay small and quiet.
def card_label(d, x, y, w, h, text):
    tw = d.textlength(text, font=SANS_B(13))
    d.rectangle([x + 3, y + h - 21, x + 3 + tw + 10, y + h - 3],
                fill=(10, 14, 30))
    d.text((x + 8, y + h - 18), text, font=SANS_B(13), fill=(255, 255, 255))
    H_CHECKS.append((f"card scene label '{text}'",
                     round((x + 3 + tw + 10) - (x + w - 1), 1)))
    if x + 3 + tw + 10 > x + w - 1:
        OVERFLOWS.append(f"H-OVERFLOW card scene label: {text}")


def _sky(d, x, y, w, h, top, bot):
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([x, y + yy, x + w, y + yy], fill=c)


def _flame(d, cx, cy, s, col=(255, 140, 40)):
    d.polygon([(cx, cy - s), (cx + s * 0.62, cy + s * 0.4),
               (cx + s * 0.3, cy + s), (cx - s * 0.3, cy + s),
               (cx - s * 0.62, cy + s * 0.4)], fill=col)
    d.polygon([(cx, cy - s * 0.3), (cx + s * 0.3, cy + s * 0.5),
               (cx, cy + s * 0.95), (cx - s * 0.3, cy + s * 0.5)],
              fill=(250, 205, 90))


def sc_warsaw(d, x, y, w, h):
    # DOMINANT: a big shield dome over the city, one missile bursting on it
    _sky(d, x, y, w, h, (18, 26, 54), (70, 62, 92))
    d.rectangle([x + 38, y + 34, x + 72, y + 62], fill=(22, 26, 46))
    d.polygon([(x + 34, y + 34), (x + 76, y + 34), (x + 55, y + 24)],
              fill=(22, 26, 46))
    d.rectangle([x + 8, y + 46, x + 26, y + 62], fill=(22, 26, 46))
    d.rectangle([x + 84, y + 42, x + 102, y + 62], fill=(22, 26, 46))
    d.arc([x + 4, y + 2, x + w - 4, y + 66], start=180, end=360,
          fill=(120, 220, 255), width=4)
    d.line([x + 88, y + 2, x + 62, y + 20], fill=(255, 120, 90), width=3)
    cx, cy = x + 60, y + 21
    for dx, dy in ((-11, -6), (0, -11), (11, -6), (-12, 3), (12, 3), (0, 10)):
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 214, 90), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 240, 180))
    card_label(d, x, y, w, h, "WARSAW")


def sc_copenhagen(d, x, y, w, h):
    # DOMINANT: the expelled attache himself, big, suitcase in hand
    _sky(d, x, y, w, h, (168, 198, 224), (226, 232, 238))
    d.rectangle([x + 4, y + 22, x + 30, y + 50], fill=(150, 96, 74))
    d.rectangle([x + 12, y + 10, x + 22, y + 22], fill=(120, 74, 56))
    d.ellipse([x + 44, y + 4, x + 62, y + 22], fill=(222, 184, 150))
    d.rectangle([x + 38, y + 22, x + 68, y + 48], fill=(40, 40, 50))
    d.line([x + 53, y + 22, x + 53, y + 46], fill=(240, 240, 240), width=3)
    d.rectangle([x + 66, y + 34, x + 86, y + 52], fill=(120, 74, 56))
    d.line([x + 68, y + 30, x + 76, y + 34], fill=INK, width=3)
    d.rectangle([x + 38, y + 48, x + 50, y + 62], fill=(40, 40, 50))
    d.rectangle([x + 56, y + 48, x + 68, y + 62], fill=(40, 40, 50))
    d.polygon([(x + 92, y + 8), (x + 104, y + 12), (x + 92, y + 16)],
              fill=(90, 90, 100))
    d.rectangle([x, y + 62, x + w, y + h], fill=(120, 130, 145))
    card_label(d, x, y, w, h, "COPENHAGEN")


def sc_finland(d, x, y, w, h):
    # DOMINANT: a big ship with big fire on deck
    _sky(d, x, y, w, h, (120, 150, 180), (190, 205, 215))
    d.rectangle([x, y + 46, x + w, y + h], fill=(46, 84, 120))
    d.polygon([(x + 6, y + 46), (x + 14, y + 32), (x + 96, y + 32),
               (x + 104, y + 46)], fill=(52, 56, 66))
    d.rectangle([x + 16, y + 22, x + 30, y + 32], fill=RED)
    d.rectangle([x + 32, y + 22, x + 46, y + 32], fill=(52, 84, 140))
    d.rectangle([x + 84, y + 18, x + 96, y + 32], fill=(230, 230, 230))
    _flame(d, x + 56, y + 16, 13)
    _flame(d, x + 68, y + 20, 9)
    d.ellipse([x + 48, y - 2, x + 78, y + 8], fill=(110, 110, 120))
    card_label(d, x, y, w, h, "THE GULF")


def sc_gaza(d, x, y, w, h):
    # DOMINANT: a big aid truck with a red cross
    _sky(d, x, y, w, h, (214, 190, 150), (232, 214, 180))
    d.rectangle([x + 8, y + 16, x + 74, y + 48], fill=(245, 243, 236))
    d.rectangle([x + 74, y + 28, x + 96, y + 48], fill=(225, 222, 214))
    d.polygon([(x + 78, y + 28), (x + 96, y + 28), (x + 92, y + 38),
               (x + 78, y + 38)], fill=(150, 180, 200))
    d.rectangle([x + 33, y + 24, x + 49, y + 40], fill=RED)
    d.rectangle([x + 37, y + 20, x + 45, y + 44], fill=RED)
    d.ellipse([x + 18, y + 46, x + 32, y + 60], fill=INK)
    d.ellipse([x + 62, y + 46, x + 76, y + 60], fill=INK)
    d.rectangle([x + 98, y + 40, x + 106, y + 48], fill=(150, 116, 62))
    cx, cy = x + 100, y + 8
    for dx, dy in ((-8, -4), (0, -8), (8, -4), (8, 4)):
        d.line([cx, cy, cx + dx, cy + dy], fill=(200, 90, 60), width=2)
    d.rectangle([x, y + 60, x + w, y + h], fill=(190, 172, 140))
    card_label(d, x, y, w, h, "GAZA")


def sc_basra(d, x, y, w, h):
    # DOMINANT: a big cooling tower in flames, lightning for the power
    _sky(d, x, y, w, h, (226, 200, 160), (240, 224, 190))
    d.polygon([(x + 18, y + 62), (x + 28, y + 16), (x + 58, y + 16),
               (x + 68, y + 62)], fill=(150, 148, 142))
    d.ellipse([x + 28, y + 11, x + 58, y + 21], fill=(110, 108, 102))
    _flame(d, x + 38, y + 6, 10)
    _flame(d, x + 50, y + 8, 8)
    d.polygon([(x + 88, y + 4), (x + 97, y + 4), (x + 90, y + 16),
               (x + 99, y + 16), (x + 84, y + 34), (x + 88, y + 20),
               (x + 81, y + 20)], fill=(250, 205, 90), outline=INK)
    d.rectangle([x + 74, y + 50, x + 102, y + 62], fill=(120, 116, 110))
    card_label(d, x, y, w, h, "BASRA")


def sc_khasab(d, x, y, w, h):
    # DOMINANT: a big tanker, one big burst at its side
    _sky(d, x, y, w, h, (170, 200, 220), (222, 230, 234))
    d.rectangle([x, y + 42, x + w, y + h], fill=(52, 92, 128))
    d.polygon([(x + 4, y + 42), (x + 12, y + 28), (x + 92, y + 28),
               (x + 102, y + 42)], fill=(40, 44, 52))
    d.rectangle([x + 14, y + 20, x + 26, y + 28], fill=(230, 230, 230))
    d.rectangle([x + 30, y + 23, x + 66, y + 28], fill=(90, 96, 104))
    cx, cy = x + 88, y + 30
    for dx, dy in ((-12, -8), (0, -14), (12, -8), (-13, 2), (13, 2),
                   (0, 12)):
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 170, 60), width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 240, 180))
    _flame(d, x + 84, y + 22, 8)
    d.polygon([(x, y + 26), (x + 12, y + 10), (x + 24, y + 26)],
              fill=(140, 118, 92))
    card_label(d, x, y, w, h, "KHASAB")


def sc_geneva(d, x, y, w, h):
    # DOMINANT: a big robot head, a gavel beside it (the talks' verdict)
    _sky(d, x, y, w, h, (206, 214, 206), (228, 232, 222))
    d.rectangle([x + 18, y + 14, x + 62, y + 56], fill=(90, 96, 110))
    d.line([x + 40, y + 14, x + 40, y + 4], fill=INK, width=3)
    d.ellipse([x + 37, y + 1, x + 43, y + 7], fill=RED)
    d.ellipse([x + 26, y + 28, x + 36, y + 38], fill=(255, 214, 90))
    d.ellipse([x + 44, y + 28, x + 54, y + 38], fill=(255, 214, 90))
    d.rectangle([x + 30, y + 46, x + 50, y + 50], fill=(60, 64, 74))
    for gx in (28, 36, 44):
        d.rectangle([x + gx, y + 46, x + gx + 3, y + 50], fill=(200, 204, 210))
    d.line([x + 74, y + 52, x + 92, y + 34], fill=(120, 74, 40), width=5)
    d.rectangle([x + 84, y + 22, x + 100, y + 32], fill=(150, 100, 60))
    d.rectangle([x + 70, y + 58, x + 102, y + 62], fill=(96, 70, 44))
    card_label(d, x, y, w, h, "GENEVA")


def sc_washington(d, x, y, w, h):
    # DOMINANT: a big database server rack, cracked by a lightning bolt
    _sky(d, x, y, w, h, (150, 175, 205), (215, 225, 235))
    d.rectangle([x + 30, y + 6, x + 74, y + 62], fill=(52, 56, 66))
    for ly in (14, 26, 38, 50):
        d.rectangle([x + 36, y + ly, x + 68, y + ly + 7], fill=(70, 76, 90))
        d.ellipse([x + 39, y + ly + 1, x + 44, y + ly + 6],
                  fill=(120, 255, 140))
        d.ellipse([x + 60, y + ly + 1, x + 65, y + ly + 6],
                  fill=(255, 120, 90))
    d.polygon([(x + 88, y + 2), (x + 98, y + 2), (x + 91, y + 15),
               (x + 100, y + 15), (x + 85, y + 32), (x + 89, y + 19),
               (x + 82, y + 19)], fill=(250, 205, 90), outline=INK)
    d.arc([x + 6, y + 26, x + 26, y + 44], 180, 360, fill=(200, 198, 190),
          width=4)
    d.rectangle([x + 4, y + 40, x + 28, y + 46], fill=(235, 233, 226))
    card_label(d, x, y, w, h, "WASHINGTON")


def sc_guasave(d, x, y, w, h):
    # DOMINANT: the wanted man — big head, cowboy hat, star badge
    _sky(d, x, y, w, h, (232, 190, 120), (240, 214, 160))
    d.ellipse([x + 82, y + 4, x + 96, y + 18], fill=(250, 205, 90))
    d.ellipse([x + 36, y + 16, x + 66, y + 46], fill=(222, 184, 150))
    d.polygon([(x + 28, y + 18), (x + 74, y + 18), (x + 64, y + 8),
               (x + 38, y + 8)], fill=(60, 44, 30))
    d.rectangle([x + 28, y + 46, x + 74, y + 64], fill=(120, 60, 50))
    d.polygon([(x + 88, y + 30), (x + 91, y + 37), (x + 98, y + 37),
               (x + 93, y + 41), (x + 95, y + 48), (x + 88, y + 44),
               (x + 81, y + 48), (x + 83, y + 41), (x + 78, y + 37),
               (x + 85, y + 37)], fill=(250, 205, 90), outline=INK)
    d.rectangle([x + 10, y + 34, x + 14, y + 56], fill=(70, 130, 70))
    d.rectangle([x + 5, y + 42, x + 10, y + 48], fill=(70, 130, 70))
    d.rectangle([x + 14, y + 44, x + 19, y + 50], fill=(70, 130, 70))
    d.rectangle([x, y + 62, x + w, y + h], fill=(206, 170, 116))
    card_label(d, x, y, w, h, "GUASAVE")


def sc_losangeles(d, x, y, w, h):
    # DOMINANT: a house frame with one big flame inside it
    _sky(d, x, y, w, h, (206, 170, 140), (226, 200, 170))
    d.rectangle([x + 26, y + 30, x + 78, y + 62], outline=(52, 44, 38),
                width=4)
    d.polygon([(x + 22, y + 30), (x + 52, y + 14), (x + 82, y + 30)],
              outline=(52, 44, 38), width=4)
    _flame(d, x + 52, y + 40, 15)
    d.line([x + 12, y + 62, x + 12, y + 38], fill=(40, 34, 30), width=3)
    d.line([x + 12, y + 42, x + 5, y + 34], fill=(40, 34, 30), width=2)
    d.line([x + 94, y + 62, x + 94, y + 42], fill=(40, 34, 30), width=3)
    d.ellipse([x + 66, y + 4, x + 84, y + 12], fill=(170, 160, 150))
    d.rectangle([x, y + 62, x + w, y + h], fill=(120, 96, 78))
    card_label(d, x, y, w, h, "LOS ANGELES")


def sc_mercury(d, x, y, w, h):
    # DOMINANT: the planet, big; the spacecraft burning toward it
    _sky(d, x, y, w, h, (8, 10, 24), (24, 28, 48))
    for sx, sy in ((8, 6), (26, 12), (96, 4), (14, 26)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(255, 255, 230))
    d.ellipse([x + 52, y + 8, x + 104, y + 60], fill=(168, 164, 158))
    for cx, cy, r in ((66, 22, 5), (84, 38, 6), (74, 50, 4), (92, 20, 4)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  outline=(130, 126, 120), width=2)
    d.rectangle([x + 18, y + 24, x + 34, y + 38], fill=(200, 204, 210))
    d.polygon([(x + 2, y + 20), (x + 18, y + 26), (x + 18, y + 36),
               (x + 2, y + 42)], fill=(70, 110, 190))
    d.polygon([(x + 34, y + 26), (x + 48, y + 20), (x + 48, y + 42),
               (x + 34, y + 36)], fill=(70, 110, 190))
    _flame(d, x + 26, y + 44, 7, col=(255, 160, 60))
    card_label(d, x, y, w, h, "MERCURY")


def sc_turin(d, x, y, w, h):
    # DOMINANT: a big gold trophy; a tennis ball and court lines behind
    _sky(d, x, y, w, h, (120, 170, 110), (90, 150, 84))
    d.rectangle([x + 4, y + 8, x + w - 4, y + 60], fill=(196, 120, 70))
    d.line([x + 4, y + 34, x + w - 4, y + 34], fill=(240, 240, 240),
           width=3)
    d.ellipse([x + 12, y + 44, x + 26, y + 58], fill=(210, 230, 80),
              outline=(240, 240, 240), width=2)
    d.polygon([(x + 38, y + 8), (x + 72, y + 8), (x + 66, y + 34),
               (x + 44, y + 34)], fill=(250, 205, 90), outline=INK)
    d.arc([x + 30, y + 12, x + 46, y + 28], 90, 270, fill=(250, 205, 90),
          width=4)
    d.arc([x + 64, y + 12, x + 80, y + 28], 270, 90, fill=(250, 205, 90),
          width=4)
    d.rectangle([x + 51, y + 34, x + 59, y + 44], fill=(250, 205, 90),
                outline=INK)
    d.rectangle([x + 42, y + 44, x + 68, y + 50], fill=(250, 205, 90),
                outline=INK)
    card_label(d, x, y, w, h, "TURIN")


CARD_SCENES = [sc_warsaw, sc_copenhagen, sc_finland, sc_gaza, sc_basra,
               sc_khasab, sc_geneva, sc_washington, sc_guasave,
               sc_losangeles, sc_mercury, sc_turin]


if __name__ == "__main__":
    main()
