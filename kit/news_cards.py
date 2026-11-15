"""Explainer graphics for the Nvidia CEO story. Dark newsroom look, green accent.
No real people are depicted: only silhouettes, documents, charts and buildings."""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

OUT = sys.argv[1] if len(sys.argv) > 1 else "nvidia/cards"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
S = 2
GREEN = (118, 185, 0)
RED = (232, 76, 60)
WHITE = (240, 240, 236)
MUTED = (150, 158, 170)
BG0, BG1 = (10, 14, 22), (22, 30, 44)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FR = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def p(v): return int(round(v * S))
def font(path, size): return ImageFont.truetype(path, p(size))


class Card:
    def __init__(self, seed=0, tint=None):
        random.seed(seed)
        self.img = Image.new("RGB", (W * S, H * S), BG0)
        d = ImageDraw.Draw(self.img)
        for y in range(H * S):
            t = y / (H * S)
            d.line([(0, y), (W * S, y)], fill=tuple(int(BG0[i] + (BG1[i] - BG0[i]) * t) for i in range(3)))
        for x in range(0, W, 80):
            d.line([(p(x), 0), (p(x), H * S)], fill=(20, 27, 40), width=p(1))
        for y in range(0, H, 80):
            d.line([(0, p(y)), (W * S, p(y))], fill=(20, 27, 40), width=p(1))
        if tint:
            self.glow(960, 540, 900, 500, tint, 200)
        self.d = ImageDraw.Draw(self.img)

    def glow(self, x, y, rx, ry, col, blur=80):
        g = Image.new("RGB", self.img.size, (0, 0, 0))
        ImageDraw.Draw(g).ellipse([p(x - rx), p(y - ry), p(x + rx), p(y + ry)], fill=col)
        self.img = ImageChops.add(self.img, g.filter(ImageFilter.GaussianBlur(p(blur))))
        self.d = ImageDraw.Draw(self.img)

    def text(self, x, y, s, size, fill=WHITE, f=FB, anchor="la"):
        self.d.text((p(x), p(y)), s, font=font(f, size), fill=fill, anchor=anchor)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=0, r=0):
        self.d.rounded_rectangle([p(x0), p(y0), p(x1), p(y1)], radius=p(r), fill=fill, outline=outline, width=p(w))

    def kicker(self, s, x=120, y=110, col=GREEN):
        self.rect(x, y + 6, x + 10, y + 52, fill=col)
        self.text(x + 30, y, s, 40, col)

    def date(self, s, x=120, y=110):
        self.rect(x, y, x + 34 + len(s) * 30, y + 70, fill=GREEN, r=10)
        self.text(x + 18, y + 6, s, 46, (8, 12, 18))

    def silhouette(self, x, y, h, col=(4, 6, 10), jacket=True):
        d = self.d
        hr = h * 0.075
        d.ellipse([p(x - hr), p(y - h), p(x + hr), p(y - h + hr * 2.2)], fill=col)
        d.rounded_rectangle([p(x - h * 0.06), p(y - h + hr * 2), p(x + h * 0.06), p(y - h + hr * 2.6)], radius=p(5), fill=col)
        d.polygon([(p(x - h * 0.2), p(y - h * 0.74)), (p(x + h * 0.2), p(y - h * 0.74)),
                   (p(x + h * 0.24), p(y - h * 0.3)), (p(x - h * 0.24), p(y - h * 0.3))], fill=col)
        d.rounded_rectangle([p(x - h * 0.2), p(y - h * 0.76), p(x + h * 0.2), p(y - h * 0.62)], radius=p(h * 0.06), fill=col)
        for s_ in (-1, 1):
            d.polygon([(p(x + s_ * h * 0.19), p(y - h * 0.72)), (p(x + s_ * h * 0.26), p(y - h * 0.68)),
                       (p(x + s_ * h * 0.29), p(y - h * 0.34)), (p(x + s_ * h * 0.22), p(y - h * 0.34))], fill=col)
            d.polygon([(p(x + s_ * h * 0.02), p(y - h * 0.32)), (p(x + s_ * h * 0.17), p(y - h * 0.32)),
                       (p(x + s_ * h * 0.15), p(y)), (p(x + s_ * h * 0.04), p(y))], fill=col)

    def chip(self, cx, cy, s, lit=True):
        d = self.d
        if lit:
            self.glow(cx, cy, s * 1.2, s * 1.2, (40, 70, 0), 90); d = self.d
        for k in range(-5, 6):
            o = k * s * 0.17
            for a, b in (((cx + o, cy - s * 1.05), (cx + o, cy - s * 0.8)), ((cx + o, cy + s * 0.8), (cx + o, cy + s * 1.05)),
                         ((cx - s * 1.05, cy + o), (cx - s * 0.8, cy + o)), ((cx + s * 0.8, cy + o), (cx + s * 1.05, cy + o))):
                d.line([(p(a[0]), p(a[1])), (p(b[0]), p(b[1]))], fill=(170, 176, 186), width=p(s * 0.05))
        d.rounded_rectangle([p(cx - s * 0.82), p(cy - s * 0.82), p(cx + s * 0.82), p(cy + s * 0.82)], radius=p(s * 0.08), fill=(34, 40, 52), outline=(90, 98, 112), width=p(4))
        d.rounded_rectangle([p(cx - s * 0.5), p(cy - s * 0.5), p(cx + s * 0.5), p(cy + s * 0.5)], radius=p(s * 0.05), fill=(18, 22, 30), outline=GREEN, width=p(5))
        for k in range(1, 4):
            o = -s * 0.5 + k * s * 0.25
            d.line([(p(cx - s * 0.5), p(cy + o)), (p(cx + s * 0.5), p(cy + o))], fill=(40, 60, 20), width=p(2))
            d.line([(p(cx + o), p(cy - s * 0.5)), (p(cx + o), p(cy + s * 0.5))], fill=(40, 60, 20), width=p(2))

    def paper(self, x, y, w, h, outlet, head, sub=None, rot=0):
        layer = Image.new("RGBA", (p(w + 60), p(h + 60)), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rectangle([p(30), p(30), p(w + 30), p(h + 30)], fill=(236, 232, 222))
        ld.text((p(30 + w / 2), p(70)), outlet, font=font(FS, 44), fill=(20, 20, 24), anchor="ma")
        ld.line([(p(60), p(140)), (p(w), p(140))], fill=(20, 20, 24), width=p(3))
        yy = 168
        for line in head:
            ld.text((p(64), p(yy)), line, font=font(FS, 50), fill=(16, 16, 20)); yy += 66
        if sub:
            ld.text((p(64), p(yy + 8)), sub, font=font(FR, 26), fill=(80, 80, 86)); yy += 50
        random.seed(len(outlet) + len(head))
        while yy < h - 20:
            ld.rectangle([p(64), p(yy + 10), p(64 + random.randint(int(w * .55), int(w * .85))), p(yy + 22)], fill=(180, 176, 168)); yy += 34
        layer = layer.rotate(rot, resample=Image.BICUBIC, expand=True)
        sh = Image.new("RGBA", layer.size, (0, 0, 0, 0)); sh.putalpha(layer.split()[3].point(lambda a: int(a * .55)))
        sh = Image.composite(Image.new("RGBA", layer.size, (0, 0, 0, 255)), sh, sh).filter(ImageFilter.GaussianBlur(p(18)))
        base = self.img.convert("RGBA")
        base.alpha_composite(sh, (p(x + 18), p(y + 26))); base.alpha_composite(layer, (p(x), p(y)))
        self.img = base.convert("RGB"); self.d = ImageDraw.Draw(self.img)

    def chart(self, x0, y0, x1, y1, pts, col=RED, labels=()):
        d = self.d
        d.rounded_rectangle([p(x0), p(y0), p(x1), p(y1)], radius=p(16), fill=(14, 19, 29), outline=(40, 50, 66), width=p(2))
        for k in range(1, 4):
            yy = y0 + (y1 - y0) * k / 4
            d.line([(p(x0 + 20), p(yy)), (p(x1 - 20), p(yy))], fill=(30, 38, 52), width=p(2))
        n = len(pts)
        xy = [(p(x0 + 40 + (x1 - x0 - 80) * i / (n - 1)), p(y0 + 40 + (y1 - y0 - 80) * (1 - v))) for i, v in enumerate(pts)]
        poly = xy + [(xy[-1][0], p(y1 - 20)), (xy[0][0], p(y1 - 20))]
        fl = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(fl).polygon(poly, fill=col + (46,))
        base = self.img.convert("RGBA"); base.alpha_composite(fl); self.img = base.convert("RGB"); d = self.d = ImageDraw.Draw(self.img)
        d.line(xy, fill=col, width=p(7), joint="curve")
        d.ellipse([xy[-1][0] - p(12), xy[-1][1] - p(12), xy[-1][0] + p(12), xy[-1][1] + p(12)], fill=col)
        for (i, s, c) in labels:
            self.text(xy[i][0] / S + 16, xy[i][1] / S - 70, s, 44, c)

    def capitol(self, cx, base, s, col=(36, 46, 64)):
        d = self.d
        d.rectangle([p(cx - s * 2.2), p(base - s * 0.55), p(cx + s * 2.2), p(base)], fill=col)
        for k in range(-9, 10):
            d.rectangle([p(cx + k * s * 0.22 - s * 0.04), p(base - s * 0.5), p(cx + k * s * 0.22 + s * 0.04), p(base - s * 0.06)], fill=tuple(c + 18 for c in col))
        d.rectangle([p(cx - s * 0.75), p(base - s * 0.85), p(cx + s * 0.75), p(base - s * 0.55)], fill=col)
        d.pieslice([p(cx - s * 0.62), p(base - s * 1.55), p(cx + s * 0.62), p(base - s * 0.35)], 180, 360, fill=col)
        d.rectangle([p(cx - s * 0.05), p(base - s * 1.85), p(cx + s * 0.05), p(base - s * 1.5)], fill=col)
        d.ellipse([p(cx - s * 0.09), p(base - s * 1.95), p(cx + s * 0.09), p(base - s * 1.8)], fill=col)

    def save(self, name):
        img = self.img.resize((W, H), Image.LANCZOS)
        vig = Image.new("L", (W, H), 0)
        ImageDraw.Draw(vig).ellipse([-260, -220, W + 260, H + 220], fill=255)
        img = Image.composite(img, Image.new("RGB", (W, H), (2, 3, 6)), vig.filter(ImageFilter.GaussianBlur(160)))
        noise = Image.effect_noise((W, H), 18).convert("RGB")
        img = Image.blend(img, ImageChops.multiply(img, noise), 0.12)
        img.save(os.path.join(OUT, name + ".jpg"), quality=92)


def stage(c, x=1280, empty=False):
    c.d.polygon([(p(x - 90), 0), (p(x + 90), 0), (p(x + 420), p(1000)), (p(x - 420), p(1000))], fill=(30, 38, 50))
    c.glow(x, 990, 430, 70, (60, 70, 80), 50)
    if not empty:
        c.silhouette(x, 990, 640)


cards = []
def card(f): cards.append(f); return f

@card
def c01():
    c = Card(1, (10, 30, 0)); stage(c)
    c.kicker("ONE WEEK AGO"); c.text(120, 190, "THE MOST POWERFUL", 76); c.text(120, 280, "PERSON IN TECH?", 76)
    c.text(120, 420, "Co-founded Nvidia · 1993", 40, MUTED, FR); c.save("c01")

@card
def c02():
    c = Card(2); c.chip(1300, 540, 300)
    c.kicker("NVIDIA"); c.text(120, 200, "$4 TRILLION", 120, GREEN); c.text(120, 360, "The chips behind", 56); c.text(120, 432, "almost every AI system", 56); c.save("c02")

@card
def c03():
    c = Card(3); stage(c, empty=True)
    c.text(120, 300, "TODAY:", 70, MUTED); c.text(120, 380, "HE'S OUT.", 150, RED); c.save("c03")

@card
def c04():
    c = Card(4); c.text(960, 190, "WHAT ACTUALLY HAPPENED?", 84, WHITE, anchor="ma")
    c.d.line([(p(220), p(620)), (p(1700), p(620))], fill=(60, 72, 90), width=p(8))
    for i, (x, lab) in enumerate(((260, "OCT 29"), (720, "NOV 8"), (1060, "NOV 11"), (1400, "NOV 12"), (1660, "DEC 1"))):
        col = RED if lab == "NOV 12" else GREEN
        c.d.ellipse([p(x - 22), p(598), p(x + 22), p(642)], fill=col)
        c.text(x, 670, lab, 40, WHITE, anchor="ma")
    c.save("c04")

@card
def c05():
    c = Card(5)
    c.d.ellipse([p(1130), p(240), p(1730), p(840)], outline=(40, 54, 72), width=p(3))
    for k in range(1, 4):
        r = 300 * k / 4; c.d.ellipse([p(1430 - r), p(540 - r), p(1430 + r), p(540 + r)], outline=(32, 44, 60), width=p(2))
    c.glow(1430, 540, 70, 70, (60, 90, 0), 30); c.d.ellipse([p(1412), p(522), p(1448), p(558)], fill=GREEN)
    c.text(1430, 590, "SINGAPORE", 34, WHITE, anchor="ma")
    c.kicker("IT STARTS WITH"); c.text(120, 200, "MEGASPEED", 110); c.text(120, 350, "Data center firm · Singapore", 44, MUTED, FR); c.text(120, 410, "An Nvidia customer", 44, MUTED, FR); c.save("c05")

@card
def c06():
    c = Card(6); c.chip(420, 560, 170, lit=False)
    c.d.line([(p(650), p(560)), (p(1290), p(560))], fill=GREEN, width=p(10))
    c.d.polygon([(p(1290), p(520)), (p(1360), p(560)), (p(1290), p(600))], fill=GREEN)
    c.rect(930, 400, 990, 720, fill=RED, r=8); c.text(960, 740, "U.S. EXPORT LIMITS", 34, RED, anchor="ma")
    c.text(1560, 520, "CHINA", 70, WHITE, anchor="ma")
    c.text(960, 120, "Did it help get around U.S. chip limits?", 54, WHITE, anchor="ma")
    c.text(960, 880, "U.S. investigation since late 2024", 40, MUTED, FR, anchor="ma"); c.save("c06")

@card
def c07():
    c = Card(7); c.date("OCT 29")
    c.paper(820, 140, 900, 760, "The New York Times", ["A \"close relationship\"", "with a former", "Megaspeed executive"], rot=-3)
    c.text(120, 280, "THE FIRST", 70); c.text(120, 360, "REPORT", 70, GREEN); c.save("c07")

@card
def c08():
    c = Card(8, (30, 4, 0))
    c.rect(560, 200, 1360, 900, fill=(196, 160, 96), r=14); c.rect(560, 160, 860, 230, fill=(196, 160, 96), r=14)
    c.rect(600, 250, 1320, 860, fill=(236, 232, 222))
    for k in range(9): c.rect(650, 470 + k * 40, 650 + random.randint(400, 600), 484 + k * 40, fill=(170, 166, 158))
    lay = Image.new("RGBA", (p(700), p(170)), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([p(6), p(6), p(694), p(164)], radius=p(12), outline=RED + (255,), width=p(10))
    ld.text((p(350), p(85)), "CLASSIFIED", font=font(FB, 92), fill=RED + (255,), anchor="mm")
    lay = lay.rotate(12, expand=True, resample=Image.BICUBIC)
    b = c.img.convert("RGBA"); b.alpha_composite(lay, (p(600), p(250))); c.img = b.convert("RGB"); c.d = ImageDraw.Draw(c.img)
    c.text(960, 940, "A secret U.S. memo, according to the Times", 42, WHITE, FR, anchor="ma"); c.save("c08")

@card
def c09():
    c = Card(9)
    c.rect(160, 260, 900, 760, fill=(16, 22, 34), outline=GREEN, w=3, r=20)
    c.text(530, 330, "NOT CHARGED", 70, GREEN, anchor="ma"); c.text(530, 450, "with spying", 46, WHITE, FR, anchor="ma")
    c.rect(1020, 260, 1760, 760, fill=(16, 22, 34), outline=RED, w=3, r=20)
    c.text(1390, 330, "CHINA:", 70, RED, anchor="ma"); c.text(1390, 450, "\"groundless,", 46, WHITE, FR, anchor="ma"); c.text(1390, 520, "a smear\"", 46, WHITE, FR, anchor="ma")
    c.text(960, 140, "ALLEGATION, NOT PROOF", 60, MUTED, anchor="ma"); c.save("c09")

@card
def c10():
    c = Card(10); c.date("NOV 8 · SUNDAY")
    c.rect(980, 220, 1760, 860, fill=(236, 236, 240), r=24); c.rect(980, 220, 1760, 320, fill=(46, 56, 74), r=24); c.rect(980, 280, 1760, 320, fill=(46, 56, 74))
    c.text(1030, 245, "To: All Nvidia employees", 34, WHITE, FR)
    for k in range(10): c.rect(1040, 380 + k * 44, 1040 + random.randint(380, 640), 396 + k * 44, fill=(170, 172, 180))
    c.text(120, 260, "HE ADMITS", 90); c.text(120, 370, "AN AFFAIR", 90, GREEN); c.save("c10")

@card
def c11():
    c = Card(11)
    c.d.ellipse([p(360), p(560), p(1560), p(860)], fill=(40, 30, 22))
    for x, y, h in ((520, 700, 380), (760, 640, 360), (1160, 640, 360), (1400, 700, 380), (960, 620, 340)):
        c.silhouette(x, y + 100, h, (6, 8, 12))
    c.d.ellipse([p(380), p(600), p(1540), p(880)], fill=(52, 38, 28))
    c.kicker("SAME DAY"); c.text(120, 190, "BOARD OPENS AN INVESTIGATION", 64); c.save("c11")

@card
def c12():
    c = Card(12); c.kicker("MONDAY, NOV 9")
    c.chart(220, 320, 1700, 920, [0.78, 0.8, 0.79, 0.82, 0.8, 0.44, 0.38, 0.4, 0.36], RED, [(8, "-5%+", RED)])
    c.text(120, 190, "NVIDIA STOCK FALLS", 72); c.save("c12")

@card
def c13():
    c = Card(13); c.date("NOV 11")
    c.paper(860, 160, 860, 720, "The New York Times", ["A second affair,", "with a senior", "Nvidia executive"], rot=3)
    c.text(120, 300, "REPORT", 70); c.text(120, 380, "No. 2", 120, RED); c.save("c13")

@card
def c14():
    c = Card(14, (24, 6, 0))
    c.d.rectangle([p(0), p(640), p(1920), p(1080)], fill=(30, 22, 18))
    for x in (520, 760, 1160, 1400): c.silhouette(x, 760, 420, (6, 8, 12))
    c.rect(780, 120, 1140, 360, fill=(14, 19, 29), outline=(60, 70, 86), w=3, r=10)
    c.text(960, 200, "?", 120, RED, anchor="ma")
    c.text(960, 860, "The board weighs his future", 56, WHITE, anchor="ma"); c.save("c14")

@card
def c15():
    c = Card(15, (40, 4, 0)); c.date("NOV 12 · THURSDAY")
    c.text(120, 300, "RESIGNED", 190, RED)
    for i, s in enumerate(("CEO", "PRESIDENT", "BOARD")):
        c.rect(130 + i * 400, 560, 470 + i * 400, 660, outline=WHITE, w=3, r=12)
        c.text(300 + i * 400, 583, s, 46, WHITE, anchor="ma")
        c.d.line([(p(140 + i * 400), p(610)), (p(460 + i * 400), p(610))], fill=RED, width=p(8))
    c.text(120, 760, "After 33 years", 60, MUTED, FR); c.save("c15")

@card
def c16():
    c = Card(16); stage(c, x=1350)
    c.kicker("INTERIM CEO"); c.text(120, 200, "COLETTE KRESS", 96); c.text(120, 330, "Nvidia's chief financial officer", 46, MUTED, FR); c.save("c16")

@card
def c17():
    c = Card(17); c.kicker("THURSDAY'S TRADING")
    c.chart(220, 300, 1700, 940, [0.82, 0.8, 0.5, 0.2, 0.14, 0.28, 0.42, 0.52, 0.56], RED, [(4, "-13%", RED), (8, "-4%", WHITE)])
    c.text(120, 190, "DOWN AS MUCH AS 13%", 66); c.save("c17")

@card
def c18():
    c = Card(18); c.date("NOV 12 · AFTERNOON")
    c.paper(860, 180, 860, 700, "Reuters", ["A third relationship,", "with another", "Nvidia employee"], rot=-2)
    c.text(120, 320, "REPORT", 70); c.text(120, 400, "No. 3", 120, RED); c.save("c18")

@card
def c19():
    c = Card(19, (0, 10, 30)); c.capitol(1300, 900, 300)
    c.date("DEC 1"); c.text(120, 230, "CONGRESS", 100); c.text(120, 360, "Closed-door interview", 50, MUTED, FR); c.text(120, 425, "3 House committees", 50, MUTED, FR)
    c.text(120, 540, "HE AGREED TO TESTIFY", 54, GREEN); c.save("c19")

@card
def c20():
    c = Card(20)
    cx, cy = 1340, 560
    c.d.line([(p(cx), p(cy - 300)), (p(cx), p(cy + 280))], fill=(150, 156, 168), width=p(14))
    c.d.line([(p(cx - 300), p(cy - 220)), (p(cx + 300), p(cy - 220))], fill=(150, 156, 168), width=p(12))
    for sx in (-300, 300):
        c.d.line([(p(cx + sx), p(cy - 220)), (p(cx + sx - 90), p(cy - 20))], fill=(150, 156, 168), width=p(4))
        c.d.line([(p(cx + sx), p(cy - 220)), (p(cx + sx + 90), p(cy - 20))], fill=(150, 156, 168), width=p(4))
        c.d.pieslice([p(cx + sx - 110), p(cy - 80), p(cx + sx + 110), p(cy + 40)], 0, 180, fill=(150, 156, 168))
    c.rect(cx - 160, cy + 270, cx + 160, cy + 310, fill=(150, 156, 168), r=10)
    c.kicker("U.S. JUSTICE DEPARTMENT"); c.text(120, 210, "A SPY?", 120); c.text(120, 380, "\"Not yet determined\"", 60, GREEN, FR); c.save("c20")

@card
def c21():
    c = Card(21)
    c.rect(160, 260, 900, 780, fill=(16, 22, 34), outline=(60, 70, 86), w=3, r=20)
    c.text(530, 320, "PRESIDENT TRUMP", 50, MUTED, anchor="ma"); c.text(530, 470, "\"So sad\"", 100, WHITE, anchor="ma")
    c.rect(1020, 260, 1760, 780, fill=(16, 22, 34), outline=GREEN, w=3, r=20)
    c.text(1390, 320, "HIS PICK TO REPLACE HIM", 44, MUTED, anchor="ma"); c.text(1390, 470, "Tim Cook", 100, GREEN, anchor="ma"); c.text(1390, 620, "of Apple", 50, WHITE, FR, anchor="ma")
    c.save("c21")

@card
def c22():
    c = Card(22); c.text(120, 130, "WHAT HAPPENS NOW?", 90)
    for i, (s, sub) in enumerate((("Board investigation", "still running"), ("Quarterly earnings", "this week"), ("Congress", "December 1"))):
        y = 340 + i * 200
        c.rect(120, y, 220, y + 100, outline=GREEN, w=5, r=14)
        c.text(270, y - 4, s, 64); c.text(270, y + 72, sub, 40, MUTED, FR)
    c.save("c22")

@card
def c23():
    c = Card(23); c.chip(960, 600, 190)
    for (x, y, s) in ((330, 300, "JAPAN"), (1590, 300, "SOUTH KOREA"), (330, 860, "TAIWAN"), (1590, 860, "CHINA")):
        c.d.line([(p(x), p(y)), (p(960), p(600))], fill=(50, 64, 84), width=p(3))
        c.rect(x - 200, y - 50, x + 200, y + 50, fill=(16, 22, 34), outline=GREEN, w=3, r=14); c.text(x, y - 26, s, 42, WHITE, anchor="ma")
    c.text(960, 90, "GOVERNMENTS ARE WATCHING", 64, WHITE, anchor="ma"); c.save("c23")

@card
def c24():
    c = Card(24, (36, 0, 0)); c.chip(960, 330, 170)
    c.text(960, 580, "DID ANY SECRETS", 96, WHITE, anchor="ma"); c.text(960, 700, "LEAVE THE COMPANY?", 96, RED, anchor="ma"); c.save("c24")

@card
def c25():
    c = Card(25, (10, 30, 0)); c.capitol(960, 760, 200, (30, 40, 56))
    c.text(960, 140, "WE'LL COVER THE HEARING", 76, WHITE, anchor="ma")
    c.rect(700, 830, 1220, 950, fill=(204, 30, 30), r=20); c.text(960, 852, "SUBSCRIBE", 66, WHITE, anchor="ma"); c.save("c25")

for f in cards:
    f(); print(f.__name__, flush=True)
