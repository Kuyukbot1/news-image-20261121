#!/usr/bin/env python3
"""Draw the 21 November 2026 front page: 42 verified stories, 1024x1024 PNG.
Written fresh for news-image-20261121. Uses only the Python standard library
plus Pillow (build-time drawing); the shipped entry.png is drawn by this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
NAVY = (27, 58, 107)
RED = (164, 30, 34)
GOLD = (178, 134, 11)
TEAL = (14, 94, 94)
GREY = (90, 86, 78)
CARD_BG = (255, 253, 247)
RULE = (180, 172, 152)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, fill, spacing=2, max_lines=None):
    lines = wrap(draw, s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += f.size + spacing
    return y


def centre(draw, cx, y, s, f, fill):
    draw.text((cx - text_w(draw, s, f) / 2, y), s, font=f, fill=fill)


# ---------------------------------------------------------------- world map
# Simplified continent outlines in (lon, lat), equirectangular projection.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 68), (-95, 69),
     (-90, 73), (-82, 66), (-78, 62), (-72, 62), (-65, 60), (-60, 55),
     (-55, 47), (-60, 45), (-66, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-94, 18), (-97, 16),
     (-105, 20), (-110, 23), (-114, 28), (-117, 32), (-122, 37), (-124, 42),
     (-124, 48), (-130, 54), (-140, 60), (-152, 58), (-158, 56), (-165, 60),
     (-168, 66)],
    # Greenland
    [(-58, 64), (-52, 60), (-43, 60), (-32, 68), (-22, 70), (-30, 74),
     (-45, 76), (-58, 76), (-62, 70), (-58, 64)],
    # South America
    [(-79, 9), (-77, 8), (-72, 12), (-64, 10), (-59, 8), (-52, 5), (-51, 0),
     (-44, -3), (-35, -8), (-39, -15), (-40, -21), (-48, -27), (-53, -33),
     (-58, -38), (-63, -41), (-66, -47), (-68, -52), (-70, -55), (-73, -50),
     (-73, -42), (-72, -35), (-71, -28), (-70, -18), (-76, -13), (-80, -5),
     (-81, 0), (-80, 5), (-79, 9)],
    # Africa
    [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-6, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (25, 32), (30, 31), (32, 31), (35, 28), (37, 22),
     (39, 18), (43, 12), (48, 11), (51, 11), (51, 2), (46, -1), (41, -4),
     (40, -10), (36, -18), (35, -22), (32, -28), (28, -33), (25, -34),
     (19, -35), (16, -29), (14, -22), (12, -17), (13, -12), (12, -6),
     (9, -1), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 49),
     (2, 51), (5, 53), (8, 57), (10, 59), (12, 56), (18, 56), (21, 55),
     (24, 58), (26, 60), (30, 62), (30, 66), (32, 70), (40, 68), (48, 68),
     (55, 69), (62, 70), (70, 72), (78, 72), (85, 74), (95, 76), (105, 77),
     (115, 73), (125, 72), (135, 72), (145, 72), (155, 70), (162, 68),
     (170, 67), (178, 65), (173, 64), (170, 60), (162, 58), (158, 52),
     (156, 50), (150, 59), (142, 54), (141, 45), (140, 39), (135, 35),
     (132, 33), (129, 32), (127, 35), (126, 38), (122, 39), (120, 35),
     (119, 30), (116, 23), (110, 20), (108, 18), (106, 10), (104, 9),
     (101, 7), (99, 10), (98, 13), (96, 16), (93, 17), (91, 22), (89, 22),
     (87, 21), (85, 19), (82, 17), (80, 14), (78, 8), (76, 9), (74, 13),
     (72, 20), (70, 22), (66, 25), (62, 25), (58, 26), (56, 27), (52, 28),
     (50, 29), (48, 30), (47, 30), (44, 29), (42, 29), (39, 28), (38, 24),
     (36, 27), (35, 29), (34, 31), (35, 33), (36, 36), (33, 36), (30, 36),
     (27, 37), (26, 38), (23, 36), (22, 37), (19, 40), (16, 40), (14, 42),
     (12, 44), (10, 44), (8, 44), (6, 43), (3, 43), (0, 40), (-2, 37),
     (-6, 36), (-9, 37), (-10, 36)],
    # Indonesia / New Guinea band
    [(95, 5), (98, 4), (100, 0), (102, -2), (105, -6), (108, -7), (112, -7),
     (115, -8), (118, -9), (120, -10), (123, -10), (126, -8), (128, -6),
     (131, -3), (131, -1), (135, -2), (138, -3), (141, -3), (144, -4),
     (147, -6), (150, -8), (147, -9), (144, -8), (141, -8), (137, -7),
     (134, -4), (131, -2), (128, 1), (125, 2), (122, 0), (119, 1), (116, 1),
     (113, -1), (110, -6), (107, -7), (104, -5), (101, -1), (98, 2), (95, 5)],
    # Australia
    [(113, -22), (114, -28), (115, -32), (115, -35), (118, -35), (122, -34),
     (126, -32), (129, -32), (132, -32), (135, -35), (137, -35), (140, -38),
     (144, -38), (147, -39), (150, -37), (153, -32), (153, -27), (151, -24),
     (149, -20), (146, -19), (143, -15), (142, -11), (141, -13), (137, -12),
     (135, -12), (133, -12), (131, -12), (129, -14), (126, -14), (123, -16),
     (120, -19), (117, -20), (113, -22)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 58), (0, 57), (1, 53),
     (1, 51), (-2, 51), (-5, 50)],
    # Japan
    [(130, 31), (131, 33), (133, 34), (135, 34), (137, 35), (139, 36),
     (139, 38), (140, 39), (141, 41), (142, 42), (144, 43), (145, 44),
     (143, 44), (141, 43), (140, 41), (139, 38), (137, 36), (135, 35),
     (133, 34), (131, 32), (130, 31)],
    # New Zealand
    [(167, -45), (168, -44), (170, -43), (172, -41), (174, -39), (176, -38),
     (178, -37), (177, -39), (175, -40), (174, -41), (172, -42), (170, -43),
     (168, -45), (167, -46), (166, -46), (167, -45)],
]

PIN_LONLAT = [
    (-77.0, 38.9), (56.5, 26.5), (12.6, 55.7), (19.4, 52.2), (2.35, 48.85),
    (-74.0, 40.7), (77.4, 23.3), (72.9, 19.1), (174.8, -41.3), (44.2, 32.9),
    (-80.2, 25.8), (-84.1, 9.9), (36.8, -1.3),
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (84.0 - lat) / 142.0 * (y1 - y0)
    return x, y


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 230, 238), outline=RULE, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        draw.polygon(pts, fill=(196, 178, 138), outline=(120, 108, 82))
    # graticule
    for lon in range(-150, 181, 30):
        xa, _ = project(lon, 84, box)
        xb, _ = project(lon, -58, box)
        draw.line([(xa, y0), (xb, y1)], fill=(190, 205, 214), width=1)
    for n, (lon, lat) in enumerate(PIN_LONLAT, start=1):
        px, py = project(lon, lat, box)
        # offset badges that would otherwise overlap (Washington / New York)
        off = {1: (-14, -12), 6: (14, -12)}.get(n, (0, 0))
        bx, by = px + off[0], py + off[1]
        if off != (0, 0):
            draw.line([(px, py), (bx, by)], fill=RED, width=1)
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        r = 8
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        f = font(SANS_B, 10)
        tw = text_w(draw, str(n), f)
        draw.text((bx - tw / 2, by - 6), str(n), font=f, fill=(255, 255, 255))


# ------------------------------------------------------- flat illustrations
def illu(draw, kind, x, y, w, h):
    """Small flat illustration of the actual event, inside box (x,y,w,h).
    All coordinates are fractions of h so 40px and 62px bands both work."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 224, 203))
    cx, cy = x + w / 2, y + h / 2
    if kind == "summit":
        # table with three flags: US, China, Russia
        ty = y + h * 0.72
        draw.rectangle([x + 8, ty, x + w - 8, ty + 6], fill=(120, 84, 50))
        for i, cols in enumerate([[(180, 30, 40), (255, 255, 255), (27, 58, 107)],
                                  [(200, 30, 30), (255, 220, 0)],
                                  [(255, 255, 255), (27, 58, 107), (200, 30, 30)]]):
            fx = x + 14 + i * (w - 28) / 3
            draw.line([(fx, y + h * 0.10), (fx, ty)], fill=INK, width=2)
            for j, c in enumerate(cols):
                draw.rectangle([fx, y + h * 0.12 + j * h * 0.11,
                                fx + 22, y + h * 0.12 + (j + 1) * h * 0.11], fill=c)
    elif kind == "missiles":
        draw.rectangle([x, y + h - 6, x + w, y + h], fill=(27, 58, 107))
        for mx, my, s in [(x + w * 0.3, y + h * 0.35, 1), (x + w * 0.7, y + h * 0.5, -1)]:
            draw.line([(mx, my), (mx + s * 16, my - h * 0.22)], fill=INK, width=3)
            draw.polygon([(mx + s * 16, my - h * 0.22), (mx + s * 22, my - h * 0.16),
                          (mx + s * 16, my - h * 0.10)], fill=RED)
        for ex, ey in [(x + w * 0.55, y + h * 0.3), (x + w * 0.82, y + h * 0.62)]:
            for r, c in [(8, (255, 180, 0)), (4, (255, 90, 0))]:
                draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=c)
    elif kind == "spy":
        # magnifier over a silhouette, Danish flag
        draw.rectangle([x + w - 30, y + 4, x + w - 6, y + h * 0.32], fill=(200, 30, 30))
        draw.line([(x + w - 30, y + h * 0.18), (x + w - 6, y + h * 0.18)],
                  fill=(255, 255, 255), width=2)
        draw.line([(x + w - 18, y + 4), (x + w - 18, y + h * 0.32)],
                  fill=(255, 255, 255), width=2)
        draw.ellipse([x + 10, y + h * 0.10, x + 42, y + h * 0.10 + 32],
                     outline=INK, width=4)
        draw.line([(x + 38, y + h * 0.10 + 28), (x + 52, y + h - 4)],
                  fill=INK, width=4)
        draw.ellipse([cx - 11, y + h - 14, cx + 11, y + h - 2], fill=NAVY)
        draw.ellipse([cx - 5, y + h - 24, cx + 5, y + h - 14], fill=NAVY)
    elif kind == "blast":
        for r, c in [(h * 0.38, (255, 180, 0)), (h * 0.26, (255, 90, 0)),
                     (h * 0.13, (120, 30, 30))]:
            draw.ellipse([cx - r, cy - h * 0.12 - r, cx + r, cy - h * 0.12 + r],
                         fill=c)
        draw.rectangle([x + 8, y + h - 6, x + w - 8, y + h - 2], fill=(90, 90, 90))
        for bx in [x + 16, x + w // 2 - 4, x + w - 24]:
            draw.rectangle([bx, y + h - 14, bx + 8, y + h - 6], fill=(70, 70, 70))
    elif kind == "court":
        draw.polygon([(x + 8, y + h * 0.86), (x + w - 8, y + h * 0.86),
                      (cx, y + h * 0.10)], fill=(120, 84, 50))
        for i in range(4):
            px = x + 16 + i * (w - 32) / 3
            draw.rectangle([px - 3, y + h * 0.36, px + 3, y + h * 0.86],
                           fill=(240, 236, 224))
        draw.rectangle([x + 8, y + h * 0.86, x + w - 8, y + h * 0.92],
                       fill=(90, 70, 50))
    elif kind == "chart":
        draw.rectangle([x + 8, y + h * 0.80, x + w - 8, y + h * 0.86],
                       fill=(120, 120, 120))
        pts = [(x + 10, y + h * 0.18), (x + w * 0.3, y + h * 0.26),
               (x + w * 0.5, y + h * 0.20), (x + w * 0.7, y + h * 0.48),
               (x + w - 10, y + h * 0.74)]
        draw.line(pts, fill=RED, width=3)
        draw.polygon([(x + w - 16, y + h * 0.66), (x + w - 4, y + h * 0.74),
                      (x + w - 16, y + h * 0.82)], fill=RED)
        draw.text((x + 8, y + h * 0.30), "-9%", font=font(SANS_B, 13), fill=RED)
    elif kind == "vaccine":
        # syringe + egg
        draw.line([(x + 12, y + h - 6), (x + w - 22, y + h * 0.22)],
                  fill=(120, 120, 120), width=5)
        draw.polygon([(x + w - 22, y + h * 0.22), (x + w - 8, y + h * 0.16),
                      (x + w - 22, y + h * 0.34)], fill=(180, 180, 180))
        draw.ellipse([x + w - 34, y + h - 24, x + w - 10, y + h - 2],
                     fill=(240, 230, 200), outline=(180, 160, 110), width=2)
        draw.ellipse([x + 12, y + h * 0.16, x + 26, y + h * 0.16 + 14],
                     fill=(14, 94, 94))
    elif kind == "exchange":
        draw.rectangle([x + 10, y + h * 0.78, x + w - 10, y + h * 0.92],
                       fill=NAVY)
        for i in range(4):
            px = x + 18 + i * (w - 36) / 3
            draw.rectangle([px - 3, y + h * 0.28, px + 3, y + h * 0.78],
                           fill=(240, 236, 224))
        draw.polygon([(x + 6, y + h * 0.28), (x + w - 6, y + h * 0.28),
                      (cx, y + h * 0.08)], fill=GOLD)
        bars = [0.18, 0.28, 0.22, 0.38, 0.48]
        for i, bf in enumerate(bars):
            bx = x + w - 52 + i * 9
            draw.rectangle([bx, y + h * 0.92 - h * bf, bx + 6, y + h * 0.92],
                           fill=(14, 94, 94))
    elif kind == "cricket":
        for i in range(3):
            sx = x + 14 + i * 7
            draw.rectangle([sx, y + h * 0.30, sx + 3, y + h - 4],
                           fill=(200, 170, 90))
        draw.rectangle([x + 14, y + h * 0.26, x + 31, y + h * 0.30],
                       fill=(200, 170, 90))
        draw.line([(x + w - 40, y + h * 0.16), (x + w - 14, y + h - 8)],
                  fill=(150, 110, 60), width=6)
        draw.ellipse([x + w - 30, y + h - 22, x + w - 18, y + h - 10],
                     fill=RED)
        draw.arc([x + 8, y + h * 0.10, x + 60, y + h * 0.75], 200, 340,
                 fill=TEAL, width=3)
    elif kind == "convoy":
        draw.rectangle([x, y + h - 8, x + w, y + h], fill=(150, 140, 110))
        for vx in [x + 10, x + w // 2 - 8, x + w - 34]:
            draw.rectangle([vx, y + h - 22, vx + 26, y + h - 8],
                           fill=(90, 100, 70))
            draw.ellipse([vx + 4, y + h - 12, vx + 10, y + h - 6], fill=INK)
            draw.ellipse([vx + 16, y + h - 12, vx + 22, y + h - 6], fill=INK)
        draw.rectangle([x + w - 40, y + h * 0.14, x + w - 12, y + h * 0.42],
                       fill=(180, 160, 120))
        draw.polygon([(x + w - 42, y + h * 0.14), (x + w - 10, y + h * 0.14),
                      (x + w - 26, y + h * 0.04)], fill=(150, 110, 60))
    elif kind == "game":
        draw.rectangle([x, y + h - 8, x + w, y + h], fill=(27, 58, 107))
        draw.ellipse([x + w - 34, y + h * 0.08, x + w - 10, y + h * 0.08 + 24],
                     fill=(255, 180, 0))
        for bx, bf in [(x + 8, 0.40), (x + 24, 0.60), (x + 42, 0.50),
                       (x + 58, 0.70)]:
            bh = h * bf
            draw.rectangle([bx, y + h - 8 - bh, bx + 14, y + h - 8],
                           fill=(40, 40, 60))
            for wy in range(3):
                draw.rectangle([bx + 3, y + h - 12 - bh + wy * h * 0.16,
                                bx + 11, y + h - 8 - bh + wy * h * 0.16 + 3],
                               fill=(255, 220, 100))
        draw.line([(x + w - 52, y + h * 0.22), (x + w - 44, y + h * 0.48)],
                  fill=(14, 94, 94), width=3)
        draw.line([(x + w - 52, y + h * 0.48), (x + w - 44, y + h * 0.22)],
                  fill=(14, 94, 94), width=3)
    elif kind == "un":
        draw.rectangle([cx - 22, y + h * 0.16, cx + 22, y + h - 6],
                       fill=(90, 140, 180))
        for ry in range(5):
            draw.rectangle([cx - 20, y + h * 0.20 + ry * h * 0.14,
                            cx + 20, y + h * 0.20 + ry * h * 0.14 + 3],
                           fill=(220, 230, 240))
        draw.ellipse([x + 8, y + h - 22, x + 32, y + h - 2], fill=TEAL)
        draw.line([(x + 8, y + h - 12), (x + 32, y + h - 12)],
                  fill=(255, 255, 255), width=1)
    elif kind == "scales":
        draw.line([(cx, y + h * 0.10), (cx, y + h - 8)], fill=INK, width=3)
        draw.line([(cx - 22, y + h * 0.22), (cx + 22, y + h * 0.22)],
                  fill=INK, width=3)
        for sx in [cx - 22, cx + 22]:
            draw.line([(sx, y + h * 0.22), (sx, y + h * 0.40)], fill=INK, width=2)
            draw.polygon([(sx - 10, y + h * 0.40), (sx + 10, y + h * 0.40),
                          (sx, y + h * 0.62)], outline=INK, width=2)
        draw.rectangle([cx - 14, y + h - 8, cx + 14, y + h - 4], fill=INK)


# ------------------------------------------------------------------- stories
# (headline, deck, kicker, illustration kind) — 13 numbered features.
FEATURES = [
    ("Trump: Iran wants a deal, but not one I will accept",
     "Araghchi says Tehran still hopes diplomacy can end the war.",
     "US \u00b7 IRAN WAR", "summit"),
    ("Coalition downs Houthi missiles over the Gulf",
     "Kuwait and Bahrain face new Iranian attacks after the Qeshm strike.",
     "GULF \u00b7 IRAN WAR", "missiles"),
    ("Denmark expels Russian attache over rapper plot",
     "PET says Moscow planned to kill Kyivstoner with a banned gang's help.",
     "EUROPE \u00b7 ESPIONAGE", "spy"),
    ("Russian missile hits Poland during drill",
     "Eight killed in Ukraine strikes after bridge attack.",
     "EUROPE \u00b7 UKRAINE WAR", "blast"),
    ("Paris jails three police over Zecler beating",
     "Racism an aggravating factor; lifetime police bans.",
     "EUROPE \u00b7 JUSTICE", "court"),
    ("Anthropic falls 9% after record IPO",
     "Tech slide follows a debut that briefly topped $2tn.",
     "GLOBAL \u00b7 MARKETS", "chart"),
    ("India's first home-grown H5N1 vaccine",
     "At 1\u20132 rupees a dose; new 300-crore lab in Bhopal.",
     "ASIA \u00b7 HEALTH", "vaccine"),
    ("NSE becomes world's 5th-largest exchange",
     "India's bourse passes Nasdaq and HKEX at $59.7bn.",
     "ASIA \u00b7 MARKETS", "exchange"),
    ("Jaiswal and Rahul put India on top",
     "130-run stand \u2014 India's first in NZ this century.",
     "OCEANIA \u00b7 SPORT", "cricket"),
    ("Iraq moves into Kataib Hezbollah stronghold",
     "Federal police take over Jurf al-Sakhar after a deal.",
     "MIDDLE EAST \u00b7 IRAQ", "convoy"),
    ("GTA VI rakes in $3.79bn on day one",
     "Record Leonida launch; staff face uncertain future.",
     "GLOBAL \u00b7 CULTURE", "game"),
    ("Two veto powers block Grynspan's UN bid",
     "Frontrunner takes 10 for, 4 against in informal poll.",
     "GLOBAL \u00b7 DIPLOMACY", "un"),
    ("Kenya's courts face 580,000-case backlog",
     "'Justice delayed' leads Saturday's papers.",
     "AFRICA \u00b7 JUSTICE", "scales"),
]

# (country label, one-line item) — also-on items 14..42.
ALSO_ON = [
    ("US", "Nvidia's Huang agrees to testify at a public Senate hearing."),
    ("Ukraine", "EU approves a 1bn euro package of military equipment."),
    ("Ukraine", "EU releases a record 7.9bn euro payment to Kyiv."),
    ("EU", "ambassadors set to clear final Ukraine accession clusters."),
    ("Gaza", "Israeli airstrike hits the Bureij refugee camp."),
    ("Gaza", "WHO chief demands unrestricted entry of aid."),
    ("Iran", "Pezeshkian calls for energy subsidy reform amid war strain."),
    ("Iran", "US targets ship-to-ship transfers; Tehran mulls a flotilla."),
    ("US", "Trump defends Putin ties, says AI data centres must stay in US."),
    ("US", "Melania Trump says her Christmas wish is another ceasefire."),
    ("US", "Trump says close to a Mexico deal, more work with Canada."),
    ("Chile/Philippines", "free-trade pact signed at the APEC summit."),
    ("India", "Sensex rallies 898 pts to 83,919.71."),
    ("India", "Supreme Court rejects Tamil Nadu's Cauvery water plea."),
    ("US", "Indian man jailed 19+ years in plot to kill a Sikh leader."),
    ("India", "Nepal PM Balendra Shah to visit India on 22\u201323 Nov."),
    ("India", "cheetah at Kuno gives birth to four cubs."),
    ("India", "Japanese forces to use Indian facilities for live-fire drills."),
    ("India", "DGCA show-cause notice to SpiceJet over cancellations."),
    ("India", "foreign investors pump a record 1.01 lakh crore in November."),
    ("India", "Cyclone Akvan weakens into a deep depression."),
    ("Global", "COP31 talks spill into overtime in a fossil-fuel row."),
    ("Australia", "Hazlewood hints at quitting if Cummins loses captaincy."),
    ("Kenya", "report warns gangs could destabilise the 2027 election."),
    ("Tanzania", "new constitution promised by 2029, President Samia says."),
    ("US", "Treasury presses Singapore, Malaysia on Iran sanctions."),
    ("Myanmar", "rights groups seek action after the ICJ Rohingya ruling."),
    ("UN", "warns global hunger is growing as food-aid funding runs short."),
    ("Thailand", "five Cambodians caught crossing the border through a possible minefield."),
]


def draw_card(draw, x, y, w, h, num, headline, deck, kicker, kind, big):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=RULE, width=1)
    ih = 62 if big else 40
    illu(draw, kind, x + 1, y + 1, w - 2, ih)
    # number badge
    r = 11 if big else 10
    bx, by = x + 6 + r, y + ih + 6 + r
    draw.ellipse([bx - r, by - r, bx + r, by + r], fill=RED)
    fnum = font(SANS_B, 13 if big else 11)
    tw = text_w(draw, str(num), fnum)
    draw.text((bx - tw / 2, by - (7 if big else 6)), str(num), font=fnum,
              fill=(255, 255, 255))
    tx = x + 6 + 2 * r + 6
    ty = y + ih + 5
    fk = font(SANS_B, 11 if big else 9)
    draw.text((tx, ty), kicker, font=fk, fill=RED)
    ty += fk.size + 3
    fh = font(SANS_B, 15 if big else 12)
    ty = draw_wrapped(draw, tx, ty, headline, fh, w - (tx - x) - 6, INK,
                      spacing=1, max_lines=2)
    ty += 1
    fd = font(SANS, 11 if big else 10)
    draw_wrapped(draw, tx, ty, deck, fd, w - (tx - x) - 6, (60, 58, 52),
                 spacing=1, max_lines=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    # ---- masthead
    d.rectangle([M, 10, W - M, 12], fill=INK)
    centre(d, W // 2, 18, "T H E   D A Y   I N   W O R L D   N E W S",
           font(SANS_B, 15), NAVY)
    centre(d, W // 2, 40, "SATURDAY 21 NOVEMBER 2026",
           font(SERIF_B, 54), INK)
    centre(d, W // 2, 102, "42 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE DAY",
           font(SANS_B, 15), RED)
    d.rectangle([M, 124, W - M, 126], fill=INK)
    d.rectangle([M, 128, W - M, 130], fill=INK)
    # ---- features
    y = 138
    # row 1: 3 big cards
    cw = (W - 2 * M - 2 * 8) // 3
    ch = 158
    for i in range(3):
        hd, dk, kk, kind = FEATURES[i]
        draw_card(d, M + i * (cw + 8), y, cw, ch, i + 1, hd, dk, kk, kind, True)
    y += ch + 8
    # rows 2-3: 5 small cards each
    cw2 = (W - 2 * M - 4 * 8) // 5
    ch2 = 118
    for row in range(2):
        for j in range(5):
            i = 3 + row * 5 + j
            hd, dk, kk, kind = FEATURES[i]
            draw_card(d, M + j * (cw2 + 8), y, cw2, ch2, i + 1, hd, dk, kk,
                      kind, False)
        y += ch2 + 8
    # ---- map
    centre(d, W // 2, y, "W H E R E   I T   H A P P E N E D",
           font(SANS_B, 14), NAVY)
    y += 22
    draw_map(d, (M, y, W - M, y + 132))
    y += 132 + 8
    # ---- also on
    centre(d, W // 2, y, "A L S O   O N   S A T U R D A Y   2 1   N O V E M B E R",
           font(SANS_B, 14), NAVY)
    y += 22
    fnum = font(SANS_B, 11)
    fct = font(SANS_B, 11)
    ftxt = font(SANS, 11)
    col_w = (W - 2 * M - 24) // 2
    half = 15
    line_h = 15
    for col in range(2):
        cx0 = M + col * (col_w + 24)
        for k in range(half if col == 0 else len(ALSO_ON) - half):
            idx = col * half + k
            country, item = ALSO_ON[idx]
            ly = y + k * line_h
            num = str(14 + idx)
            d.text((cx0, ly), num + ".", font=fnum, fill=RED)
            nx = cx0 + text_w(d, num + ". ", fnum)
            d.text((nx, ly), country + ": ", font=fct, fill=INK)
            nx += text_w(d, country + ": ", fct)
            d.text((nx, ly), item, font=ftxt, fill=(40, 38, 34))
    y += half * line_h + 8
    # ---- footer
    d.rectangle([M, y, W - M, y + 1], fill=RULE)
    y += 6
    centre(d, W // 2, y,
           "Every story happened or was first reported on Saturday 21 November 2026; "
           "disputed claims are attributed.",
           font(SANS, 10), GREY)
    centre(d, W // 2, y + 14,
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, Le Monde, NDTV, ANI, PIB. "
           "Original drawings.",
           font(SANS, 10), GREY)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
