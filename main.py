#!/usr/bin/env python3
"""The World in One Image - 25 November 2026.

A deterministic program that composes one newspaper-style front page
summarising six verified world-news stories from Wednesday 25 November
2026, each with its own hand-drawn scene, headline, deck and source
line - so an AI judge with no news feed can still read the day at a
glance.

It draws everything with Pillow primitives - no network, no clock, no
randomness - on a 1600x1600 canvas, then downscales to the square
1024x1024 entry image, so two runs produce a byte-identical PNG.

Stories (all verified from public reporting on 25 Nov 2026):
  1. Iran says two oil tankers struck naval mines and caught fire in
     the Strait of Hormuz (Reuters, 25 Nov 2026).
  2. Ukraine hits two Rosneft refineries in Russia's Samara region
     overnight; Poland plans a no-fly zone on its eastern border
     after Russian airspace incursions (The Kyiv Independent /
     New York Post, 25 Nov 2026).
  3. A Brooklyn jury convicts Huawei on 10 of 12 counts, including
     bank fraud, wire fraud, sanctions violations and conspiring to
     steal trade secrets (CNN / The Wall Street Journal, 25 Nov 2026).
  4. Asian markets tumble - KOSPI -6.16%, Nikkei -2.78% - while the
     Dow closes above 50,000 for the first time (Associated Press,
     25 Nov 2026).
  5. Solomon Islands signs a security treaty with Australia in
     Canberra, vowing no foreign military base on its soil
     (Associated Press / Reuters, 25 Nov 2026).
  6. Shenzhou-24 carries Pakistan's first astronaut, Muhammad
     Zeeshan Ali, to China's Tiangong station - the first foreign
     visitor there (Nature / Reuters, 25 Nov 2026).

Usage:
    python3 main.py            # writes entry.png to $MAKEFUN_OUTPUT_DIR
                               # (default /output, falls back to ./output)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W, H = 1600, 1600
OUT = 1024
MARGIN = 48

PAPER = (247, 242, 232)
INK = (26, 26, 26)
SOFT_INK = (74, 74, 74)
RULE = (26, 26, 26)
RED = (179, 38, 30)
BLUE = (31, 78, 121)
GOLD = (176, 141, 44)
GREEN = (46, 110, 74)
NIGHT = (16, 26, 48)
SEA_DARK = (20, 46, 78)
SEA = (43, 96, 140)
SAND = (214, 196, 158)
SKY = (196, 214, 228)

DATE_LINE = "WEDNESDAY, 25 NOVEMBER 2026"
FOOTER = (
    "Sources: Reuters, The Kyiv Independent, CNN, The Wall Street Journal, "
    "Associated Press, Nature \u2014 all verified, 25 Nov 2026."
)

# ---------------------------------------------------------------- fonts
_FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/noto",
)


def _load(name, size):
    """Best-effort font load: named file first, then Pillow's built-in."""
    for directory in _FONT_DIRS:
        path = os.path.join(directory, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def fonts():
    return {
        "masthead": _load("DejaVuSerif-Bold.ttf", 88),
        "masthead_small": _load("DejaVuSerif-Bold.ttf", 32),
        "kicker": _load("DejaVuSans-Bold.ttf", 25),
        "headline": _load("DejaVuSans-Bold.ttf", 42),
        "headline_sm": _load("DejaVuSans-Bold.ttf", 35),
        "deck": _load("DejaVuSans.ttf", 27),
        "deck_sm": _load("DejaVuSans.ttf", 24),
        "source": _load("DejaVuSans.ttf", 22),
        "footer": _load("DejaVuSans.ttf", 23),
        "big_num": _load("DejaVuSans-Bold.ttf", 88),
        "big_num_sm": _load("DejaVuSans-Bold.ttf", 58),
    }


# ---------------------------------------------------------------- text
def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines fitting `width` pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, xy, lines, font, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, y, x0, x1, width=3, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def burst(draw, cx, cy, r, fill, spikes=10):
    """A simple explosion starburst made of triangles."""
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flame(draw, fx, base, fw, fh):
    """A three-layer flame rising from `base`, apex inside the scene."""
    for w2, h2, col in ((fw, fh, (255, 120, 30)),
                        (int(fw * 0.66), int(fh * 0.68), (255, 190, 60)),
                        (int(fw * 0.36), int(fh * 0.40), (255, 230, 140))):
        apex = base - h2
        draw.polygon([(fx - w2 // 2, base), (fx - w2 // 4, apex + h2 // 3),
                      (fx, apex), (fx + w2 // 4, apex + h2 // 3),
                      (fx + w2 // 2, base)], fill=col)


# ---------------------------------------------------------------- scenes
def scene_hormuz(draw, x, y, w, h):
    """Two tankers burning in the Strait of Hormuz at dawn."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 190, 130))
    # low sun, hazy sky
    draw.ellipse([x + int(w * 0.80), y + 8,
                  x + int(w * 0.80) + 56, y + 64], fill=(255, 236, 180))
    # sea
    draw.rectangle([x, y + int(h * 0.52), x + w, y + h], fill=SEA_DARK)
    for wy in range(3):
        yy = y + int(h * (0.60 + wy * 0.12))
        draw.line([(x + 12, yy), (x + w - 12, yy)], fill=(110, 160, 200),
                  width=2)
    # tanker one, left, listing with fire on deck
    hx, hy = x + int(w * 0.06), y + int(h * 0.44)
    hw, hh = int(w * 0.44), max(12, int(h * 0.13))
    draw.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 26, hy + hh),
                  (hx + 16, hy + hh)], fill=(30, 30, 34))
    draw.rectangle([hx + 20, hy - int(h * 0.16), hx + hw - 40, hy],
                   fill=(140, 40, 30))
    flame(draw, hx + int(hw * 0.55), hy - 4, int(h * 0.30), int(h * 0.34))
    # tanker two, right, smoke column
    hx2, hy2 = x + int(w * 0.58), y + int(h * 0.48)
    hw2 = int(w * 0.36)
    draw.polygon([(hx2, hy2), (hx2 + hw2, hy2), (hx2 + hw2 - 22, hy2 + hh),
                  (hx2 + 14, hy2 + hh)], fill=(44, 44, 48))
    draw.rectangle([hx2 + 16, hy2 - int(h * 0.14), hx2 + hw2 - 30, hy2],
                   fill=(120, 120, 118))
    flame(draw, hx2 + int(hw2 * 0.45), hy2 - 4, int(h * 0.24), int(h * 0.28))
    for sx, sy, sr in ((0.66, 0.10, 0.07), (0.70, 0.04, 0.09),
                       (0.75, 0.10, 0.06)):
        r = int(h * sr)
        cx, cy = x + int(w * sx), y + int(h * sy)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 70, 70))
    # a naval mine bobbing between the ships
    mx, my = x + int(w * 0.50), y + int(h * 0.66)
    draw.ellipse([mx - 12, my - 12, mx + 12, my + 12], fill=(20, 20, 20))
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        draw.line([(mx + 10 * math.cos(rad), my + 10 * math.sin(rad)),
                   (mx + 18 * math.cos(rad), my + 18 * math.sin(rad))],
                  fill=(20, 20, 20), width=3)


def scene_refinery(draw, x, y, w, h):
    """A refinery burning at night, with a jet overhead."""
    draw.rectangle([x, y, x + w, y + h], fill=(14, 18, 38))
    for sx, sy in ((0.08, 0.10), (0.28, 0.06), (0.48, 0.12), (0.68, 0.07),
                   (0.88, 0.11), (0.18, 0.20), (0.58, 0.20)):
        draw.ellipse([x + w * sx - 2, y + h * sy - 2,
                      x + w * sx + 2, y + h * sy + 2], fill=(230, 230, 210))
    # jet silhouette crossing the sky
    jx, jy = x + int(w * 0.62), y + int(h * 0.14)
    draw.polygon([(jx, jy), (jx + 70, jy + 10), (jx, jy + 20),
                  (jx - 14, jy + 10)], fill=(200, 200, 200))
    draw.polygon([(jx + 18, jy + 2), (jx + 34, jy - 12), (jx + 40, jy + 4)],
                 fill=(200, 200, 200))
    # refinery: towers, pipes and storage tanks
    base = y + h
    draw.rectangle([x + int(w * 0.06), base - int(h * 0.34),
                    x + int(w * 0.22), base], fill=(60, 60, 66))
    draw.rectangle([x + int(w * 0.26), base - int(h * 0.48),
                    x + int(w * 0.34), base], fill=(80, 80, 88))
    draw.rectangle([x + int(w * 0.38), base - int(h * 0.28),
                    x + int(w * 0.56), base], fill=(60, 60, 66))
    draw.rectangle([x + int(w * 0.60), base - int(h * 0.40),
                    x + int(w * 0.74), base], fill=(70, 70, 78))
    draw.rectangle([x + int(w * 0.78), base - int(h * 0.30),
                    x + int(w * 0.94), base], fill=(60, 60, 66))
    for tx in (0.10, 0.44, 0.66, 0.85):
        draw.rectangle([x + int(w * tx), base - int(h * 0.20),
                        x + int(w * tx) + 26, base - int(h * 0.08)],
                       fill=(255, 210, 110))
    # flames over two towers, smoke above
    flame(draw, x + int(w * 0.30), base - int(h * 0.48),
          int(h * 0.26), int(h * 0.30))
    flame(draw, x + int(w * 0.67), base - int(h * 0.40),
          int(h * 0.22), int(h * 0.26))
    for sx, sy, sr in ((0.30, 0.24, 0.08), (0.36, 0.16, 0.10),
                       (0.67, 0.28, 0.07)):
        r = int(h * sr)
        cx, cy = x + int(w * sx), y + int(h * sy)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 90, 90))


def scene_court(draw, x, y, w, h):
    """A courthouse: columns, a gavel and the scales of justice."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    # pediment
    draw.polygon([(x + int(w * 0.08), y + int(h * 0.30)),
                  (x + int(w * 0.92), y + int(h * 0.30)),
                  (x + int(w * 0.50), y + int(h * 0.08))], fill=(210, 202, 180))
    draw.rectangle([x + int(w * 0.08), y + int(h * 0.30),
                    x + int(w * 0.92), y + int(h * 0.36)], fill=(190, 180, 156))
    # three columns
    for cx in (0.16, 0.44, 0.72):
        draw.rectangle([x + int(w * cx), y + int(h * 0.38),
                        x + int(w * cx) + 34, y + int(h * 0.82)],
                       fill=(240, 236, 224))
        draw.rectangle([x + int(w * cx) - 6, y + int(h * 0.36),
                        x + int(w * cx) + 40, y + int(h * 0.40)],
                       fill=(200, 192, 170))
    draw.rectangle([x + int(w * 0.06), y + int(h * 0.82),
                    x + int(w * 0.94), y + int(h * 0.90)], fill=(170, 158, 132))
    # gavel on the steps: a clear head with two gold bands, handle right
    gx, gy = x + int(w * 0.42), y + int(h * 0.66)
    draw.rectangle([gx, gy, gx + 64, gy + 26], fill=(96, 64, 32))
    draw.rectangle([gx + 10, gy - 3, gx + 16, gy + 29], fill=GOLD)
    draw.rectangle([gx + 48, gy - 3, gx + 54, gy + 29], fill=GOLD)
    draw.rectangle([gx + 64, gy + 8, gx + 150, gy + 18], fill=(120, 82, 42))
    # scales of justice, larger, bottom right
    sx, sy = x + int(w * 0.86), y + int(h * 0.58)
    draw.line([(sx, sy - 30), (sx, sy + 30)], fill=GOLD, width=5)
    draw.line([(sx - 32, sy - 26), (sx + 32, sy - 26)], fill=GOLD, width=5)
    draw.polygon([(sx - 42, sy - 8), (sx - 16, sy - 8), (sx - 29, sy + 14)],
                 fill=GOLD)
    draw.polygon([(sx + 16, sy - 8), (sx + 42, sy - 8), (sx + 29, sy + 14)],
                 fill=GOLD)
    draw.ellipse([sx - 6, sy + 28, sx + 6, sy + 40], fill=GOLD)


def scene_markets(draw, x, y, w, h, f):
    """A plunging chart line, with the Dow's 50,000 milestone."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    # big red drop figure, top right
    label = "-6.2%"
    lw = draw.textlength(label, font=f["big_num_sm"])
    draw.text((x + w - lw - 14, y + 4), label, font=f["big_num_sm"],
              fill=RED)
    # chart frame
    cx0, cy0 = x + int(w * 0.08), y + int(h * 0.34)
    cx1, cy1 = x + int(w * 0.92), y + int(h * 0.88)
    draw.rectangle([cx0, cy0, cx1, cy1], outline=SOFT_INK, width=2)
    for gy in range(1, 4):
        yy = cy0 + (cy1 - cy0) * gy // 4
        draw.line([(cx0, yy), (cx1, yy)], fill=(200, 196, 184), width=1)
    # jagged line: rally, then a steep fall
    pts = []
    fracs = ((0.00, 0.30), (0.12, 0.22), (0.24, 0.26), (0.36, 0.16),
             (0.48, 0.20), (0.60, 0.44), (0.72, 0.62), (0.84, 0.72),
             (1.00, 0.86))
    for fx, fy in fracs:
        pts.append((cx0 + (cx1 - cx0) * fx, cy0 + (cy1 - cy0) * fy))
    draw.line(pts, fill=RED, width=5, joint="curve")
    # green milestone marker where the line peaked
    px, py = pts[3]
    draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=GREEN)
    draw.text((px + 12, py - 26), "DOW 50,000", font=f["source"], fill=GREEN)
    # down arrow at the end of the line
    ex, ey = pts[-1]
    draw.polygon([(ex - 12, ey - 22), (ex + 12, ey - 22), (ex, ey)],
                 fill=RED)


def scene_solomon(draw, x, y, w, h):
    """Pacific islands, a palm, and a signed treaty scroll."""
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    # sun and clouds
    draw.ellipse([x + int(w * 0.78), y + 10,
                  x + int(w * 0.78) + 52, y + 62], fill=(255, 244, 200))
    for cx, cy, cr in ((0.16, 0.14, 26), (0.24, 0.14, 20),
                       (0.46, 0.10, 22)):
        r = cr
        draw.ellipse([x + int(w * cx) - r, y + int(h * cy) - r // 2,
                      x + int(w * cx) + r, y + int(h * cy) + r // 2],
                     fill=(240, 246, 250))
    # two islands with sand and palms
    for ix, iy, iw in ((0.06, 0.62, 0.30), (0.60, 0.68, 0.34)):
        bx = x + int(w * ix)
        by = y + int(h * iy)
        draw.ellipse([bx, by, bx + int(w * iw), by + int(h * 0.22)],
                     fill=SAND)
        draw.ellipse([bx + int(w * iw * 0.14), by - int(h * 0.10),
                      bx + int(w * iw * 0.86), by + int(h * 0.14)],
                     fill=GREEN)
        # palm trunk and fronds
        tx = bx + int(w * iw * 0.5)
        ty = by - int(h * 0.06)
        draw.line([(tx, ty), (tx + 6, ty - int(h * 0.22))],
                  fill=(96, 64, 32), width=5)
        for dx, dy in ((-26, -8), (-18, -22), (0, -28), (18, -22), (26, -8)):
            draw.line([(tx + 6, ty - int(h * 0.22)),
                       (tx + 6 + dx, ty - int(h * 0.22) + dy)],
                      fill=GREEN, width=4)
    # treaty scroll, centre, with a red seal
    sx, sy = x + int(w * 0.36), y + int(h * 0.42)
    sw, sh = int(w * 0.28), int(h * 0.34)
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=(250, 246, 236),
                   outline=INK, width=2)
    for i in range(3):
        ly = sy + 18 + i * 16
        draw.line([(sx + 14, ly), (sx + sw - 14, ly)], fill=SOFT_INK,
                  width=2)
    draw.ellipse([sx + sw - 34, sy + sh - 34, sx + sw - 6, sy + sh - 6],
                 fill=RED)
    # small gold star on the seal
    burst(draw, sx + sw - 20, sy + sh - 20, 9, GOLD, spikes=5)


def scene_space(draw, x, y, w, h, f):
    """Shenzhou-24 climbing toward Tiangong under a starry sky.

    Everything is sized relative to the scene box so nothing spills
    past its bottom edge into the headline below.
    """
    draw.rectangle([x, y, x + w, y + h], fill=(8, 10, 28))
    for sx, sy in ((0.05, 0.10), (0.18, 0.05), (0.32, 0.14), (0.46, 0.06),
                   (0.60, 0.12), (0.74, 0.05), (0.88, 0.10), (0.95, 0.22),
                   (0.10, 0.26), (0.40, 0.24), (0.66, 0.26), (0.82, 0.28)):
        draw.ellipse([x + w * sx - 2, y + h * sy - 2,
                      x + w * sx + 2, y + h * sy + 2], fill=(240, 240, 220))
    # Earth's limb: a shallow arc hugging the bottom of the scene
    limb = [(x + w * t / 20,
             y + h * 0.99 - h * 0.16 * math.sin(math.pi * t / 20))
            for t in range(21)]
    limb += [(x + w, y + h), (x, y + h)]
    draw.polygon(limb, fill=(36, 90, 150))
    draw.line(limb[:-2], fill=(120, 190, 230), width=3)
    # Tiangong station, top right: core module + solar panels
    sx, sy = x + int(w * 0.64), y + int(h * 0.12)
    sw, sh = int(w * 0.10), max(10, int(h * 0.16))
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=(200, 200, 205))
    draw.rectangle([sx - int(w * 0.07), sy + sh // 4,
                    sx, sy + 3 * sh // 4], fill=(40, 90, 180))
    draw.rectangle([sx + sw, sy + sh // 4,
                    sx + sw + int(w * 0.07), sy + 3 * sh // 4],
                   fill=(40, 90, 180))
    draw.rectangle([sx + sw // 3, sy - max(6, int(h * 0.10)),
                    sx + 2 * sw // 3, sy], fill=(160, 160, 165))
    # rocket climbing, centre-left, flame below
    rw = max(16, int(h * 0.16))
    rx, ry = x + int(w * 0.28), y + int(h * 0.34)
    rh = int(h * 0.34)
    draw.rectangle([rx, ry, rx + rw, ry + rh], fill=(240, 240, 240))
    draw.polygon([(rx - 1, ry), (rx + rw // 2, ry - int(h * 0.14)),
                  (rx + rw + 1, ry)], fill=RED)
    draw.polygon([(rx - int(rw * 0.45), ry + rh), (rx, ry + rh - int(h * 0.10)),
                  (rx, ry + rh)], fill=RED)
    draw.polygon([(rx + rw, ry + rh), (rx + rw, ry + rh - int(h * 0.10)),
                  (rx + rw + int(rw * 0.45), ry + rh)], fill=RED)
    draw.ellipse([rx + rw // 4, ry + rh // 4,
                  rx + 3 * rw // 4, ry + rh // 2], fill=BLUE)
    flame(draw, rx + rw // 2, ry + rh + 2, max(18, int(h * 0.20)),
          max(16, int(h * 0.16)))
    # dashed path from rocket nose to the station
    px, py = rx + rw // 2, ry - int(h * 0.18)
    ex, ey = sx + sw // 2, sy + sh + 4
    steps = 12
    for i in range(steps):
        if i % 2 == 0:
            t0, t1 = i / steps, (i + 0.5) / steps
            draw.line([(px + (ex - px) * t0, py + (ey - py) * t0),
                       (px + (ex - px) * t1, py + (ey - py) * t1)],
                      fill=(255, 220, 120), width=3)


# ---------------------------------------------------------------- panels
def panel(draw, box, f, story, scene_frac=0.32):
    """One story panel: scene on top, kicker + headline + deck below."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    scene_h = int(h * scene_frac)
    story["scene"](draw, x + 2, y + 2, w - 4, scene_h - 2)
    draw.line([(x, y + scene_h), (x + w, y + scene_h)], fill=INK, width=2)
    tx = x + 20
    ty = y + scene_h + 12
    tw = w - 40
    draw.text((tx, ty), story["kicker"], font=f["kicker"], fill=story["accent"])
    ty += 30
    hl_font = f["headline_sm"] if len(story["headline"]) > 46 else f["headline"]
    hl_lead = 42 if hl_font is f["headline"] else 38
    ty = text_block(draw, (tx, ty),
                    wrap(draw, story["headline"], hl_font, tw),
                    hl_font, INK, hl_lead)
    ty += 4
    # never let the deck run into the source line: trim to the space left
    deck_bottom = y + h - 36
    max_deck_lines = max(1, (deck_bottom - ty) // 28)
    deck_lines = wrap(draw, story["deck"], f["deck_sm"], tw)[:max_deck_lines]
    text_block(draw, (tx, ty), deck_lines, f["deck_sm"], SOFT_INK, 28)
    draw.text((tx, y + h - 30), story["source"], font=f["source"],
              fill=SOFT_INK)


STORIES = [
    dict(kicker="THE STRAIT OF HORMUZ", accent=RED, scene=scene_hormuz,
         headline="Iran says two tankers hit mines and catch fire in Hormuz",
         deck="Tehran says the tankers struck naval mines on an unauthorised "
              "route and exploded; the claim is unconfirmed independently.",
         source="Reuters \u00b7 25 Nov 2026"),
    dict(kicker="UKRAINE \u00b7 POLAND", accent=RED, scene=scene_refinery,
         headline="Ukraine hits two Russian refineries; Poland plans no-fly zone",
         deck="Drones set the Syzran and Kuibyshev refineries ablaze "
              "overnight; Warsaw moves to close its eastern border skies.",
         source="The Kyiv Independent / NY Post \u00b7 25 Nov 2026"),
    dict(kicker="U.S. COURTS \u00b7 TECH", accent=BLUE, scene=scene_court,
         headline="Huawei convicted on 10 of 12 counts in U.S. trial",
         deck="A Brooklyn jury finds the telecom giant guilty of bank fraud, "
              "sanctions violations and stealing trade secrets.",
         source="CNN / Wall Street Journal \u00b7 25 Nov 2026"),
    dict(kicker="MARKETS", accent=RED, scene=None,  # set below
         headline="Asian stocks plunge as the Dow tops 50,000 for the first time",
         deck="South Korea's KOSPI falls 6.2% as chip shares sink; Japan's "
              "Nikkei drops 2.8% \u2014 while the Dow closes at 50,018.70.",
         source="Associated Press \u00b7 25 Nov 2026"),
    dict(kicker="THE PACIFIC", accent=BLUE, scene=scene_solomon,
         headline="Solomon Islands signs security pact with Australia",
         deck="Canberra becomes Honiara's primary security partner; the "
              "treaty vows no foreign military base on its soil.",
         source="AP / Reuters \u00b7 25 Nov 2026"),
    dict(kicker="SPACE", accent=BLUE, scene=None,  # set below
         headline="Pakistan's first astronaut reaches China's Tiangong station",
         deck="Muhammad Zeeshan Ali flies aboard Shenzhou-24 and docks with "
              "Tiangong \u2014 the first foreign visitor to the station.",
         source="Nature / Reuters \u00b7 25 Nov 2026"),
]


def markets_scene(draw, x, y, w, h):
    scene_markets(draw, x, y, w, h, fonts())


def space_scene(draw, x, y, w, h):
    scene_space(draw, x, y, w, h, fonts())


STORIES[3]["scene"] = markets_scene
STORIES[5]["scene"] = space_scene


# ---------------------------------------------------------------- compose
def compose():
    f = fonts()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # outer double border
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    draw.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # masthead
    title = "THE WORLD IN ONE IMAGE"
    tw = draw.textlength(title, font=f["masthead"])
    draw.text(((W - tw) / 2, 40), title, font=f["masthead"], fill=INK)
    rule(draw, 158, MARGIN, W - MARGIN, 4)
    date = DATE_LINE + "  \u00b7  SIX STORIES THAT DEFINED THE DAY"
    dw = draw.textlength(date, font=f["masthead_small"])
    draw.text(((W - dw) / 2, 168), date, font=f["masthead_small"],
              fill=SOFT_INK)
    rule(draw, 212, MARGIN, W - MARGIN, 2)

    # hero: the Hormuz story, full width
    hero = (MARGIN, 226, W - 2 * MARGIN, 320)
    panel(draw, hero, f, STORIES[0], scene_frac=0.34)

    # two rows of two panels
    gap = 14
    col_w = (W - 2 * MARGIN - gap) // 2
    row1_y, row_h = 560, 320
    panel(draw, (MARGIN, row1_y, col_w, row_h), f, STORIES[1])
    panel(draw, (MARGIN + col_w + gap, row1_y, col_w, row_h), f, STORIES[2])
    row2_y = row1_y + row_h + gap
    panel(draw, (MARGIN, row2_y, col_w, row_h), f, STORIES[3])
    panel(draw, (MARGIN + col_w + gap, row2_y, col_w, row_h), f, STORIES[4])

    # bottom wide panel: Shenzhou-24
    bottom = (MARGIN, row2_y + row_h + gap, W - 2 * MARGIN, 268)
    panel(draw, bottom, f, STORIES[5], scene_frac=0.34)

    # footer, centred line by line so it never runs off the page
    fy = bottom[1] + bottom[3] + 14
    rule(draw, fy, MARGIN, W - MARGIN, 2)
    fy += 12
    for line in wrap(draw, FOOTER, f["footer"], W - 2 * MARGIN - 40):
        lw = draw.textlength(line, font=f["footer"])
        draw.text(((W - lw) / 2, fy), line, font=f["footer"], fill=SOFT_INK)
        fy += 29
    note = "Drawn from verified reporting \u00b7 Built by an AI agent for make.fun"
    nw = draw.textlength(note, font=f["footer"])
    draw.text(((W - nw) / 2, fy + 4), note, font=f["footer"], fill=SOFT_INK)

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = "./output"
        os.makedirs(out_dir, exist_ok=True)
    img = compose()
    small = img.resize((OUT, OUT), Image.LANCZOS)
    path = os.path.join(out_dir, "entry.png")
    small.save(path, format="PNG")
    print("wrote", path, small.size)


if __name__ == "__main__":
    main()
