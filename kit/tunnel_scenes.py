"""Scenes for 'The $70 Million Tunnel Heist' in the cinematic silhouette style."""
import os
import random
import sys
from PIL import ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from real import Scene, p, pts, mix, FONT, FONT_R  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "tunnel")
os.makedirs(OUT, exist_ok=True)
WARM = (255, 196, 120)
COOL = (150, 180, 230)


def text(s, x, y, t, size=30, fill=(236, 230, 214), bold=True, anchor="la"):
    s.d.text((p(x), p(y)), t, font=ImageFont.truetype(FONT if bold else FONT_R, p(size)), fill=fill, anchor=anchor)


# ------------------------------------------------------------------ backgrounds
def vault(s, hole=True, pallets=0, light=(110, 104, 88)):
    s.grad((46, 50, 58), (30, 33, 40), 0, 640)
    for x in range(0, 1920, 160):                       # steel wall panels
        s.line([(x, 0), (x, 640)], (36, 39, 46), 5)
    for y in (160, 400):
        s.line([(0, y), (1920, y)], (36, 39, 46), 4)
    for cx in range(120, 760, 104):                     # deposit drawers, left
        for cy in range(210, 560, 78):
            s.rect(cx, cy, cx + 86, cy + 62, (58, 62, 70), outline=(30, 32, 38), width=3)
            s.ell(cx + 36, cy + 24, cx + 50, cy + 38, (120, 112, 90))
    s.poly([(0, 640), (1920, 640), (1920, 1080), (0, 1080)], (58, 60, 64))
    for i in range(1, 7):                               # floor seams in perspective
        y = 640 + i * i * 12
        s.line([(0, y), (1920, y)], (48, 50, 54), 3)
    for x in range(-600, 2600, 320):
        s.line([(960 + (x - 960) * .35, 640), (x, 1080)], (48, 50, 54), 3)
    s.rect(1500, 150, 1860, 640, (40, 43, 50), outline=(24, 26, 30), width=6)   # doorway
    s.beam([(1520, 170), (1840, 170), (1500, 1080), (900, 1080)], (58, 52, 38), 40)
    s.glow(960, 40, 520, 120, light, 90)
    if pallets:
        for k in range(pallets):
            bx = 300 + k * 330
            s.shade([bx - 30, 900, bx + 290, 960], 150, 14, ellipse=True)
            s.rect(bx, 890, bx + 260, 915, (92, 74, 50))
            for r in range(5):
                for c in range(5):
                    x0, y0 = bx + 6 + c * 50, 850 - r * 38
                    s.rect(x0, y0, x0 + 46, y0 + 34, (112, 132, 104), outline=(60, 76, 58), width=2)
                    s.rect(x0 + 17, y0, x0 + 29, y0 + 34, (206, 198, 170))
    if hole:
        s.shade([700, 800, 1220, 960], 140, 26, ellipse=True)
        s.ell(760, 822, 1160, 938, (8, 8, 10))
        s.ell(790, 840, 1130, 938, (2, 2, 3))
        random.seed(3)
        for _ in range(26):                             # rubble
            a = random.uniform(0, 6.28)
            import math
            rx, ry = 960 + math.cos(a) * random.uniform(215, 330), 880 + math.sin(a) * random.uniform(64, 110)
            w = random.uniform(10, 34)
            s.poly([(rx, ry), (rx + w, ry - w * .4), (rx + w * 1.3, ry + w * .3), (rx + w * .3, ry + w * .5)],
                   mix((92, 92, 94), (50, 52, 56), random.random()))


def palm(s, x, y, h, col):
    s.line([(x, y), (x + h * .06, y - h * .5), (x + h * .02, y - h)], col, max(6, h * .035))
    import math
    for a in (-2.6, -2.1, -1.6, -1.0, -.5, .1, 3.3):
        ex, ey = x + h * .02 + math.cos(a) * h * .42, y - h + math.sin(a) * h * .26 + h * .1
        s.line([(x + h * .02, y - h), ((x + ex) / 2, y - h - h * .1 + (ey - (y - h)) * .2), (ex, ey)], col, max(4, h * .02))


