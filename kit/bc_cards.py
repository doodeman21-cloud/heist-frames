"""Cards for 'GTA 6 vs the real Bonnie and Clyde'. Silhouettes, maps, documents only.
Sepia 1930s look for history, neon look for GTA 6 parts. No game art or logos."""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

OUT = sys.argv[1] if len(sys.argv) > 1 else "bonnie/cards"
os.makedirs(OUT, exist_ok=True)
W, H, S = 1920, 1080, 2
CREAM, RED, INK, GOLD = (238, 226, 200), (210, 58, 44), (14, 10, 7), (214, 170, 96)
PINK, TEAL = (255, 70, 160), (40, 220, 210)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FR = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def p(v): return int(round(v * S))
def font(f, s): return ImageFont.truetype(f, p(s))


class Card:
    def __init__(self, mode="sepia", seed=0):
        random.seed(seed); self.mode = mode
        a, b = ((26, 19, 13), (64, 48, 32)) if mode == "sepia" else ((12, 6, 26), (40, 12, 52))
        self.img = Image.new("RGB", (W * S, H * S)); d = ImageDraw.Draw(self.img)
        for y in range(H * S):
            t = y / (H * S); d.line([(0, y), (W * S, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)))
        self.d = ImageDraw.Draw(self.img)
        if mode == "neon":
            self.glow(1500, 300, 500, 300, (90, 20, 70), 160); self.glow(300, 900, 500, 260, (10, 60, 70), 160)
        else:
            self.glow(960, 420, 900, 420, (50, 36, 18), 200)
        self.fg = CREAM if mode == "sepia" else (245, 240, 250)
        self.acc = RED if mode == "sepia" else PINK

    def glow(self, x, y, rx, ry, col, blur=80):
        g = Image.new("RGB", self.img.size, (0, 0, 0))
        ImageDraw.Draw(g).ellipse([p(x - rx), p(y - ry), p(x + rx), p(y + ry)], fill=col)
        self.img = ImageChops.add(self.img, g.filter(ImageFilter.GaussianBlur(p(blur)))); self.d = ImageDraw.Draw(self.img)

    def text(self, x, y, s, size, fill=None, f=FB, anchor="la"):
        self.d.text((p(x), p(y)), s, font=font(f, size), fill=fill or self.fg, anchor=anchor)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=0, r=0):
        self.d.rounded_rectangle([p(x0), p(y0), p(x1), p(y1)], radius=p(r), fill=fill, outline=outline, width=p(w))

    def kicker(self, s, x=120, y=100):
        self.rect(x, y + 6, x + 10, y + 52, fill=self.acc); self.text(x + 30, y, s, 40, self.acc)

    def person(self, x, y, h, col=INK, woman=False, hat=False):
        d = self.d; hr = h * 0.075
        d.ellipse([p(x - hr), p(y - h), p(x + hr), p(y - h + hr * 2.2)], fill=col)
        if hat:
            d.rectangle([p(x - hr * 1.9), p(y - h + hr * 0.55), p(x + hr * 1.9), p(y - h + hr * 0.8)], fill=col)
            d.rounded_rectangle([p(x - hr * 1.05), p(y - h - hr * 0.5), p(x + hr * 1.05), p(y - h + hr * 0.7)], radius=p(4), fill=col)
        if woman:
            d.polygon([(p(x - hr * 1.2), p(y - h + hr)), (p(x + hr * 1.2), p(y - h + hr)), (p(x + hr * 1.4), p(y - h + hr * 3.2)), (p(x - hr * 1.4), p(y - h + hr * 3.2))], fill=col)
        d.rounded_rectangle([p(x - h * .06), p(y - h + hr * 2), p(x + h * .06), p(y - h + hr * 2.6)], radius=p(5), fill=col)
        d.rounded_rectangle([p(x - h * .19), p(y - h * .76), p(x + h * .19), p(y - h * .62)], radius=p(h * .06), fill=col)
        if woman:
            d.polygon([(p(x - h * .17), p(y - h * .72)), (p(x + h * .17), p(y - h * .72)), (p(x + h * .14), p(y - h * .42)), (p(x - h * .14), p(y - h * .42))], fill=col)
            d.polygon([(p(x - h * .14), p(y - h * .44)), (p(x + h * .14), p(y - h * .44)), (p(x + h * .27), p(y - h * .1)), (p(x - h * .27), p(y - h * .1))], fill=col)
            for s_ in (-1, 1):
                d.rectangle([p(x + s_ * h * .1 - h * .025), p(y - h * .12), p(x + s_ * h * .1 + h * .025), p(y)], fill=col)
        else:
            d.polygon([(p(x - h * .2), p(y - h * .74)), (p(x + h * .2), p(y - h * .74)), (p(x + h * .23), p(y - h * .3)), (p(x - h * .23), p(y - h * .3))], fill=col)
            for s_ in (-1, 1):
                d.polygon([(p(x + s_ * h * .02), p(y - h * .32)), (p(x + s_ * h * .17), p(y - h * .32)), (p(x + s_ * h * .15), p(y)), (p(x + s_ * h * .04), p(y))], fill=col)
        for s_ in (-1, 1):
            d.polygon([(p(x + s_ * h * .17), p(y - h * .72)), (p(x + s_ * h * .24), p(y - h * .68)), (p(x + s_ * h * .27), p(y - h * .36)), (p(x + s_ * h * .2), p(y - h * .36))], fill=col)

    def spotlight(self, x, top, bottom, w):
        g = Image.new("RGB", self.img.size, (0, 0, 0))
        ImageDraw.Draw(g).polygon([(p(x - 40), p(top)), (p(x + 40), p(top)), (p(x + w), p(bottom)), (p(x - w), p(bottom))], fill=(70, 58, 40) if self.mode == "sepia" else (60, 20, 60))
        self.img = ImageChops.add(self.img, g.filter(ImageFilter.GaussianBlur(p(30)))); self.d = ImageDraw.Draw(self.img)

    def car(self, x, y, w, col=INK, holes=False):
        d = self.d; h = w * 0.32
        d.rounded_rectangle([p(x), p(y - h * .55), p(x + w), p(y - h * .12)], radius=p(h * .15), fill=col)
        d.polygon([(p(x + w * .22), p(y - h * .55)), (p(x + w * .32), p(y - h)), (p(x + w * .66), p(y - h)), (p(x + w * .76), p(y - h * .55))], fill=col)
        d.polygon([(p(x - w * .02), p(y - h * .2)), (p(x + w * .2), p(y - h * .6)), (p(x + w * .2), p(y - h * .2))], fill=col)
        d.polygon([(p(x + w * 1.02), p(y - h * .2)), (p(x + w * .8), p(y - h * .6)), (p(x + w * .8), p(y - h * .2))], fill=col)
        for cx in (x + w * .2, x + w * .8):
            d.ellipse([p(cx - h * .26), p(y - h * .38), p(cx + h * .26), p(y + h * .14)], fill=col)
            d.ellipse([p(cx - h * .1), p(y - h * .22), p(cx + h * .1), p(y - h * .02)], fill=(70, 60, 48))
        if holes:
            random.seed(7)
            for _ in range(60):
                hx, hy = x + random.uniform(.05, .95) * w, y - random.uniform(.2, .95) * h
                if hy < y - h * .55 and not (x + w * .3 < hx < x + w * .7): continue
                d.ellipse([p(hx - 5), p(hy - 5), p(hx + 5), p(hy + 5)], fill=(200, 186, 160))

    def bars(self, x0, y0, x1, y1):
        for x in range(x0, x1, 70): self.rect(x, y0, x + 18, y1, fill=(10, 8, 6))
        self.rect(x0 - 20, y0, x1, y0 + 26, fill=(10, 8, 6)); self.rect(x0 - 20, (y0 + y1) // 2, x1, (y0 + y1) // 2 + 22, fill=(10, 8, 6))

    def paper(self, x, y, w, h, head, sub, rot=0):
        pl = Image.new("RGBA", (p(w), p(h)), (232, 222, 196, 255)); d = ImageDraw.Draw(pl)
        d.text((p(w / 2), p(30)), "THE DAILY TRIBUNE", font=font(FS, 34), fill=(30, 24, 18), anchor="ma")
        d.line([(p(30), p(84)), (p(w - 30), p(84))], fill=(30, 24, 18), width=p(3))
        yy = 110
        for line in head:
            d.text((p(w / 2), p(yy)), line, font=font(FS, 62), fill=(20, 16, 12), anchor="ma"); yy += 74
        d.rectangle([p(40), p(yy + 20), p(w * .55), p(h - 60)], fill=(150, 140, 120))
        d.text((p(w * .3), p(yy + 40)), sub, font=font(FR, 22), fill=(40, 34, 26), anchor="ma")
        for k in range(10):
            ly = yy + 30 + k * 26
            if ly < h - 60: d.rectangle([p(w * .6), p(ly), p(w - 40), p(ly + 8)], fill=(120, 110, 95))
        pl = pl.rotate(rot, expand=True, resample=Image.BICUBIC)
        sh = Image.new("RGBA", pl.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 140), mask=pl.split()[3])
        self.img.paste(sh.filter(ImageFilter.GaussianBlur(p(14))), (p(x + 16), p(y + 20)), sh.filter(ImageFilter.GaussianBlur(p(14))))
        self.img.paste(pl, (p(x), p(y)), pl); self.d = ImageDraw.Draw(self.img)

    def usmap(self, route=False, lines=False):
        # stylised central US block with a few states
        pts = [(560, 230), (1380, 230), (1420, 520), (1300, 760), (1080, 820), (900, 760), (700, 800), (520, 620)]
        self.d.polygon([(p(a), p(b)) for a, b in pts], fill=(84, 66, 44) if self.mode == "sepia" else (40, 20, 60), outline=self.fg, width=p(3))
        if lines:
            for xs in (760, 980, 1180):
                for yy in range(240, 800, 30): self.d.line([(p(xs), p(yy)), (p(xs), p(yy + 15))], fill=self.fg, width=p(3))
            self.d.line([(p(560), p(500)), (p(1400), p(500))], fill=(0, 0, 0, 0))
        names = [("TEXAS", 820, 690), ("OKLAHOMA", 860, 470), ("MISSOURI", 1180, 360), ("LOUISIANA", 1180, 700), ("KANSAS", 780, 300)]
        for n, a, b in names: self.text(a, b, n, 26, (200, 186, 160) if self.mode == "sepia" else (200, 180, 220), f=FR, anchor="mm")
        if route:
            r = [(820, 640), (900, 520), (1000, 430), (1180, 400), (1250, 520), (1100, 600), (1220, 690)]
            for i in range(len(r) - 1):
                self.d.line([(p(r[i][0]), p(r[i][1])), (p(r[i + 1][0]), p(r[i + 1][1]))], fill=self.acc, width=p(7))
            for a, b in r: self.d.ellipse([p(a - 14), p(b - 14), p(a + 14), p(b + 14)], fill=self.acc)

    def palms(self):
        for x, hh in ((160, 620), (1760, 680), (1640, 520)):
            self.d.line([(p(x), p(1080)), (p(x + 30), p(1080 - hh))], fill=(8, 4, 16), width=p(18))
            for a in range(0, 360, 45):
                ex, ey = x + 30 + math.cos(math.radians(a)) * 170, 1080 - hh + math.sin(math.radians(a)) * 60 + 40
                self.d.line([(p(x + 30), p(1080 - hh)), (p(ex), p(ey))], fill=(8, 4, 16), width=p(14))

    def save(self, name):
        im = self.img.resize((W, H), Image.LANCZOS)
        if self.mode == "sepia":
            n = Image.effect_noise((W, H), 22).convert("RGB"); im = Image.blend(im, ImageChops.multiply(im, n.point(lambda v: 160 + v // 3)), 0.35)
        v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-300, -200, W + 300, H + 200], fill=255)
        im = Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), v.filter(ImageFilter.GaussianBlur(160)))
        im.save(f"{OUT}/{name}.jpg", quality=92)


