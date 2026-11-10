"""Stickman comic kit: solid black figures in coloured outfits with a white rim,
flat saturated backgrounds, bold stroked labels. Everything is drawn at 2x and
downsampled on save. Coordinates passed to helpers are in 1920x1080 space."""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

S = 2
W, H = 1920 * S, 1080 * S
INK = (12, 12, 16)
WHITE = (255, 255, 255)
YELLOW = (255, 206, 30)
RED = (226, 54, 44)
SKIN = (238, 214, 190)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def p(v):
    return int(round(v * S))


def font(size):
    return ImageFont.truetype(FONT, max(8, p(size)))


def shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c)


# ---------- primitive helpers (unscaled coords) ----------
def rect(d, x0, y0, x1, y1, fill=None, outline=None, width=0, radius=0):
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    box = [p(x0), p(y0), p(x1), p(y1)]
    if radius:
        d.rounded_rectangle(box, radius=p(radius), fill=fill, outline=outline, width=p(width) if outline else 0)
    else:
        d.rectangle(box, fill=fill, outline=outline, width=p(width) if outline else 0)


def ell(d, x0, y0, x1, y1, fill=None, outline=None, width=0):
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    d.ellipse([p(x0), p(y0), p(x1), p(y1)], fill=fill, outline=outline, width=p(width) if outline else 0)


def circ(d, cx, cy, r, fill=None, outline=None, width=0):
    ell(d, cx - r, cy - r, cx + r, cy + r, fill, outline, width)


def poly(d, pts, fill=None, outline=None, width=0):
    pts = [(p(x), p(y)) for x, y in pts]
    d.polygon(pts, fill=fill)
    if outline:
        d.line(pts + [pts[0]], fill=outline, width=p(width or 6), joint="curve")


def line(d, pts, fill=INK, width=6):
    d.line([(p(x), p(y)) for x, y in pts], fill=fill, width=p(width), joint="curve")


def limb(d, pts, color, width):
    pp = [(p(x), p(y)) for x, y in pts]
    d.line(pp, fill=color, width=p(width), joint="curve")
    r = p(width) / 2
    for x, y in pp:
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def text(d, x, y, s, size, fill=WHITE, anchor="la", stroke=True, stroke_fill=INK):
    d.text((p(x), p(y)), s, font=font(size), fill=fill, anchor=anchor,
           stroke_width=p(size * 0.11) if stroke else 0, stroke_fill=stroke_fill)


def vgrad(img, top, bottom, y0, y1):
    d = ImageDraw.Draw(img)
    for y in range(p(y0), p(y1)):
        t = (y - p(y0)) / max(1, p(y1) - p(y0))
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))


def rim(layer, px=7, color=WHITE):
    """White comic rim around whatever is on an RGBA layer (bbox-cropped for speed)."""
    bb = layer.getbbox()
    if not bb:
        return layer
    m = p(px) + 4
    bb = (max(0, bb[0] - m), max(0, bb[1] - m), min(W, bb[2] + m), min(H, bb[3] + m))
    crop = layer.crop(bb)
    grown = crop.split()[3].filter(ImageFilter.MaxFilter(2 * p(px) + 1))
    halo = Image.new("RGBA", crop.size, color + (0,))
    halo.putalpha(grown)
    halo.alpha_composite(crop)
    out = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    out.paste(halo, bb[:2])
    return out


# ---------- poses (offsets from the ground point under the hips) ----------
STAND = dict(head=(0, -400), neck=(0, -330), shoulder=(0, -306), hip=(0, -170),
             kneeL=(-30, -86), footL=(-52, -6), kneeR=(30, -86), footR=(54, -6),
             elbowL=(-56, -236), handL=(-66, -160), elbowR=(56, -236), handR=(66, -160))
POINT = dict(STAND, elbowR=(86, -300), handR=(170, -318), elbowL=(-58, -250), handL=(-40, -180))
RUN = dict(head=(26, -400), neck=(16, -330), shoulder=(14, -306), hip=(0, -170),
           kneeL=(-70, -96), footL=(-150, -130), kneeR=(66, -90), footR=(104, -8),
           elbowL=(-70, -250), handL=(-118, -310), elbowR=(84, -250), handR=(150, -222))
CARRY = dict(head=(10, -400), neck=(6, -330), shoulder=(6, -306), hip=(0, -170),
             kneeL=(-38, -88), footL=(-62, -6), kneeR=(44, -90), footR=(70, -6),
             elbowL=(40, -236), handL=(104, -250), elbowR=(60, -214), handR=(124, -206))
HANDSUP = dict(STAND, elbowL=(-84, -330), handL=(-96, -430), elbowR=(84, -330), handR=(96, -430))
PHONE = dict(STAND, elbowR=(78, -300), handR=(44, -392), elbowL=(-56, -236), handL=(-30, -170))
HIPS = dict(STAND, elbowL=(-86, -236), handL=(-30, -186), elbowR=(86, -236), handR=(30, -186))
CROSS = dict(STAND, elbowL=(-60, -240), handL=(34, -252), elbowR=(60, -240), handR=(-34, -262))
SHRUG = dict(STAND, elbowL=(-76, -270), handL=(-130, -316), elbowR=(76, -270), handR=(130, -316))
SIT = dict(head=(0, -330), neck=(0, -262), shoulder=(0, -240), hip=(0, -110),
           kneeL=(70, -112), footL=(76, -6), kneeR=(96, -106), footR=(104, -6),
           elbowL=(40, -180), handL=(110, -196), elbowR=(56, -170), handR=(128, -184))
BARS = dict(STAND, elbowL=(-70, -300), handL=(-60, -370), elbowR=(70, -300), handR=(60, -370))