def street(s, mode="day", sign=True, pickup=False):
    T = {"day": ((150, 178, 204), (226, 214, 190), (214, 196, 160), (120, 116, 110), (30, 34, 30)),
         "dawn": ((70, 84, 120), (236, 170, 120), (150, 126, 110), (74, 72, 78), (18, 20, 24)),
         "night": ((10, 14, 30), (34, 42, 66), (44, 48, 62), (26, 28, 36), (8, 9, 12))}[mode]
    sky0, sky1, wall, road, sil = T
    s.grad(sky0, sky1, 0, 700)
    if mode == "dawn":
        s.glow(1500, 660, 520, 200, (120, 70, 30), 110)
    random.seed(5)
    x = 0
    while x < 1920:                                       # distant city
        w, h = random.randint(70, 150), random.randint(80, 240)
        s.rect(x, 640 - h, x + w, 640, mix(sky1, sil, .45))
        if mode == "night":
            for wy in range(640 - h + 14, 630, 26):
                for wx in range(x + 10, x + w - 12, 24):
                    if random.random() < .22:
                        s.rect(wx, wy, wx + 9, wy + 12, (190, 150, 80))
        x += w + random.randint(0, 20)
    # bank: big modern block on the right
    bank = mix(wall, (120, 120, 120), .35)
    s.rect(1180, 250, 1920, 760, bank)
    for cx in range(1220, 1920, 96):
        s.rect(cx, 290, cx + 34, 760, mix(bank, (0, 0, 0), .22))
        s.rect(cx + 44, 330, cx + 86, 720, mix((60, 80, 100), sil, .3 if mode != "night" else .8))
    s.rect(1160, 232, 1920, 262, mix(bank, (0, 0, 0), .35))
    s.rect(1320, 180, 1800, 236, mix(bank, (0, 0, 0), .45))
    text(s, 1560, 208, "BANCO CENTRAL", 30, mix((230, 226, 214), sil, .25 if mode != "night" else .6), anchor="mm")
    # house: small single-storey on the left
    hx = 150
    s.rect(hx, 520, hx + 560, 760, wall)
    s.poly([(hx - 30, 520), (hx + 590, 520), (hx + 520, 440), (hx + 40, 440)], mix((150, 84, 60), sil, .2 if mode == "day" else .6))
    s.rect(hx + 70, 600, hx + 180, 760, mix((84, 60, 44), sil, .2))
    s.rect(hx + 260, 590, hx + 470, 690, mix((60, 80, 100), sil, .35 if mode != "night" else .85))
    s.line([(hx + 365, 590), (hx + 365, 690)], mix(wall, (0, 0, 0), .4), 5)
    if sign:
        s.rect(hx + 230, 470, hx + 520, 540, (236, 232, 214) if mode == "day" else mix((236, 232, 214), sil, .5),
               outline=(40, 70, 44), width=5)
        text(s, hx + 375, 505, "GRAMA SINTÉTICA", 26, (40, 90, 50) if mode == "day" else (30, 50, 36), anchor="mm")
    s.rect(0, 760, 1920, 800, mix(road, (200, 200, 200), .25))        # pavement
    s.rect(0, 800, 1920, 1080, road)
    for lx in range(-40, 1920, 260):
        s.rect(lx, 930, lx + 130, 942, mix(road, (230, 220, 170), .6))
    palm(s, 880, 762, 330, sil)
    palm(s, 1050, 762, 250, sil)
    if pickup:
        truck(s, 560, 905, 1.0, mix((200, 200, 196), sil, .2 if mode == "day" else .7))


def truck(s, x, y, k, col, load=True):
    s.shade([x - 20 * k, y - 6 * k, x + 420 * k, y + 22 * k], 150, 10, ellipse=True)
    s.rect(x, y - 96 * k, x + 400 * k, y - 30 * k, col, r=10 * k)
    s.poly([(x + 230 * k, y - 96 * k), (x + 262 * k, y - 160 * k), (x + 352 * k, y - 160 * k), (x + 384 * k, y - 96 * k)], col)
    s.poly([(x + 246 * k, y - 100 * k), (x + 270 * k, y - 150 * k), (x + 344 * k, y - 150 * k), (x + 366 * k, y - 100 * k)], (70, 88, 104))
    if load:
        for i in range(4):
            s.ell(x + (14 + i * 52) * k, y - 132 * k, x + (74 + i * 52) * k, y - 88 * k, (104, 86, 60))
    for cx in (x + 78 * k, x + 316 * k):
        s.ell(cx - 34 * k, y - 62 * k, cx + 34 * k, y + 6 * k, (14, 14, 16))
        s.ell(cx - 14 * k, y - 42 * k, cx + 14 * k, y - 14 * k, (90, 90, 92))


