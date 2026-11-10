"""Cinematic silhouette kit: realistic-proportion figures, soft light, muted colour, film grain.
All coordinates are in 1920x1080 space; drawing is supersampled 2x."""
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

S = 2
W, H = 1920 * S, 1080 * S
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DARK = (16, 17, 22)


def p(v):
    return int(round(v * S))


def pts(seq):
    return [(p(x), p(y)) for x, y in seq]


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


POSES = {
    "stand": dict(hip=(0, .52), neck=(0, .86), head=(0, .935), sL=(-.11, .84), sR=(.11, .84), eL=(-.14, .66), eR=(.14, .66),
                  hL=(-.13, .5), hR=(.13, .5), kL=(-.085, .27), kR=(.085, .27), fL=(-.09, 0), fR=(.09, 0)),
    "walk": dict(hip=(0, .52), neck=(.02, .86), head=(.03, .935), sL=(-.09, .84), sR=(.12, .84), eL=(-.15, .67), eR=(.17, .68),
                 hL=(-.2, .54), hR=(.24, .56), kL=(-.1, .27), kR=(.1, .29), fL=(-.2, .02), fR=(.13, 0)),
    "carry": dict(hip=(0, .52), neck=(.03, .85), head=(.05, .925), sL=(-.08, .83), sR=(.13, .83), eL=(-.05, .93), eR=(.2, .93),
                  hL=(.0, 1.0), hR=(.12, 1.0), kL=(-.09, .27), kR=(.09, .28), fL=(-.17, .01), fR=(.12, 0)),
    "dig": dict(hip=(0, .5), neck=(.17, .79), head=(.24, .85), sL=(.08, .8), sR=(.25, .76), eL=(.2, .62), eR=(.31, .6),
                hL=(.27, .47), hR=(.37, .43), kL=(-.07, .26), kR=(.1, .28), fL=(-.11, 0), fR=(.15, 0)),
    "crawl": dict(hip=(-.25, .2), neck=(.15, .27), head=(.26, .31), sL=(.1, .29), sR=(.16, .24), eL=(.2, .13), eR=(.26, .14),
                  hL=(.31, .02), hR=(.38, .03), kL=(-.2, .03), kR=(-.32, .04), fL=(-.46, .03), fR=(-.57, .03)),
    "cuffed": dict(hip=(0, .52), neck=(.01, .85), head=(.03, .92), sL=(-.11, .83), sR=(.11, .83), eL=(-.13, .66), eR=(.11, .66),
                   hL=(-.04, .53), hR=(.02, .53), kL=(-.085, .27), kR=(.085, .27), fL=(-.09, 0), fR=(.09, 0)),
    "reach": dict(hip=(0, .52), neck=(0, .86), head=(0, .93), sL=(-.11, .85), sR=(.11, .85), eL=(-.13, 1.0), eR=(.12, 1.0),
                  hL=(-.05, 1.15), hR=(.06, 1.15), kL=(-.085, .27), kR=(.085, .27), fL=(-.1, 0), fR=(.1, 0)),
    "drag": dict(hip=(0, .48), neck=(-.15, .79), head=(-.2, .86), sL=(-.2, .8), sR=(-.08, .77), eL=(-.04, .68), eR=(.02, .66),
                 hL=(.12, .6), hR=(.16, .58), kL=(.07, .26), kR=(-.09, .25), fL=(.15, 0), fR=(-.13, 0)),
    "sit": dict(hip=(0, .3), neck=(.02, .62), head=(.04, .7), sL=(-.1, .6), sR=(.12, .6), eL=(-.1, .44), eR=(.16, .44),
                hL=(.02, .34), hR=(.22, .34), kL=(.18, .3), kR=(.2, .29), fL=(.2, 0), fR=(.24, 0)),
    "lie": dict(hip=(0, .06), neck=(.34, .07), head=(.42, .08), sL=(.32, .1), sR=(.32, .04), eL=(.2, .04), eR=(.22, .03),
                hL=(.08, .03), hR=(.1, .02), kL=(-.26, .05), kR=(-.25, .04), fL=(-.5, .03), fR=(-.52, .02)),
}