def neon_title(c, big, small):
    c.text(960, 330, big, 190, (255, 255, 255), anchor="mm")
    for dx, col in ((-5, TEAL), (5, PINK)): c.text(960 + dx, 330, big, 190, col, anchor="mm")
    c.text(960, 330, big, 190, (255, 245, 252), anchor="mm"); c.text(960, 500, small, 54, TEAL, anchor="mm")

c = Card("neon", 1); c.palms(); neon_title(c, "GTA 6", "OUT TODAY  ·  NOV 19, 2026"); c.save("b01")
c = Card("neon", 2); c.palms(); c.person(820, 840, 520, (6, 2, 14), woman=True); c.person(1100, 840, 560, (6, 2, 14)); c.text(960, 160, "LUCIA  &  JASON", 90, anchor="mm"); c.text(960, 250, "a couple robbing their way across 'Florida'", 40, TEAL, f=FR, anchor="mm"); c.save("b02")
c = Card("neon", 3); c.text(960, 250, "THE INSPIRATION", 50, TEAL, anchor="mm"); c.rect(460, 330, 1460, 640, outline=PINK, w=5, r=30); c.text(960, 430, "BONNIE", 110, anchor="mm"); c.text(960, 560, "& CLYDE", 110, PINK, anchor="mm"); c.text(960, 740, "according to Rockstar's head of narrative", 40, (200, 190, 220), f=FR, anchor="mm"); c.save("b03")
c = Card("sepia", 4); c.text(960, 380, "THE REAL STORY", 130, anchor="mm", f=FS); c.text(960, 520, "1930 – 1934", 60, GOLD, anchor="mm"); c.save("b04")
c = Card("sepia", 5); c.kicker("TEXAS · 1930"); c.text(120, 200, "The Great Depression", 90, f=FS)
for i, x in enumerate(range(300, 1700, 150)): c.person(x, 900, 360 + (i % 3) * 20, (12, 9, 6), hat=i % 2 == 0)
c.save("b05")
c = Card("sepia", 6); c.spotlight(1200, 0, 960, 380); c.person(1200, 930, 640, woman=True); c.kicker("BONNIE PARKER"); c.text(120, 200, "19", 220, GOLD); c.text(120, 470, "waitress", 52, f=FR); c.text(120, 540, "writes poetry", 52, f=FR); c.save("b06")
c = Card("sepia", 7); c.spotlight(1200, 0, 960, 380); c.person(1200, 930, 660, hat=True); c.kicker("CLYDE BARROW"); c.text(120, 200, "20", 220, GOLD); c.text(120, 470, "small-time thief", 52, f=FR); c.text(120, 540, "West Dallas", 52, f=FR); c.save("b07")
c = Card("sepia", 8); c.spotlight(960, 0, 960, 520); c.person(860, 930, 600, woman=True); c.person(1060, 930, 650, hat=True); c.text(960, 120, "JANUARY 1930", 56, GOLD, anchor="mm"); c.save("b08")
c = Card("sepia", 9); c.person(960, 960, 640, hat=True); c.bars(560, 140, 1400, 1000); c.rect(640, 70, 1280, 170, fill=RED, r=10); c.text(960, 120, "ARRESTED", 80, (250, 240, 230), anchor="mm"); c.save("b09")
c = Card("sepia", 10); c.bars(1000, 140, 1800, 1000); c.person(1350, 960, 620, hat=True); c.person(600, 960, 620, woman=True); c.text(120, 110, "SMUGGLED", 70, GOLD); c.text(120, 190, "A GUN INTO JAIL", 70); c.save("b10")
c = Card("sepia", 11); c.text(960, 260, "CAUGHT AGAIN", 110, anchor="mm", f=FS); c.rect(560, 380, 1360, 600, outline=CREAM, w=4, r=8); c.text(960, 440, "EASTHAM", 80, anchor="mm"); c.text(960, 540, "PRISON FARM · TEXAS", 44, GOLD, anchor="mm"); c.save("b11")
c = Card("sepia", 12); c.text(120, 110, "1932", 70, GOLD); c.text(960, 470, "\"never go back\"", 130, anchor="mm", f=FS); c.save("b12")
c = Card("sepia", 13); c.usmap(route=True); c.text(120, 90, "TWO-YEAR CRIME SPREE", 56, GOLD); c.text(120, 860, "banks · gas stations · grocery stores", 44, f=FR); c.save("b13")
c = Card("sepia", 14); c.text(960, 380, "$ A FEW HUNDRED", 140, anchor="mm", f=FS); c.text(960, 530, "per robbery, sometimes less", 50, GOLD, f=FR, anchor="mm"); c.save("b14")
c = Card("sepia", 15)
for k in range(8): c.rect(100 + k * 40, 700 + k * 14, 600 + k * 40, 708 + k * 14, fill=(120, 96, 66))
c.car(700, 860, 900); c.text(120, 110, "FAST CARS", 90, GOLD); c.save("b15")
c = Card("sepia", 16); c.usmap(lines=True); c.text(120, 90, "STATE LINES", 70, GOLD); c.text(120, 870, "local sheriffs couldn't follow", 46, f=FR); c.save("b16")
c = Card("sepia", 17); c.kicker("JOPLIN, MISSOURI · 1933"); d = c.d
c.rect(560, 520, 1360, 940, fill=(16, 12, 8)); d.polygon([(p(520), p(530)), (p(960), p(260)), (p(1400), p(530))], fill=(16, 12, 8))
for x in (660, 1160): c.rect(x, 620, x + 120, 760, fill=(220, 180, 100))
c.rect(900, 700, 1020, 940, fill=(40, 30, 20)); c.text(960, 200, "POLICE RAID", 70, RED, anchor="mm"); c.save("b17")
c = Card("sepia", 18); c.rect(260, 340, 1660, 740, fill=(20, 16, 12), r=10)
for x in range(280, 1660, 60): c.rect(x, 360, x + 30, 390, fill=(200, 186, 160)); c.rect(x, 690, x + 30, 720, fill=(200, 186, 160))
for i, x in enumerate(range(320, 1600, 330)):
    c.rect(x, 420, x + 280, 660, fill=(120, 104, 80)); c.person(x + 140, 655, 220, (30, 22, 14), woman=i % 2 == 0, hat=i % 2 == 1)