def room(s):
    s.grad((70, 60, 50), (44, 38, 34), 0, 700)
    s.rect(1300, 170, 1640, 470, (150, 150, 130))                      # window
    s.line([(1470, 170), (1470, 470)], (40, 34, 30), 10)
    s.line([(1300, 320), (1640, 320)], (40, 34, 30), 10)
    s.poly([(0, 700), (1920, 700), (1920, 1080), (0, 1080)], (72, 56, 42))
    for x in range(-800, 2800, 150):
        s.line([(960 + (x - 960) * .4, 700), (x, 1080)], (58, 44, 34), 4)
    s.beam([(1300, 180), (1640, 180), (1200, 1080), (500, 1080)], (70, 60, 36), 50)
    s.ell(640, 800, 1180, 960, (10, 8, 7))                             # the hole
    s.ell(670, 826, 1150, 960, (3, 2, 2))
    for mx, my, mw in ((250, 900, 330), (1330, 930, 380), (90, 990, 260)):
        s.poly([(mx, my), (mx + mw * .5, my - mw * .42), (mx + mw, my)], (92, 68, 46))
        s.poly([(mx + mw * .5, my - mw * .42), (mx + mw, my), (mx + mw * .62, my)], (70, 52, 36))
    for sx_, sy_ in ((1560, 860), (1640, 880), (1500, 890)):
        s.ell(sx_ - 60, sy_ - 100, sx_ + 60, sy_, (126, 110, 84))
        s.rect(sx_ - 18, sy_ - 112, sx_ + 18, sy_ - 92, (96, 82, 62))
    s.line([(960, 0), (960, 150)], (20, 18, 16), 4)                    # bare bulb
    s.ell(946, 150, 974, 184, (255, 236, 180))
    s.glow(960, 190, 300, 220, (96, 74, 34), 80)


def cross(s, cars=True, lights=True, dusk=False):
    sky0, sky1 = ((60, 70, 110), (220, 150, 110)) if dusk else ((150, 178, 204), (220, 214, 196))
    s.grad(sky0, sky1, 0, 330)
    s.rect(120, 190, 430, 330, (206, 190, 158))                         # house
    s.poly([(100, 190), (450, 190), (410, 140), (140, 140)], (150, 84, 60))
    s.rect(1420, 60, 1880, 330, (150, 150, 146))                        # bank
    for cx in range(1450, 1860, 70):
        s.rect(cx, 90, cx + 40, 300, (104, 118, 132))
    text(s, 1650, 36, "BANCO CENTRAL", 24, (40, 40, 44), anchor="mm")
    text(s, 275, 118, "RENTED HOUSE", 22, (40, 40, 44), anchor="mm")
    s.rect(0, 330, 1920, 372, (70, 70, 74))                             # avenue surface
    for lx in range(470, 1400, 120):
        s.rect(lx, 348, lx + 60, 354, (220, 210, 160))
    if cars:
        for cx, col in ((560, (160, 60, 50)), (800, (60, 90, 130)), (1040, (200, 200, 196)), (1250, (70, 110, 80))):
            s.rect(cx, 296, cx + 150, 330, col, r=10)
            s.poly([(cx + 28, 298), (cx + 46, 268), (cx + 108, 268), (cx + 126, 298)], col)
            s.ell(cx + 18, 312, cx + 52, 346, (16, 16, 18))
            s.ell(cx + 98, 312, cx + 132, 346, (16, 16, 18))
    for i, (c0, c1, y0, y1) in enumerate((((104, 78, 54), (88, 64, 44), 372, 560), ((88, 64, 44), (66, 48, 34), 560, 800),
                                          ((66, 48, 34), (40, 30, 24), 800, 1080))):
        s.grad(c0, c1, y0, y1)
    random.seed(9)
    for _ in range(90):                                                  # stones and strata
        x, y = random.randint(0, 1920), random.randint(390, 1060)
        r = random.randint(4, 16)
        s.ell(x - r, y - r * .6, x + r, y + r * .6, mix((120, 100, 80), (50, 40, 32), random.random()))
    s.rect(1420, 330, 1880, 520, (90, 92, 96))                           # bank basement + vault floor slab
    s.rect(1470, 372, 1830, 480, (52, 56, 64))
    s.rect(1470, 480, 1830, 520, (120, 120, 122))
    tun = (22, 16, 12)
    s.rect(250, 330, 310, 690, tun)                                      # shaft down
    s.rect(250, 640, 1640, 690, tun)                                     # main tunnel
    s.rect(1590, 500, 1640, 690, tun)                                    # shaft up to the vault
    for x in range(330, 1600, 90):
        s.line([(x, 640), (x, 690)], (96, 70, 44), 5)                    # wooden frames
    if lights:
        for x in range(360, 1600, 180):
            s.ell(x - 5, 644, x + 5, 654, (255, 230, 170))
            s.glow(x, 660, 46, 26, (90, 66, 26), 16)