class Scene:
    def __init__(self, seed=0):
        random.seed(seed)
        self.img = Image.new("RGB", (W, H), DARK)
        self.d = ImageDraw.Draw(self.img)

    # ---- primitives -------------------------------------------------
    def grad(self, top, bottom, y0=0, y1=1080):
        for y in range(p(y0), p(y1)):
            t = (y - p(y0)) / max(1, p(y1) - p(y0))
            self.d.line([(0, y), (W, y)], fill=mix(top, bottom, t))

    def rect(self, x0, y0, x1, y1, fill, outline=None, width=0, r=0):
        if r:
            self.d.rounded_rectangle([p(x0), p(y0), p(x1), p(y1)], radius=p(r), fill=fill, outline=outline, width=p(width))
        else:
            self.d.rectangle([p(x0), p(y0), p(x1), p(y1)], fill=fill, outline=outline, width=p(width))

    def poly(self, seq, fill):
        self.d.polygon(pts(seq), fill=fill)

    def ell(self, x0, y0, x1, y1, fill):
        self.d.ellipse([p(x0), p(y0), p(x1), p(y1)], fill=fill)

    def line(self, seq, fill, width=4):
        self.d.line(pts(seq), fill=fill, width=p(width), joint="curve")

    def glow(self, x, y, rx, ry, color, blur=60):
        g = Image.new("RGB", (W, H), (0, 0, 0))
        ImageDraw.Draw(g).ellipse([p(x - rx), p(y - ry), p(x + rx), p(y + ry)], fill=color)
        self.img = ImageChops.add(self.img, g.filter(ImageFilter.GaussianBlur(p(blur))))
        self.d = ImageDraw.Draw(self.img)

    def beam(self, seq, color, blur=30):
        g = Image.new("RGB", (W, H), (0, 0, 0))
        ImageDraw.Draw(g).polygon(pts(seq), fill=color)
        self.img = ImageChops.add(self.img, g.filter(ImageFilter.GaussianBlur(p(blur))))
        self.d = ImageDraw.Draw(self.img)

    def shade(self, seq, alpha=120, blur=18, ellipse=False):
        sh = Image.new("L", (W, H), 0)
        sd = ImageDraw.Draw(sh)
        if ellipse:
            sd.ellipse([p(v) for v in seq], fill=alpha)
        else:
            sd.polygon(pts(seq), fill=alpha)
        sh = sh.filter(ImageFilter.GaussianBlur(p(blur)))
        self.img = Image.composite(Image.new("RGB", (W, H), (4, 5, 8)), self.img, sh)
        self.d = ImageDraw.Draw(self.img)

    def haze(self, y0, y1, color, alpha=90):
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle([0, p(y0), W, p(y1)], fill=alpha)
        m = m.filter(ImageFilter.GaussianBlur(p(70)))
        self.img = Image.composite(Image.new("RGB", (W, H), color), self.img, m)
        self.d = ImageDraw.Draw(self.img)

    # ---- figures ----------------------------------------------------
    def person(self, x, y, h, pose="stand", flip=False, color=(18, 19, 24), rim=(255, 196, 120), light=(-1, -1),
               shadow=True, cap=False, rot_ground=True):
        P = POSES[pose]
        sx = -1 if flip else 1

        def j(n):
            ox, oy = P[n]
            return (x + sx * ox * h, y - oy * h)

        if shadow:
            self.shade([x - .22 * h, y - .02 * h, x + .22 * h, y + .035 * h], alpha=150, blur=10, ellipse=True)
        layer = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(layer)

        def cap_line(a, b, w0, w1=None):
            w1 = w1 or w0
            (ax, ay), (bx, by) = a, b
            n = 14
            for i in range(n + 1):
                t = i / n
                cx, cy, r = ax + (bx - ax) * t, ay + (by - ay) * t, (w0 + (w1 - w0) * t) * h / 2
                d.ellipse([p(cx - r), p(cy - r), p(cx + r), p(cy + r)], fill=255)

        hip, neck = j("hip"), j("neck")
        hl, hr = (hip[0] - sx * .085 * h, hip[1]), (hip[0] + sx * .085 * h, hip[1])
        for k, f, hp in (("kL", "fL", hl), ("kR", "fR", hr)):
            cap_line(hp, j(k), .095, .072)
            cap_line(j(k), j(f), .07, .05)
            fx, fy = j(f)
            d.ellipse([p(fx - .03 * h), p(fy - .035 * h), p(fx + sx * .09 * h if sx > 0 else fx + .03 * h), p(fy + .012 * h)] if sx > 0
                      else [p(fx - .09 * h), p(fy - .035 * h), p(fx + .03 * h), p(fy + .012 * h)], fill=255)
        d.polygon(pts([j("sL"), j("sR"), hr, hl]), fill=255)
        cap_line(j("sL"), j("sR"), .075)
        cap_line(hl, hr, .1)
        cap_line(neck, hip, .17, .15)
        for s_, e_, h_ in (("sL", "eL", "hL"), ("sR", "eR", "hR")):
            cap_line(j(s_), j(e_), .065, .05)
            cap_line(j(e_), j(h_), .048, .038)
            hx, hy = j(h_)
            d.ellipse([p(hx - .024 * h), p(hy - .024 * h), p(hx + .024 * h), p(hy + .024 * h)], fill=255)
        cap_line(neck, j("head"), .05)
        cx, cy = j("head")
        d.ellipse([p(cx - .052 * h), p(cy - .068 * h), p(cx + .052 * h), p(cy + .062 * h)], fill=255)
        if cap:
            d.pieslice([p(cx - .056 * h), p(cy - .078 * h), p(cx + .056 * h), p(cy + .03 * h)], 180, 360, fill=255)
            d.rectangle([p(cx), p(cy - .03 * h), p(cx + sx * .1 * h), p(cy - .016 * h)] if sx > 0
                        else [p(cx - .1 * h), p(cy - .03 * h), p(cx), p(cy - .016 * h)], fill=255)
        layer = layer.filter(ImageFilter.GaussianBlur(p(0.6)))
        self.img.paste(Image.new("RGB", (W, H), color), (0, 0), layer)
        if rim:
            off = ImageChops.offset(layer, p(-light[0] * 3.2), p(-light[1] * 3.2))
            edge = ImageChops.subtract(layer, off).filter(ImageFilter.GaussianBlur(p(0.8)))
            edge = edge.point(lambda v: int(v * 0.8))
            self.img.paste(Image.new("RGB", (W, H), rim), (0, 0), edge)
        self.d = ImageDraw.Draw(self.img)
        return j

    # ---- finishing --------------------------------------------------
    def finish(self, path, title=None, sub=None, pos="bl", accent=(226, 170, 62), big=None):
        img = self.img
        vig = Image.new("L", (W, H), 0)
        ImageDraw.Draw(vig).ellipse([-p(260), -p(240), W + p(260), H + p(240)], fill=255)
        vig = vig.filter(ImageFilter.GaussianBlur(p(170)))
        img = Image.composite(img, Image.new("RGB", (W, H), (3, 4, 7)), vig)
        d = ImageDraw.Draw(img)
        if big:
            f = ImageFont.truetype(FONT, p(big[1]))
            d.text((p(960) + p(3), p(big[2]) + p(4)), big[0], font=f, fill=(0, 0, 0), anchor="mm")
            d.text((p(960), p(big[2])), big[0], font=f, fill=big[3] if len(big) > 3 else (240, 236, 226), anchor="mm")
        if title:
            y = 900 if pos == "bl" else 70
            sh = Image.new("L", (W, H), 0)
            ImageDraw.Draw(sh).rectangle([0, p(y - 50), p(1300), p(y + 130)], fill=170)
            sh = sh.filter(ImageFilter.GaussianBlur(p(60)))
            img = Image.composite(Image.new("RGB", (W, H), (4, 5, 8)), img, sh)
            d = ImageDraw.Draw(img)
            d.rectangle([p(70), p(y), p(78), p(y + (96 if sub else 52))], fill=accent)
            d.text((p(100), p(y - 6)), title, font=ImageFont.truetype(FONT, p(46)), fill=(242, 238, 228))
            if sub:
                d.text((p(100), p(y + 56)), sub, font=ImageFont.truetype(FONT_R, p(32)), fill=(198, 192, 178))
        out = img.resize((1920, 1080), Image.LANCZOS)
        noise = Image.effect_noise((1920, 1080), 22).convert("RGB")
        out = Image.blend(out, ImageChops.multiply(out, noise), 0.22)
        out.save(path)