c.text(960, 180, "A ROLL OF FILM LEFT BEHIND", 64, GOLD, anchor="mm"); c.save("b18")
c = Card("sepia", 19); c.paper(560, 150, 820, 760, ["OUTLAW", "COUPLE"], "photos found in hideout", -4); c.save("b19")
c = Card("sepia", 20); c.img = Image.new("RGB", c.img.size, (12, 8, 6)); c.d = ImageDraw.Draw(c.img); c.text(960, 300, "THE REALITY", 60, GOLD, anchor="mm"); c.text(960, 470, "9+", 200, RED, anchor="mm"); c.text(960, 630, "police officers killed", 60, anchor="mm"); c.save("b20")
c = Card("sepia", 21); c.spotlight(1250, 0, 960, 380); c.person(1250, 940, 680, hat=True); c.kicker("1934"); c.text(120, 200, "FRANK HAMER", 100, f=FS); c.text(120, 340, "retired Texas Ranger", 52, GOLD, f=FR); c.text(120, 420, "tracked them for 3+ months", 46, f=FR); c.save("b21")
c = Card("sepia", 22); d = c.d; d.polygon([(p(860), p(560)), (p(1060), p(560)), (p(1700), p(1080)), (p(220), p(1080))], fill=(96, 78, 54))
for x in range(0, 1920, 90): d.ellipse([p(x - 80), p(500 + (x * 37) % 60), p(x + 80), p(700 + (x * 37) % 60)], fill=(30, 26, 16)) if not 700 < x < 1200 else None
c.glow(960, 470, 500, 120, (90, 70, 30), 120); c.text(960, 140, "MAY 23, 1934", 90, anchor="mm", f=FS); c.text(960, 250, "a country road in Louisiana", 48, GOLD, f=FR, anchor="mm"); c.save("b22")
c = Card("sepia", 23); c.img = Image.new("RGB", c.img.size, (14, 9, 6)); c.d = ImageDraw.Draw(c.img); c.text(960, 420, "100+", 240, RED, anchor="mm"); c.text(960, 600, "rounds fired in seconds", 60, anchor="mm"); c.save("b23")
c = Card("sepia", 24); c.text(560, 300, "BONNIE", 60, GOLD, anchor="mm"); c.text(1360, 300, "CLYDE", 60, GOLD, anchor="mm"); c.text(560, 500, "23", 240, anchor="mm", f=FS); c.text(1360, 500, "25", 240, anchor="mm", f=FS); c.rect(955, 260, 965, 700, fill=(120, 100, 70)); c.save("b24")
c = Card("sepia", 25)
for i in range(22): c.person(80 + i * 85 + (i % 2) * 30, 1000 + (i % 3) * 30, 420 + (i * 37) % 120, (14 + i % 3 * 4, 10, 7), hat=i % 3 == 0, woman=i % 4 == 1)
c.text(960, 160, "CROWDS TOOK SOUVENIRS", 76, anchor="mm", f=FS); c.save("b25")
c = Card("sepia", 26); c.spotlight(960, 0, 900, 700); c.car(460, 860, 1000, (24, 18, 12), holes=True); c.text(960, 150, "THE CAR IS STILL ON DISPLAY", 66, GOLD, anchor="mm"); c.save("b26")
a = Card("sepia", 27); b = Card("neon", 27)
a.paper(180, 220, 560, 620, ["OUTLAWS"], "1934", -3); a.text(480, 120, "1934", 70, GOLD, anchor="mm")
b.rect(1250, 200, 1600, 900, fill=(10, 4, 20), outline=TEAL, w=6, r=40); b.person(1425, 820, 420, PINK, woman=True); b.text(1425, 120, "2026", 70, TEAL, anchor="mm")
m = Image.new("L", a.img.size, 0); ImageDraw.Draw(m).polygon([(0, 0), (p(1000), 0), (p(900), p(1080)), (0, p(1080))], fill=255)
b.img = Image.composite(a.img, b.img, m); b.d = ImageDraw.Draw(b.img); b.d.line([(p(1000), 0), (p(900), p(1080))], fill=(255, 255, 255), width=p(6)); b.save("b27")
c = Card("neon", 28); c.palms(); c.rect(760, 150, 1160, 900, fill=(10, 4, 20), outline=PINK, w=6, r=44); c.d.polygon([(p(910), p(240)), (p(910), p(360)), (p(1020), p(300))], fill=PINK); c.text(960, 470, "VIRAL", 80, anchor="mm"); c.text(960, 560, "millions of views", 36, TEAL, f=FR, anchor="mm")
for k in range(3): c.rect(830, 660 + k * 60, 1090 - k * 50, 690 + k * 60, fill=(70, 40, 90), r=12)
c.save("b28")
c = Card("neon", 29); c.palms(); c.text(960, 380, "HOW WILL", 130, anchor="mm"); c.text(960, 530, "IT END?", 130, PINK, anchor="mm"); c.save("b29")
c = Card("sepia", 30); c.text(960, 360, "MORE TRUE CRIME", 100, anchor="mm", f=FS); c.rect(700, 470, 1220, 590, fill=RED, r=60); c.text(960, 530, "SUBSCRIBE", 60, (250, 240, 230), anchor="mm"); c.save("b30")
print("cards done")