def tunnel(s):
    s.rect(0, 0, 1920, 1080, (8, 6, 5))
    vx, vy = 960, 540
    n = 13
    for i in range(n):
        t = 1 - i / n
        k = t * t
        w, h = 80 + 2150 * k, 60 + 1300 * k
        x0, y0, x1, y1 = vx - w / 2, vy - h * .46, vx + w / 2, vy + h * .54
        wallc = mix((16, 12, 9), (150, 142, 122), k * .8 + .05)          # plastic sheeting
        s.rect(x0, y0, x1, y1, wallc)
        s.rect(x0, y1 - h * .12, x1, y1, mix((12, 9, 7), (96, 72, 50), k))      # dirt floor
        fr = mix((20, 14, 9), (122, 86, 52), k * .9 + .05)                # wooden frame
        tk = 6 + 46 * k
        s.rect(x0, y0, x0 + tk, y1, fr)
        s.rect(x1 - tk, y0, x1, y1, fr)
        s.rect(x0, y0, x1, y0 + tk, fr)
    for i in range(1, 6):
        k = (1 - i / 6.5) ** 2
        y = vy - (60 + 1300 * k) * .46 + 30 + 60 * k
        s.ell(vx - 8 - 16 * k, y, vx + 8 + 16 * k, y + 20 + 34 * k, (255, 236, 180))
        s.glow(vx, y + 20, 150 * k + 30, 90 * k + 20, (110, 82, 36), 30 + 30 * k)
    s.line([(vx, 0), (vx, 330)], (30, 24, 18), 3)


def highway(s):
    s.grad((40, 48, 84), (226, 150, 104), 0, 620)
    s.glow(420, 600, 520, 160, (110, 60, 26), 110)
    for hx, hw, hh in ((0, 700, 120), (500, 900, 170), (1200, 800, 110)):
        s.poly([(hx, 620), (hx + hw * .5, 620 - hh), (hx + hw, 620)], (40, 42, 58))
    s.rect(0, 620, 1920, 1080, (38, 40, 48))
    s.poly([(0, 760), (1920, 700), (1920, 1080), (0, 1080)], (30, 32, 38))
    for lx in range(-100, 1920, 300):
        s.poly([(lx, 900), (lx + 170, 894), (lx + 176, 908), (lx + 6, 914)], (190, 180, 140))


def transporter(s, x, y):
    s.shade([x - 30, y - 8, x + 1120, y + 26], 160, 12, ellipse=True)
    s.rect(x, y - 190, x + 190, y - 30, (150, 40, 36), r=14)             # cab
    s.rect(x + 20, y - 170, x + 110, y - 104, (80, 100, 116), r=8)
    s.rect(x + 200, y - 60, x + 1080, y - 34, (60, 62, 68))              # lower deck
    s.rect(x + 200, y - 250, x + 1080, y - 236, (60, 62, 68))            # upper deck
    for px_ in (x + 210, x + 640, x + 1066):
        s.rect(px_, y - 250, px_ + 12, y - 34, (60, 62, 68))
    cols = ((200, 200, 196), (60, 90, 130), (160, 60, 50), (70, 110, 80))
    for i, (cx, cy) in enumerate(((x + 240, y - 62), (x + 660, y - 62), (x + 240, y - 252), (x + 660, y - 252))):
        c = cols[i]
        s.rect(cx, cy - 74, cx + 380, cy - 22, c, r=10)
        s.poly([(cx + 200, cy - 74), (cx + 226, cy - 130), (cx + 320, cy - 130), (cx + 350, cy - 74)], c)
        s.poly([(cx + 214, cy - 78), (cx + 234, cy - 122), (cx + 312, cy - 122), (cx + 334, cy - 78)], (60, 76, 90))
        for wx in (cx + 70, cx + 300):
            s.ell(wx - 30, cy - 50, wx + 30, cy + 8, (14, 14, 16))
    for wx in (x + 60, x + 150, x + 800, x + 900, x + 1000):
        s.ell(wx - 40, y - 62, wx + 40, y + 16, (14, 14, 16))
        s.ell(wx - 14, y - 36, wx + 14, y - 10, (86, 86, 88))