def stickman(x, y, pose=STAND, s=1.0, jacket=(40, 70, 120), hat="beanie", hat_color=(200, 50, 50),
             masked=False, face="neutral", flip=False, badge=None, long_coat=False):
    """One clothed black stick figure on its own RGBA layer. x,y = ground under hips."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    sx = -1 if flip else 1

    def j(n):
        ox, oy = pose[n]
        return (x + sx * ox * s, y + oy * s)

    lw = 26 * s
    for k, f_ in (("kneeL", "footL"), ("kneeR", "footR")):
        limb(d, [j("hip"), j(k), j(f_)], INK, lw)
        fx, fy = j(f_)
        rect(d, fx - 22 * s + sx * 14 * s, fy - 16 * s, fx + 22 * s + sx * 14 * s, fy + 14 * s, fill=(60, 44, 32), radius=12 * s)
    limb(d, [j("shoulder"), j("elbowL"), j("handL")], INK, lw * 0.9)
    limb(d, [j("shoulder"), j("elbowL")], shade(jacket, 0.8), lw * 1.05)
    limb(d, [j("neck"), j("hip")], INK, lw * 1.2)
    nx, ny = j("neck")
    hx_, hy_ = j("hip")
    bottom = hy_ + (90 * s if long_coat else 6 * s)
    rect(d, min(nx, hx_) - 44 * s, ny - 6 * s, max(nx, hx_) + 44 * s, bottom, fill=jacket, radius=26 * s)
    line(d, [((nx + hx_) / 2, ny + 6 * s), ((nx + hx_) / 2, bottom - 4 * s)], fill=shade(jacket, 0.7), width=5 * s)
    if badge:
        text(d, (nx + hx_) / 2, ny + 54 * s, badge, 30 * s, fill=YELLOW, anchor="mm", stroke=False)
    limb(d, [j("shoulder"), j("elbowR"), j("handR")], INK, lw * 0.9)
    limb(d, [j("shoulder"), j("elbowR")], jacket, lw * 1.05)
    for hnd in ("handL", "handR"):
        gx, gy = j(hnd)
        circ(d, gx, gy, 17 * s, fill=(40, 40, 46))
    cx, cy = j("head")
    r = 62 * s
    circ(d, cx, cy, r, fill=INK)
    if masked:
        rect(d, cx - 40 * s, cy - 14 * s, cx + 40 * s, cy + 16 * s, fill=SKIN, radius=14 * s)
    # eyes
    if face == "shades":
        rect(d, cx - 46 * s, cy - 14 * s, cx + 46 * s, cy + 12 * s, fill=(40, 44, 60), radius=8 * s)
        line(d, [(cx - 46 * s, cy - 10 * s), (cx + 46 * s, cy - 10 * s)], fill=(150, 160, 190), width=4 * s)
    elif face in ("dead",):
        for dx in (-20, 20):
            line(d, [(cx + dx * s - 9 * s, cy - 10 * s), (cx + dx * s + 9 * s, cy + 8 * s)], fill=WHITE, width=5 * s)
            line(d, [(cx + dx * s + 9 * s, cy - 10 * s), (cx + dx * s - 9 * s, cy + 8 * s)], fill=WHITE, width=5 * s)
    elif face == "sleep":
        for dx in (-20, 20):
            line(d, [(cx + dx * s - 10 * s, cy), (cx + dx * s + 10 * s, cy)], fill=WHITE, width=5 * s)
    else:
        big = 1.35 if face == "scared" else 1.0
        for dx in (-18, 18):
            if masked:
                ell(d, cx + dx * s - 7 * s, cy - 8 * s, cx + dx * s + 7 * s, cy + 10 * s, fill=INK)
            else:
                ell(d, cx + dx * s - 10 * s * big, cy - 12 * s * big, cx + dx * s + 10 * s * big, cy + 10 * s * big, fill=WHITE)
                circ(d, cx + dx * s + sx * 2 * s, cy + 1 * s, 4.5 * s, fill=INK)
    bc = INK if masked else WHITE
    if face == "angry":
        line(d, [(cx - 32 * s, cy - 26 * s), (cx - 8 * s, cy - 14 * s)], fill=bc, width=6 * s)
        line(d, [(cx + 32 * s, cy - 26 * s), (cx + 8 * s, cy - 14 * s)], fill=bc, width=6 * s)
    elif face == "scared":
        line(d, [(cx - 30 * s, cy - 24 * s), (cx - 10 * s, cy - 32 * s)], fill=WHITE, width=5 * s)
        line(d, [(cx + 30 * s, cy - 24 * s), (cx + 10 * s, cy - 32 * s)], fill=WHITE, width=5 * s)
        ell(d, cx - 10 * s, cy + 22 * s, cx + 10 * s, cy + 42 * s, fill=WHITE)
    elif face == "happy" and not masked:
        d.arc([p(cx - 22 * s), p(cy + 6 * s), p(cx + 22 * s), p(cy + 40 * s)], 10, 170, fill=WHITE, width=p(6 * s))
    elif face == "sad" and not masked:
        d.arc([p(cx - 20 * s), p(cy + 26 * s), p(cx + 20 * s), p(cy + 56 * s)], 190, 350, fill=WHITE, width=p(6 * s))
    # hats
    if hat == "beanie":
        d.pieslice([p(cx - r - 3), p(cy - r - 8 * s), p(cx + r + 3), p(cy + r - 8 * s)], 180, 360, fill=hat_color)
        rect(d, cx - r - 6, cy - 22 * s, cx + r + 6, cy - 2 * s, fill=shade(hat_color, 0.75), radius=8 * s)
        circ(d, cx, cy - r - 12 * s, 14 * s, fill=hat_color)
    elif hat == "fedora":
        rect(d, cx - r - 30 * s, cy - 36 * s, cx + r + 30 * s, cy - 18 * s, fill=hat_color, radius=9 * s)
        rect(d, cx - 50 * s, cy - 104 * s, cx + 50 * s, cy - 30 * s, fill=hat_color, radius=20 * s)
        rect(d, cx - 50 * s, cy - 54 * s, cx + 50 * s, cy - 36 * s, fill=shade((150, 40, 40), 1))
    elif hat == "cap":
        d.pieslice([p(cx - r - 3), p(cy - r - 10 * s), p(cx + r + 3), p(cy + r - 10 * s)], 180, 360, fill=hat_color)
        rect(d, cx + (0 if sx > 0 else -r - 44 * s), cy - 24 * s, cx + (r + 44 * s if sx > 0 else 0), cy - 8 * s, fill=shade(hat_color, 0.8), radius=8 * s)
    elif hat == "hardhat":
        d.pieslice([p(cx - r - 6), p(cy - r - 14 * s), p(cx + r + 6), p(cy + r - 14 * s)], 180, 360, fill=hat_color)
        rect(d, cx - r - 16 * s, cy - 26 * s, cx + r + 16 * s, cy - 12 * s, fill=shade(hat_color, 0.85), radius=6 * s)
    elif hat == "hair":
        d.pieslice([p(cx - r - 2), p(cy - r - 12 * s), p(cx + r + 2), p(cy + r - 16 * s)], 180, 360, fill=hat_color)
    return layer, j


# ---------- props ----------
def bag(d, x, y, s=1.0):
    r = 70 * s
    ell(d, x - r - 7, y - 2 * r - 7, x + r + 7, y + 7, fill=INK)
    ell(d, x - r, y - 2 * r, x + r, y, fill=(226, 190, 120))
    d.pieslice([p(x - r), p(y - 2 * r), p(x + r), p(y)], 20, 160, fill=(204, 164, 96))
    poly(d, [(x - 24 * s, y - 2 * r + 10), (x + 24 * s, y - 2 * r + 10), (x + 44 * s, y - 2 * r - 44 * s), (x - 44 * s, y - 2 * r - 44 * s)],
         fill=(226, 190, 120), outline=INK, width=6)
    rect(d, x - 30 * s, y - 2 * r, x + 30 * s, y - 2 * r + 16 * s, fill=(150, 40, 40), radius=6)
    d.text((p(x), p(y - r + 4)), "$", font=font(84 * s), fill=(30, 110, 60), anchor="mm", stroke_width=p(3), stroke_fill=(245, 240, 220))


def bill(d, x, y, ang=0.0, s=1.0):
    w, h = 84 * s, 40 * s
    c, s_ = math.cos(ang), math.sin(ang)
    pts = [(x + a * c - b * s_, y + a * s_ + b * c) for a, b in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    poly(d, pts, fill=(120, 196, 110), outline=INK, width=5)
    circ(d, x, y, 10 * s, fill=(60, 140, 70))


def cash_stack(d, x, y, n=3, s=1.0):
    """Banded bundles stacked upward from (x,y) bottom-centre."""
    w, h = 120 * s, 34 * s
    for i in range(n):
        yy = y - i * h
        rect(d, x - w / 2, yy - h, x + w / 2, yy, fill=(120, 196, 110), outline=INK, width=5)
        rect(d, x - 16 * s, yy - h, x + 16 * s, yy, fill=(245, 240, 220), outline=INK, width=4)


def money_pile(d, x, y, cols=6, rows=4, s=1.0):
    for c in range(cols):
        n = max(1, rows - abs(c - (cols - 1) / 2) * 1.1)
        cash_stack(d, x + (c - (cols - 1) / 2) * 126 * s, y, int(round(n + 1)), s)


def gem(d, x, y, s=1.0, color=(90, 200, 240)):
    poly(d, [(x - 30 * s, y - 20 * s), (x - 14 * s, y - 40 * s), (x + 14 * s, y - 40 * s), (x + 30 * s, y - 20 * s), (x, y + 20 * s)],
         fill=color, outline=INK, width=5)
    line(d, [(x - 30 * s, y - 20 * s), (x + 30 * s, y - 20 * s)], width=4)


def van(d, x, y, s=1.0, flip=False, body=(46, 50, 66)):
    """Side view van, bottom-left wheel line at (x,y). Faces right unless flip."""
    def X(v):
        return x + (560 * s - v * s if flip else v * s)

    def bx(a, b):
        return sorted((X(a), X(b)))
    a, b = bx(-8, 568)
    rect(d, a, y - 388 * s, b, y + 8 * s, fill=INK, radius=40 * s)
    a, b = bx(0, 560)
    rect(d, a, y - 380 * s, b, y, fill=body, radius=34 * s)
    a, b = bx(14, 546)
    rect(d, a, y - 366 * s, b, y - 320 * s, fill=shade(body, 1.5), radius=18 * s)
    a, b = bx(380, 530)
    rect(d, a, y - 300 * s, b, y - 190 * s, fill=(150, 206, 236), outline=INK, width=7, radius=14 * s)
    a, b = bx(40, 340)
    rect(d, a, y - 170 * s, b, y - 156 * s, fill=shade(body, 0.7))
    line(d, [(X(360), y - 350 * s), (X(360), y - 30 * s)], fill=shade(body, 0.6), width=6 * s)
    a, b = bx(524, 566)
    rect(d, a, y - 120 * s, b, y - 80 * s, fill=YELLOW, outline=INK, width=5, radius=8 * s)
    a, b = bx(-6, 30)
    rect(d, a, y - 120 * s, b, y - 80 * s, fill=RED, outline=INK, width=5, radius=8 * s)
    for cx in (130, 440):
        circ(d, X(cx), y + 4 * s, 78 * s, fill=INK)
        circ(d, X(cx), y + 4 * s, 62 * s, fill=(58, 58, 66))
        circ(d, X(cx), y + 4 * s, 26 * s, fill=(190, 190, 200), outline=INK, width=6)


def car(d, x, y, s=1.0, color=(240, 130, 180), flip=False, police=False):
    """Classic long sedan, wheel line at y, left end at x."""
    def X(v):
        return x + (620 * s - v * s if flip else v * s)
    pts = [(X(0), y - 60 * s), (X(10), y - 150 * s), (X(150), y - 160 * s), (X(210), y - 250 * s), (X(430), y - 250 * s),
           (X(500), y - 160 * s), (X(610), y - 140 * s), (X(620), y - 50 * s), (X(600), y - 20 * s), (X(20), y - 20 * s)]
    poly(d, pts, fill=color, outline=INK, width=9)
    poly(d, [(X(226), y - 236 * s), (X(310), y - 236 * s), (X(310), y - 166 * s), (X(176), y - 166 * s)], fill=(170, 220, 244), outline=INK, width=6)
    poly(d, [(X(330), y - 236 * s), (X(420), y - 236 * s), (X(474), y - 166 * s), (X(330), y - 166 * s)], fill=(170, 220, 244), outline=INK, width=6)
    line(d, [(X(20), y - 100 * s), (X(600), y - 100 * s)], fill=shade(color, 0.75), width=7 * s)
    poly(d, [(X(0), y - 60 * s), (X(-26), y - 190 * s), (X(40), y - 152 * s)], fill=color, outline=INK, width=7)  # tail fin
    a, b = sorted((X(596), X(626)))
    rect(d, a, y - 120 * s, b, y - 90 * s, fill=YELLOW, outline=INK, width=5, radius=6 * s)
    if police:
        a, b = sorted((X(280), X(350)))
        rect(d, a, y - 284 * s, b, y - 250 * s, fill=RED, outline=INK, width=6, radius=8 * s)
        a, b = sorted((X(350), X(400)))
        rect(d, a, y - 284 * s, b, y - 250 * s, fill=(60, 120, 240), outline=INK, width=6, radius=8 * s)
        text(d, X(310), y - 128 * s, "POLICE", 34 * s, fill=WHITE, anchor="mm", stroke=False)
    for cx in (130, 490):
        circ(d, X(cx), y - 14 * s, 62 * s, fill=INK)
        circ(d, X(cx), y - 14 * s, 46 * s, fill=(58, 58, 66))
        circ(d, X(cx), y - 14 * s, 20 * s, fill=(210, 210, 220), outline=INK, width=5)


def plane(d, x, y, s=1.0, body=(236, 240, 248), stripe=(40, 80, 170)):
    """Jet facing right, nose near x+760s."""
    rect(d, x, y - 60 * s, x + 700 * s, y + 60 * s, fill=body, outline=INK, width=8, radius=60 * s)
    poly(d, [(x + 640 * s, y - 58 * s), (x + 770 * s, y - 6 * s), (x + 760 * s, y + 30 * s), (x + 640 * s, y + 58 * s)], fill=body, outline=INK, width=8)
    poly(d, [(x + 20 * s, y - 50 * s), (x - 50 * s, y - 220 * s), (x + 60 * s, y - 220 * s), (x + 170 * s, y - 56 * s)], fill=stripe, outline=INK, width=8)
    poly(d, [(x + 290 * s, y + 20 * s), (x + 470 * s, y + 20 * s), (x + 250 * s, y + 200 * s), (x + 170 * s, y + 200 * s)], fill=shade(body, 0.86), outline=INK, width=8)
    rect(d, x + 60 * s, y + 4 * s, x + 640 * s, y + 20 * s, fill=stripe)
    for wx in range(150, 620, 52):
        circ(d, x + wx * s, y - 22 * s, 13 * s, fill=(70, 120, 190))
    poly(d, [(x + 690 * s, y - 30 * s), (x + 730 * s, y - 14 * s), (x + 690 * s, y - 6 * s)], fill=(70, 120, 190), outline=INK, width=4)


def crate(d, x, y, w=110, h=110):
    rect(d, x, y - h, x + w, y, fill=(214, 150, 70), outline=INK, width=7)
    line(d, [(x, y - h), (x + w, y)], width=5)
    line(d, [(x + w, y - h), (x, y)], width=5)


def vault_door(d, cx, cy, r=300, open_=False):
    circ(d, cx, cy, r + 26, fill=(70, 78, 96), outline=INK, width=10)
    if open_:
        circ(d, cx, cy, r, fill=(24, 26, 36), outline=INK, width=10)
    else:
        circ(d, cx, cy, r, fill=(168, 178, 196), outline=INK, width=10)
        circ(d, cx, cy, r - 50, fill=(146, 156, 176), outline=INK, width=8)
        for a in range(0, 360, 30):
            circ(d, cx + (r - 24) * math.cos(math.radians(a)), cy + (r - 24) * math.sin(math.radians(a)), 11, fill=(98, 106, 124))
        for a in (0, 60, 120):
            dx, dy = 130 * math.cos(math.radians(a)), 130 * math.sin(math.radians(a))
            line(d, [(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=INK, width=22)
            line(d, [(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=(210, 190, 90), width=12)
        circ(d, cx, cy, 44, fill=(210, 190, 90), outline=INK, width=8)


def bubble(d, x, y, s, size=54, w=None, tail="left"):
    f = font(size)
    lines = s.split("\n")
    tw = max(d.textlength(t, font=f) for t in lines) / S
    bw, bh = tw + 70, len(lines) * size * 1.2 + 50
    rect(d, x, y, x + bw, y + bh, fill=WHITE, outline=INK, width=8, radius=34)
    tx = x + 70 if tail == "left" else x + bw - 130
    poly(d, [(tx, y + bh - 6), (tx + 60, y + bh - 6), (tx + (0 if tail == "left" else 60), y + bh + 60)], fill=WHITE)
    line(d, [(tx, y + bh - 4), (tx + (0 if tail == "left" else 60), y + bh + 60), (tx + 60, y + bh - 4)], width=8)
    for i, t in enumerate(lines):
        d.text((p(x + 35), p(y + 25 + i * size * 1.2)), t, font=f, fill=INK)


def big_x(d, cx, cy, r=70, width=22, color=RED):
    for a, b in (((cx - r, cy - r), (cx + r, cy + r)), ((cx + r, cy - r), (cx - r, cy + r))):
        line(d, [a, b], fill=INK, width=width + 12)
    for a, b in (((cx - r, cy - r), (cx + r, cy + r)), ((cx + r, cy - r), (cx - r, cy + r))):
        line(d, [a, b], fill=color, width=width)


def portrait(d, x, y, name, hat="beanie", hat_color=(200, 50, 50), jacket=(40, 70, 120), masked=False, w=190, h=250, status=None):
    """Framed mugshot card with a mini head. status: None | 'x' | 'missing'"""
    rect(d, x, y, x + w, y + h, fill=(250, 246, 232), outline=INK, width=8, radius=10)
    rect(d, x + 14, y + 14, x + w - 14, y + h - 62, fill=(150, 170, 200))
    cx, cy, r = x + w / 2, y + 104, 46
    rect(d, cx - 56, cy + 40, cx + 56, y + h - 62, fill=jacket, radius=18)
    circ(d, cx, cy, r, fill=INK)
    if masked:
        rect(d, cx - 30, cy - 10, cx + 30, cy + 12, fill=SKIN, radius=10)
        for dx in (-13, 13):
            circ(d, cx + dx, cy + 1, 6, fill=INK)
    else:
        for dx in (-14, 14):
            circ(d, cx + dx, cy, 8, fill=WHITE)
            circ(d, cx + dx, cy + 1, 3.5, fill=INK)
    if hat == "beanie":
        d.pieslice([p(cx - r - 2), p(cy - r - 6), p(cx + r + 2), p(cy + r - 6)], 180, 360, fill=hat_color)
        rect(d, cx - r - 4, cy - 16, cx + r + 4, cy - 2, fill=shade(hat_color, 0.75), radius=6)
    elif hat == "fedora":
        rect(d, cx - r - 20, cy - 28, cx + r + 20, cy - 14, fill=hat_color, radius=6)
        rect(d, cx - 36, cy - 76, cx + 36, cy - 22, fill=hat_color, radius=14)
    elif hat == "cap":
        d.pieslice([p(cx - r - 2), p(cy - r - 8), p(cx + r + 2), p(cy + r - 8)], 180, 360, fill=hat_color)
        rect(d, cx, cy - 18, cx + r + 30, cy - 6, fill=shade(hat_color, 0.8), radius=6)
    elif hat == "hair":
        d.pieslice([p(cx - r - 2), p(cy - r - 10), p(cx + r + 2), p(cy + r - 12)], 180, 360, fill=hat_color)
    d.text((p(cx), p(y + h - 32)), name, font=font(26), fill=INK, anchor="mm")
    if status == "x":
        big_x(d, cx, y + h / 2 - 20, r=70, width=18)
    elif status == "missing":
        big_x(d, cx, y + h / 2 - 20, r=70, width=18, color=(255, 150, 30))


def fingerprint(d, cx, cy, r=46, color=RED):
    for k in range(5):
        rr = r - k * 9
        d.arc([p(cx - rr), p(cy - rr * 1.2), p(cx + rr), p(cy + rr * 1.2)], 200 + k * 8, 520 - k * 8, fill=color, width=p(5))


def lamp_post(d, x, y, h=520):
    rect(d, x - 9, y - h, x + 9, y, fill=(40, 44, 60))
    rect(d, x - 9, y - h, x + 90, y - h + 16, fill=(40, 44, 60), radius=6)
    ell(d, x + 56, y - h + 10, x + 110, y - h + 44, fill=(255, 236, 150), outline=INK, width=5)


# ---------- scene ----------
class Scene:
    def __init__(self, seed=1):
        random.seed(seed)
        self.rgb = Image.new("RGB", (W, H), (30, 40, 90))
        self.img = None
        self.d = ImageDraw.Draw(self.rgb)

    def lock_bg(self):
        """Switch from background painting (RGB) to layered drawing (RGBA)."""
        self.img = self.rgb.convert("RGBA")
        self.d = ImageDraw.Draw(self.img)

    def glow(self, draw_fn, blur=26):
        """Additive blurred light on the background (call before lock_bg)."""
        g = Image.new("RGB", (W, H), (0, 0, 0))
        draw_fn(ImageDraw.Draw(g))
        g = g.filter(ImageFilter.GaussianBlur(p(blur)))
        self.rgb = ImageChops.add(self.rgb, g)
        self.d = ImageDraw.Draw(self.rgb)

    def man(self, x, y, pose=STAND, hold=None, shadow=True, rim_px=7, **kw):
        if self.img is None:
            self.lock_bg()
        s = kw.get("s", 1.0)
        if shadow:
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ell(ImageDraw.Draw(sh), x - 125 * s, y - 14, x + 125 * s, y + 26, fill=(10, 12, 26, 130))
            self.img.alpha_composite(sh)
        layer, j = stickman(x, y, pose, **kw)
        if hold:
            hold(ImageDraw.Draw(layer), j)
        self.img.alpha_composite(rim(layer, rim_px))
        self.d = ImageDraw.Draw(self.img)
        return j

    def prop(self, fn, rim_px=6):
        if self.img is None:
            self.lock_bg()
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fn(ImageDraw.Draw(layer))
        self.img.alpha_composite(rim(layer, rim_px) if rim_px else layer)
        self.d = ImageDraw.Draw(self.img)

    def label(self, x, y, s, size=84, fill=WHITE, anchor="la"):
        if self.img is None:
            self.lock_bg()
        text(self.d, x, y, s, size, fill=fill, anchor=anchor)

    def save(self, path):
        if self.img is None:
            self.lock_bg()
        self.d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=p(14))
        self.img.convert("RGB").resize((1920, 1080), Image.LANCZOS).save(path, quality=93)


# ---------- backgrounds (paint on sc.rgb via sc.d before any man/prop) ----------
def night_sky(sc, horizon=760, top=(20, 34, 92), bottom=(64, 108, 178), moon=(1325, 215), skyline=True):
    vgrad(sc.rgb, top, bottom, 0, horizon)
    d = sc.d
    for _ in range(70):
        x, y = random.randint(0, 1920), random.randint(0, int(horizon * 0.55))
        circ(d, x, y, random.choice([1.5, 1.5, 2, 3]), fill=(236, 240, 255))
    if moon:
        mx, my = moon
        circ(d, mx, my, 145, fill=(110, 150, 214))
        circ(d, mx, my, 115, fill=(255, 244, 196))
        circ(d, mx - 30, my - 40, 25, fill=(240, 224, 164))
        circ(d, mx + 50, my + 40, 16, fill=(240, 224, 164))
    for cx, cy, w_ in ((300, 250, 300), (900, 180, 220), (1650, 330, 260)):
        rect(d, cx, cy, cx + w_, cy + 44, fill=shade(top, 2.0), radius=22)
        rect(d, cx + 50, cy - 30, cx + w_ - 60, cy + 20, fill=shade(top, 2.0), radius=22)
    if skyline:
        sil = shade(top, 1.25)
        x = 0
        while x < 1920:
            w_ = random.randint(60, 150)
            h_ = random.randint(70, 220)
            rect(d, x, horizon - h_, x + w_, horizon, fill=sil)
            for wy in range(horizon - h_ + 16, horizon - 15, 30):
                for wx in range(x + 12, x + w_ - 14, 26):
                    if random.random() < 0.3:
                        rect(d, wx, wy, wx + 11, wy + 14, fill=(255, 214, 110))
            x += w_ + random.randint(0, 24)


def tarmac(sc, y=860):
    d = sc.d
    rect(d, 0, y, 1920, 1080, fill=(70, 76, 104))
    rect(d, 0, y + 120, 1920, 1080, fill=(56, 62, 88))
    line(d, [(0, y), (1920, y)], width=10)
    for lx in range(-60, 1920, 300):
        poly(d, [(lx, 1024), (lx + 170, 1024), (lx + 196, 1050), (lx + 26, 1050)], fill=YELLOW)


def control_tower(d, x=268, base=760):
    rect(d, x - 18, base - 330, x + 18, base, fill=(22, 38, 96))
    poly(d, [(x - 68, base - 330), (x + 68, base - 330), (x + 44, base - 394), (x - 44, base - 394)], fill=(22, 38, 96))
    rect(d, x - 36, base - 378, x + 36, base - 346, fill=(120, 230, 236))
    circ(d, x, base - 416, 10, fill=(255, 70, 60))


def cargo_building(sc, bx0=1230, ground=860, sign="CARGO BLDG 261", door_open=True):
    d = sc.d
    rect(d, bx0, 250, 1920, ground, fill=(214, 86, 60))
    for cx in range(bx0 + 20, 1920, 36):
        line(d, [(cx, 260), (cx, ground)], fill=(190, 70, 48), width=6)
    rect(d, bx0 - 20, 214, 1920, 262, fill=(120, 44, 34))
    line(d, [(bx0, 250), (bx0, ground)], width=10)
    line(d, [(bx0 - 20, 214), (1920, 214)], width=10)
    line(d, [(bx0 - 20, 262), (1920, 262)], width=8)
    rect(d, bx0 + 70, 300, 1880, 400, fill=(250, 246, 232), outline=INK, width=9, radius=12)
    d.text((p((bx0 + 70 + 1880) / 2), p(350)), sign, font=font(54), fill=INK, anchor="mm")
    x0, x1 = bx0 + 170, bx0 + 570
    if door_open:
        rect(d, x0, 470, x1, ground, fill=(255, 226, 120))
        poly(d, [(x0 + 100, 560), (x1 - 100, 560), (x1, ground), (x0, ground)], fill=(255, 240, 170))
        for ly in range(470, 550, 20):
            rect(d, x0, ly, x1, ly + 13, fill=(120, 128, 150))
        for cx, cw, ch in ((x0 + 30, 100, 100), (x0 + 140, 120, 150), (x0 + 280, 90, 86)):
            crate(d, cx, ground, cw, ch)
    else:
        rect(d, x0, 470, x1, ground, fill=(150, 158, 176))
        for ly in range(470, ground, 22):
            line(d, [(x0, ly), (x1, ly)], fill=(120, 128, 150), width=5)
    rect(d, x0, 470, x1, ground, outline=INK, width=10)


def bg_airport(sc, building=True, door_open=True, jet=True, light=True):
    night_sky(sc)
    d = sc.d
    control_tower(d)
    if jet:
        plane(d, 420, 730, 0.78)
    if building:
        cargo_building(sc, door_open=door_open)
    tarmac(sc)
    if building and door_open and light:
        sc.glow(lambda g: poly(g, [(1400, 860), (1800, 860), (1700, 1080), (900, 1080)], fill=(110, 84, 20)))


def bg_room(sc, wall=(96, 60, 54), floor=(120, 84, 54), floor_y=880, stripes=True):
    d = sc.d
    rect(d, 0, 0, 1920, floor_y, fill=wall)
    if stripes:
        for x in range(0, 1920, 120):
            rect(d, x, 0, x + 60, floor_y, fill=shade(wall, 0.92))
    rect(d, 0, floor_y - 26, 1920, floor_y, fill=shade(wall, 0.6))
    rect(d, 0, floor_y, 1920, 1080, fill=floor)
    for x in range(-200, 2200, 230):
        line(d, [(x, floor_y), (x - 140, 1080)], fill=shade(floor, 0.8), width=5)
    line(d, [(0, floor_y), (1920, floor_y)], width=10)


def bg_bar(sc):
    bg_room(sc, wall=(110, 46, 52), floor=(98, 66, 44))
    d = sc.d
    # shelves with bottles
    for sy in (250, 400):
        rect(d, 80, sy, 900, sy + 18, fill=(70, 40, 30), outline=INK, width=6)
        for bx in range(110, 880, 64):
            c = random.choice([(60, 150, 90), (200, 150, 50), (150, 60, 60), (70, 110, 170)])
            rect(d, bx, sy - 90, bx + 34, sy, fill=c, outline=INK, width=5, radius=6)
            rect(d, bx + 10, sy - 120, bx + 24, sy - 86, fill=c, outline=INK, width=5)
    # neon sign
    rect(d, 1240, 150, 1780, 330, fill=(40, 20, 40), outline=INK, width=9, radius=18)
    text(d, 1510, 240, "ROBERT'S LOUNGE", 46, fill=(255, 120, 200), anchor="mm", stroke=False)
    # hanging lamp
    line(d, [(1100, 0), (1100, 150)], width=6)
    poly(d, [(1040, 210), (1160, 210), (1130, 150), (1070, 150)], fill=(60, 60, 70), outline=INK, width=6)
    sc.glow(lambda g: poly(g, [(1050, 210), (1150, 210), (1420, 880), (780, 880)], fill=(70, 56, 20)), blur=30)
    sc.glow(lambda g: rect(g, 1220, 130, 1800, 350, fill=(60, 14, 44), radius=30), blur=40)


def bg_street(sc, snow=False, hydrant_x=None):
    night_sky(sc, horizon=640, moon=(1620, 160), skyline=False)
    d = sc.d
    cols = [(150, 70, 60), (120, 80, 110), (90, 100, 130), (160, 110, 70)]
    x = -40
    k = 0
    while x < 1920:
        w_ = random.randint(380, 520)
        top = random.randint(150, 260)
        c = cols[k % len(cols)]
        rect(d, x, top, x + w_, 840, fill=c, outline=INK, width=9)
        rect(d, x - 10, top - 24, x + w_ + 10, top + 10, fill=shade(c, 0.7), outline=INK, width=7)
        for wy in range(top + 60, 700, 150):
            for wx in range(x + 50, x + w_ - 100, 130):
                lit = random.random() < 0.45
                rect(d, wx, wy, wx + 80, wy + 100, fill=(255, 220, 120) if lit else (40, 46, 76), outline=INK, width=6)
                line(d, [(wx + 40, wy), (wx + 40, wy + 100)], width=4)
        rect(d, x + w_ / 2 - 50, 700, x + w_ / 2 + 50, 840, fill=shade(c, 0.5), outline=INK, width=7)
        x += w_
        k += 1
    rect(d, 0, 840, 1920, 900, fill=(150, 150, 160))
    line(d, [(0, 840), (1920, 840)], width=9)
    rect(d, 0, 900, 1920, 1080, fill=(60, 64, 84))
    line(d, [(0, 900), (1920, 900)], width=9)
    for lx in range(40, 1920, 320):
        rect(d, lx, 990, lx + 170, 1004, fill=(230, 230, 220))
    lamp_post(d, 1180, 840)
    if hydrant_x:
        hx = hydrant_x
        rect(d, hx - 22, 770, hx + 22, 840, fill=RED, outline=INK, width=6, radius=8)
        rect(d, hx - 34, 790, hx + 34, 808, fill=RED, outline=INK, width=6, radius=6)
        circ(d, hx, 764, 20, fill=RED, outline=INK, width=6)
    if snow:
        rect(d, 0, 828, 1920, 846, fill=(240, 244, 250), radius=8)
        for _ in range(140):
            circ(d, random.randint(0, 1920), random.randint(0, 1080), random.choice([3, 4, 5, 6]), fill=(244, 248, 255))
    sc.glow(lambda g: poly(g, [(1236, 340), (1290, 340), (1520, 900), (1000, 900)], fill=(64, 56, 20)), blur=30)


def bg_warehouse(sc):
    bg_room(sc, wall=(72, 86, 112), floor=(104, 108, 120), stripes=False)
    d = sc.d
    for x in range(0, 1920, 46):
        line(d, [(x, 0), (x, 854)], fill=(64, 78, 104), width=5)
    for sx_ in (60, 1380):
        for sy in (330, 560, 790):
            rect(d, sx_, sy, sx_ + 480, sy + 18, fill=(60, 64, 80), outline=INK, width=6)
            for cx in range(sx_ + 20, sx_ + 420, 150):
                crate(d, cx, sy, 120, random.choice([110, 130, 150]))
        rect(d, sx_, 150, sx_ + 16, 880, fill=(60, 64, 80), outline=INK, width=5)
        rect(d, sx_ + 464, 150, sx_ + 480, 880, fill=(60, 64, 80), outline=INK, width=5)
    for lx in (640, 1240):
        line(d, [(lx, 0), (lx, 110)], width=6)
        poly(d, [(lx - 70, 170), (lx + 70, 170), (lx + 36, 110), (lx - 36, 110)], fill=(60, 60, 70), outline=INK, width=6)
    sc.glow(lambda g: [poly(g, [(lx - 60, 170), (lx + 60, 170), (lx + 330, 880), (lx - 330, 880)], fill=(60, 54, 24)) for lx in (640, 1240)], blur=34)


def bg_vault(sc, open_=False, cx=1380, cy=470):
    d = sc.d
    rect(d, 0, 0, 1920, 880, fill=(110, 120, 140))
    for x in range(0, 1920, 240):
        rect(d, x + 8, 8, x + 232, 872, fill=(124, 134, 154), outline=(90, 98, 118), width=6, radius=8)
        for yy in (40, 440, 840):
            for xx in (x + 30, x + 210):
                circ(d, xx, yy, 8, fill=(86, 94, 112))
    rect(d, 0, 880, 1920, 1080, fill=(84, 90, 106))
    line(d, [(0, 880), (1920, 880)], width=10)
    vault_door(d, cx, cy, 300, open_)


def bg_office(sc):
    bg_room(sc, wall=(190, 180, 150), floor=(110, 96, 84), stripes=False)
    d = sc.d
    # window with blinds
    rect(d, 120, 160, 620, 560, fill=(110, 170, 220), outline=INK, width=10)
    for by in range(180, 560, 34):
        rect(d, 126, by, 614, by + 16, fill=(236, 232, 214))
    # corkboard
    rect(d, 1180, 130, 1840, 580, fill=(200, 150, 90), outline=INK, width=10, radius=8)


def bg_prison(sc):
    d = sc.d
    rect(d, 0, 0, 1920, 880, fill=(110, 112, 122))
    for row, y in enumerate(range(0, 880, 80)):
        off = 0 if row % 2 else 90
        for x in range(-180 + off, 1920, 180):
            rect(d, x, y, x + 180, y + 80, outline=(88, 90, 100), width=5)
    rect(d, 1260, 150, 1560, 380, fill=(60, 110, 180), outline=INK, width=10)  # window
    for bx in range(1300, 1560, 60):
        rect(d, bx, 150, bx + 14, 380, fill=(50, 52, 60))
    rect(d, 0, 880, 1920, 1080, fill=(84, 86, 96))
    line(d, [(0, 880), (1920, 880)], width=10)
    # bunk
    rect(d, 60, 700, 620, 740, fill=(70, 72, 84), outline=INK, width=8)
    rect(d, 80, 650, 600, 704, fill=(210, 210, 200), outline=INK, width=7, radius=10)
    rect(d, 80, 740, 100, 880, fill=(70, 72, 84), outline=INK, width=6)
    rect(d, 580, 740, 600, 880, fill=(70, 72, 84), outline=INK, width=6)


def cell_bars(sc, x0=0, x1=1920, step=170):
    def draw(d):
        for bx in range(x0 + 40, x1, step):
            rect(d, bx, 0, bx + 24, 1080, fill=(52, 54, 64))
            rect(d, bx + 5, 0, bx + 11, 1080, fill=(96, 100, 116))
        rect(d, x0, 96, x1, 136, fill=(52, 54, 64))
    sc.prop(draw, rim_px=0)


def bg_junkyard(sc):
    vgrad(sc.rgb, (255, 170, 90), (255, 220, 150), 0, 760)
    d = sc.d
    circ(d, 1500, 300, 120, fill=(255, 240, 190))
    cols = [(170, 70, 60), (70, 110, 150), (190, 160, 70), (100, 130, 90), (120, 120, 130)]
    for row, by in enumerate((700, 620, 540)):
        for x in range(-40 + row * 70, 1100 - row * 140, 250):
            c = random.choice(cols)
            rect(d, x, by - 76, x + 230, by, fill=c, outline=INK, width=8, radius=22)
            rect(d, x + 50, by - 124, x + 180, by - 70, fill=shade(c, 0.85), outline=INK, width=7, radius=16)
    rect(d, 0, 780, 1920, 1080, fill=(150, 110, 80))
    line(d, [(0, 780), (1920, 780)], width=10)
    # crusher
    rect(d, 1240, 330, 1300, 800, fill=(90, 90, 100), outline=INK, width=8)
    rect(d, 1800, 330, 1860, 800, fill=(90, 90, 100), outline=INK, width=8)
    rect(d, 1220, 290, 1880, 350, fill=(230, 180, 40), outline=INK, width=9)
    rect(d, 1320, 350, 1780, 430, fill=(120, 120, 132), outline=INK, width=9)
    for hx in range(1330, 1780, 60):
        poly(d, [(hx, 430), (hx + 50, 430), (hx + 25, 468)], fill=(120, 120, 132), outline=INK, width=5)


def bg_card(sc, c1=(40, 60, 140), c2=(30, 46, 110), cx=960, cy=560, rays=18):
    d = sc.d
    rect(d, 0, 0, 1920, 1080, fill=c1)
    for k in range(rays):
        a0 = 2 * math.pi * k / rays
        a1 = a0 + math.pi / rays
        poly(d, [(cx, cy), (cx + 2400 * math.cos(a0), cy + 2400 * math.sin(a0)), (cx + 2400 * math.cos(a1), cy + 2400 * math.sin(a1))], fill=c2)