def police_car(s, x, y, k=1.0):
    s.shade([x - 20, y - 6, x + 380 * k, y + 20], 150, 10, ellipse=True)
    s.rect(x, y - 84 * k, x + 360 * k, y - 26 * k, (228, 228, 224), r=12 * k)
    s.poly([(x + 80 * k, y - 84 * k), (x + 116 * k, y - 140 * k), (x + 250 * k, y - 140 * k), (x + 290 * k, y - 84 * k)], (228, 228, 224))
    s.poly([(x + 96 * k, y - 88 * k), (x + 124 * k, y - 132 * k), (x + 244 * k, y - 132 * k), (x + 270 * k, y - 88 * k)], (50, 64, 80))
    s.rect(x + 20 * k, y - 62 * k, x + 340 * k, y - 48 * k, (30, 50, 110))
    for wx in (x + 76 * k, x + 286 * k):
        s.ell(wx - 32 * k, y - 56 * k, wx + 32 * k, y + 8 * k, (14, 14, 16))
    s.rect(x + 150 * k, y - 156 * k, x + 180 * k, y - 140 * k, (255, 60, 50))
    s.rect(x + 182 * k, y - 156 * k, x + 212 * k, y - 140 * k, (60, 110, 255))
    s.glow(x + 160 * k, y - 150 * k, 150, 90, (130, 20, 16), 50)
    s.glow(x + 200 * k, y - 150 * k, 150, 90, (16, 40, 130), 50)


def night_street(s, van=False):
    s.grad((8, 10, 24), (30, 36, 60), 0, 720)
    random.seed(12)
    x = 0
    while x < 1920:
        w, h = random.randint(180, 320), random.randint(300, 560)
        s.rect(x, 720 - h, x + w, 720, (20, 22, 34))
        for wy in range(720 - h + 30, 690, 64):
            for wx in range(x + 24, x + w - 40, 60):
                lit = random.random() < .2
                s.rect(wx, wy, wx + 30, wy + 40, (196, 150, 80) if lit else (14, 16, 26))
        x += w + random.randint(6, 30)
    s.rect(0, 720, 1920, 1080, (22, 24, 34))
    s.rect(0, 720, 1920, 748, (36, 38, 50))
    for lx in (420, 1380):                                               # street lamps
        s.line([(lx, 720), (lx, 330), (lx + 70, 318)], (10, 10, 14), 8)
        s.ell(lx + 60, 312, lx + 96, 330, (255, 226, 160))
        s.beam([(lx + 78, 326), (lx - 200, 1080), (lx + 380, 1080)], (70, 54, 26), 50)
        s.glow(lx + 78, 330, 110, 80, (120, 92, 40), 40)
    s.glow(960, 1000, 900, 60, (26, 22, 14), 40)                         # wet reflection
    if van:
        vx, vy = 1050, 930
        s.shade([vx - 30, vy - 8, vx + 560, vy + 26], 170, 12, ellipse=True)
        s.rect(vx, vy - 250, vx + 520, vy - 30, (14, 15, 20), r=22)
        s.rect(vx + 370, vy - 220, vx + 494, vy - 140, (40, 52, 70), r=10)
        s.rect(vx + 60, vy - 230, vx + 250, vy - 40, (4, 4, 6))          # open sliding door
        for wx in (vx + 110, vx + 420):
            s.ell(wx - 46, vy - 70, wx + 46, vy + 16, (6, 6, 8))
        s.glow(vx + 520, vy - 90, 120, 60, (110, 96, 50), 30)


def road_dawn(s):
    s.grad((54, 62, 100), (238, 176, 126), 0, 600)
    s.glow(1100, 590, 600, 150, (120, 66, 30), 110)
    for hx, hw, hh in ((-200, 1100, 190), (600, 1100, 260), (1300, 900, 170)):
        s.poly([(hx, 600), (hx + hw * .5, 600 - hh), (hx + hw, 600)], (52, 56, 74))
    s.rect(0, 600, 1920, 1080, (60, 66, 54))
    s.poly([(820, 600), (900, 600), (1500, 1080), (200, 1080)], (44, 46, 52))
    for i in range(6):
        t = (i / 6) ** 2
        y = 620 + t * 460
        w = 4 + t * 26
        s.poly([(858 + t * -10 - w / 2, y), (858 + t * -10 + w / 2, y), (858 - t * 20 + w, y + 30 + t * 40), (858 - t * 20 - w, y + 30 + t * 40)],
               (200, 190, 150))
    for i in range(9):                                                   # fence posts
        t = i / 9
        x, y, h = 940 + t * 760, 606 + t * 300, 20 + t * 90
        s.line([(x, y), (x, y - h)], (30, 30, 34), 3 + t * 6)
    s.haze(520, 700, (236, 190, 150), 70)


def bars(s):
    s.grad((50, 54, 60), (28, 30, 36), 0, 760)
    for y in range(120, 760, 110):
        s.line([(0, y), (1920, y)], (40, 43, 48), 3)
    s.rect(0, 760, 1920, 1080, (44, 46, 50))
    s.rect(820, 150, 1100, 330, (150, 164, 180))
    for x in range(850, 1100, 50):
        s.line([(x, 150), (x, 330)], (24, 26, 30), 8)
    s.beam([(820, 160), (1100, 160), (1400, 1080), (520, 1080)], (56, 60, 66), 50)


def card(s, tint=(40, 34, 26)):
    s.grad((14, 15, 20), (6, 6, 9))
    s.glow(960, 520, 760, 300, tint, 150)


# ------------------------------------------------------------------ scenes
def build():
    def sc(i):
        return Scene(seed=i)

    def out(s, i, **kw):
        s.finish(os.path.join(OUT, f"t{i:02d}.png"), **kw)

    s = sc(1); vault(s)                                                  # 1 the discovery
    s.person(1560, 880, 430, "stand", flip=True, rim=WARM, light=(1, -1))
    s.person(1720, 900, 460, "walk", flip=True, rim=WARM, light=(1, -1))
    out(s, 1, title="FORTALEZA, BRAZIL", sub="Monday, 8 August 2005")

    s = sc(2); vault(s)                                                  # 2 seventy million gone
    out(s, 2, big=("$70 MILLION — GONE", 110, 330), title="NO ALARM. NO WITNESSES.", sub="And a two-day head start")

    s = sc(3); street(s, "day", sign=False)                              # 3 three months earlier
    out(s, 3, title="THREE MONTHS EARLIER", sub="A few doors down the street", pos="tl")

    s = sc(4); street(s, "day", sign=True)                               # 4 the cover business
    s.person(470, 800, 300, "reach", rim=(255, 240, 210), light=(1, -1))
    s.person(640, 810, 310, "stand", flip=True, rim=(255, 240, 210), light=(1, -1), cap=True)
    out(s, 4, title="A NEW BUSINESS OPENS", sub="Plants and artificial grass", pos="tl")

    s = sc(5); street(s, "day", sign=True, pickup=True)                  # 5 sacks of soil
    j = s.person(380, 830, 320, "carry", rim=(255, 240, 210), light=(1, -1), cap=True)
    x, y = j("hR"); s.ell(x - 70, y - 62, x + 60, y + 14, (104, 86, 60))
    s.person(1500, 850, 330, "stand", flip=True, rim=(255, 240, 210), light=(-1, -1))
    out(s, 5, title="SACKS OF SOIL, EVERY DAY", sub="For a gardening company, nothing unusual", pos="tl")

    s = sc(6); card(s, (52, 38, 22))                                     # 6 it was the street
    s.poly([(560, 800), (960, 470), (1360, 800)], (96, 70, 46))
    s.poly([(960, 470), (1360, 800), (1090, 800)], (70, 50, 34))
    s.shade([500, 780, 1420, 850], 150, 16, ellipse=True)
    out(s, 6, big=("IT WASN'T GARDEN SOIL", 84, 250), title="IT WAS THE STREET")

    s = sc(7); room(s)                                                   # 7 digging
    j = s.person(560, 900, 430, "dig", rim=WARM, light=(1, -1))
    x, y = j("hR"); s.line([(x - 60, y - 150), (x + 70, y + 120)], (60, 44, 30), 9)
    s.poly([(x + 50, y + 100), (x + 110, y + 110), (x + 96, y + 190), (x + 44, y + 170)], (120, 124, 130))
    s.person(1250, 930, 420, "carry", flip=True, rim=WARM, light=(1, -1))
    out(s, 7, title="INSIDE THE HOUSE", sub="They were digging")

    s = sc(8); cross(s)                                                  # 8 the route
    s.line([(330, 760), (1560, 760)], (236, 230, 214), 4)
    for ax in (330, 1560):
        s.line([(ax, 742), (ax, 778)], (236, 230, 214), 4)
    text(s, 945, 800, "80 METRES", 44, anchor="mm")
    s.line([(200, 380), (200, 660)], (236, 230, 214), 4)
    text(s, 110, 520, "4 m", 40, anchor="mm")
    text(s, 950, 250, "ONE OF THE CITY'S BUSIEST AVENUES", 28, (40, 40, 44), anchor="mm")
    out(s, 8, title="UNDER THE AVENUE", sub="Traffic covered the noise")

    s = sc(9); tunnel(s)                                                 # 9 engineered tunnel
    s.person(960, 1010, 560, "crawl", rim=WARM, light=(0, -1), shadow=False)
    out(s, 9, title="70 CM WIDE", sub="Wood-lined walls, plastic sheeting, electric lights", pos="tl")

    s = sc(10); vault(s, hole=False, pallets=4)                          # 10 the target
    out(s, 10, title="USED BANKNOTES", sub="Mixed serial numbers. Almost impossible to trace.", pos="tl")

    s = sc(11); street(s, "night", sign=True)                            # 11 the weekend
    s.glow(1560, 300, 420, 160, (30, 34, 50), 80)
    out(s, 11, title="THE FIRST WEEKEND OF AUGUST", sub="The bank is closed", pos="tl")

    s = sc(12); s.grad((66, 48, 34), (30, 22, 18))                       # 12 cutting through the floor
    s.rect(0, 0, 1920, 300, (118, 118, 120))
    for x in range(60, 1920, 150):
        s.line([(x, 20), (x, 280)], (84, 60, 44), 7)                     # rebar
    for y in (90, 200):
        s.line([(0, y), (1920, y)], (84, 60, 44), 7)
    s.poly([(840, 300), (1100, 300), (1060, 120), (900, 110)], (20, 16, 14))
    s.glow(980, 190, 190, 150, (150, 96, 30), 50)
    j = s.person(960, 1010, 640, "reach", rim=(255, 190, 90), light=(0, -1), shadow=False)
    random.seed(4)
    for _ in range(60):                                                  # sparks
        import math
        a, r = random.uniform(.2, 2.94), random.uniform(20, 240)
        x0, y0 = 980 + math.cos(a) * r * .9, 250 + math.sin(a) * r
        s.line([(x0, y0), (x0 + math.cos(a) * 16, y0 + math.sin(a) * 16)], (255, 214, 120), 3)
    out(s, 12, title="1.1 METRES OF REINFORCED CONCRETE", sub="The sensors never triggered")

    s = sc(13); tunnel(s)                                                # 13 hauling it out
    j = s.person(1020, 1000, 520, "drag", rim=WARM, light=(0, -1), shadow=False)
    x, y = j("hR")
    s.line([(x, y), (x + 330, y + 250)], (40, 30, 22), 7)
    for i in range(3):
        bx, by = x + 300 + i * 70, y + 215 + i * 34
        s.rect(bx, by, bx + 150, by + 84, (112, 132, 104), outline=(60, 76, 58), width=3)
        s.rect(bx + 60, by, bx + 90, by + 84, (206, 198, 170))
    out(s, 13, title="3.5 TONS OF CASH", sub="Dragged back through the tunnel, bundle by bundle", pos="tl")

    s = sc(14); street(s, "dawn", sign=True)                             # 14 gone by Monday
    out(s, 14, title="MONDAY MORNING", sub="The house is empty", pos="tl")

    s = sc(15); vault(s, light=(60, 58, 54))                             # 15 biggest in history
    out(s, 15, big=("BRAZIL'S BIGGEST BANK ROBBERY", 86, 320), title="FOR A MOMENT, THE PERFECT CRIME")

    s = sc(16); card(s, (60, 16, 12))                                    # 16 it wasn't
    out(s, 16, big=("IT WASN'T.", 150, 540, (226, 86, 70)))

    s = sc(17); highway(s)                                               # 17 the transporter
    transporter(s, 520, 900)
    police_car(s, 60, 930, 1.1)
    s.person(480, 950, 330, "stand", rim=(255, 170, 120), light=(-1, -1), cap=True)
    out(s, 17, title="FOUR DAYS LATER", sub="About $2 million found hidden inside the cars", pos="tl")

    s = sc(18); night_street(s)                                          # 18 arrests
    police_car(s, 1280, 950, 1.2)
    s.person(760, 960, 470, "stand", rim=COOL, light=(1, -1), cap=True)
    s.person(940, 960, 450, "cuffed", rim=COOL, light=(1, -1))
    s.person(1110, 960, 470, "stand", flip=True, rim=COOL, light=(1, -1), cap=True)
    out(s, 18, title="THE SPENDING GAVE THEM AWAY", sub="Arrests followed, one after another", pos="tl")

    s = sc(19); night_street(s)                                          # 19 other hunters
    s.person(300, 1000, 620, "stand", rim=None, color=(6, 6, 9))
    s.person(1640, 1010, 660, "stand", flip=True, rim=None, color=(6, 6, 9))
    s.person(1000, 900, 300, "walk", rim=WARM, light=(-1, -1))
    out(s, 19, title="THE POLICE WERE NOT ALONE", sub="Other criminals came looking for the money", pos="tl")

    s = sc(20); night_street(s, van=True)                                # 20 the kidnapping
    s.person(900, 950, 430, "drag", flip=True, rim=WARM, light=(-1, -1))
    s.person(1010, 950, 420, "cuffed", rim=WARM, light=(-1, -1))
    out(s, 20, title="TWO MONTHS AFTER THE ROBBERY", sub="A suspected leader is kidnapped. The family pays.", pos="tl")

    s = sc(21); road_dawn(s)                                             # 21 found dead
    out(s, 21, title="HE WAS FOUND DEAD ANYWAY", sub="More kidnappings followed. Each time, the families paid.", pos="tl")

    s = sc(22); bars(s)                                                  # 22 dozens arrested
    for i, x in enumerate((420, 700, 980, 1260, 1540)):
        s.person(x, 1010, 520 + (i % 2) * 30, "stand" if i % 2 else "cuffed", flip=i > 2, rim=COOL, light=(0, -1))
    for x in range(40, 1920, 150):
        s.rect(x, 0, x + 26, 1080, (12, 13, 16))
        s.rect(x + 4, 0, x + 10, 1080, (44, 48, 54))
    out(s, 22, title="DOZENS ARRESTED")

    s = sc(23); card(s, (36, 44, 30))                                    # 23 the money
    for r in range(3):
        for c in range(4 - r):
            x0, y0 = 250 + c * 110 + r * 55, 760 - r * 74
            s.rect(x0, y0, x0 + 100, y0 + 66, (112, 132, 104), outline=(60, 76, 58), width=3)
            s.rect(x0 + 38, y0, x0 + 62, y0 + 66, (206, 198, 170))
    for r in range(7):
        for c in range(8 - r):
            x0, y0 = 880 + c * 110 + r * 55, 760 - r * 74
            s.rect(x0, y0, x0 + 100, y0 + 66, None, outline=(110, 112, 116), width=3)
    text(s, 470, 880, "RECOVERED", 34, anchor="mm")
    text(s, 1320, 880, "NEVER FOUND", 34, (226, 170, 62), anchor="mm")
    out(s, 23, big=("MOST OF THE MONEY NEVER CAME BACK", 66, 150))

    s = sc(24); cross(s, cars=False, dusk=True)                          # 24 recap
    s.haze(0, 1080, (10, 10, 16), 110)
    text(s, 960, 850, "3 MONTHS OF DIGGING  ·  1 WEEKEND  ·  $70 MILLION", 50, anchor="mm")
    text(s, 960, 930, "Almost nobody who touched it got to keep it", 36, (226, 170, 62), bold=False, anchor="mm")
    out(s, 24)

    s = sc(25); tunnel(s)                                                # 25 subscribe
    s.haze(0, 1080, (6, 5, 4), 120)
    s.rect(700, 600, 1220, 720, (200, 44, 36), r=18)
    text(s, 960, 660, "SUBSCRIBE", 70, (250, 246, 238), anchor="mm")
    out(s, 25, big=("MORE TRUE HEISTS EVERY WEEK", 80, 380), title=None)
    text  # noqa


if __name__ == "__main__":
    build()
    print("done")
