"""Lufthansa heist — 32 scenes in the stickman comic style."""
import os
import sys
from kit import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/stickman/out"
os.makedirs(OUT, exist_ok=True)

WERNER = dict(jacket=(120, 170, 220), hat="cap", hat_color=(40, 70, 150))
KRUG = dict(jacket=(130, 80, 150), hat="hair", hat_color=(130, 90, 50))
HILL = dict(jacket=(190, 60, 50), hat="hair", hat_color=(70, 46, 30))
BURKE = dict(jacket=(92, 60, 40), hat="fedora", hat_color=(30, 30, 36), long_coat=True)
EDW = dict(jacket=(240, 140, 40), hat="beanie", hat_color=(70, 70, 84))
FBI = dict(jacket=(30, 40, 70), hat="hair", hat_color=(60, 44, 30), face="shades", badge="FBI")
COP = dict(jacket=(40, 70, 170), hat="cap", hat_color=(30, 50, 130))
WORKER = dict(jacket=(240, 130, 40), hat="hardhat", hat_color=(250, 210, 40))
CREW = [dict(jacket=(36, 96, 150), hat_color=(214, 60, 50)), dict(jacket=(60, 130, 80), hat_color=(240, 190, 40)),
        dict(jacket=(120, 70, 140), hat_color=(60, 160, 170)), dict(jacket=(150, 60, 60), hat_color=(240, 240, 240)),
        dict(jacket=(70, 80, 100), hat_color=(250, 130, 40)), dict(jacket=(60, 60, 70), hat_color=(120, 200, 90))]


def crew(i, **kw):
    return dict(CREW[i % len(CREW)], hat="beanie", masked=True, **kw)


def out(n):
    return os.path.join(OUT, f"s{n:02d}.png")


def s01():
    sc = Scene(1)
    bg_airport(sc, door_open=False)
    sc.glow(lambda g: poly(g, [(700, 790), (700, 830), (1100, 900), (1100, 700)], fill=(80, 70, 26)), blur=24)
    sc.prop(lambda d: van(d, 130, 900, 1.0))
    sc.label(60, 44, "JFK AIRPORT · NEW YORK", 80)
    sc.label(60, 146, "DECEMBER 11, 1978 · 3:00 AM", 72, fill=YELLOW)
    sc.save(out(1))


def s02():
    sc = Scene(2)
    bg_airport(sc, building=False)
    sc.prop(lambda d: [rect(d, 520 - k * 60, 600 + k * 70, 760 - k * 60, 614 + k * 70, fill=WHITE, radius=7) for k in range(3)], rim_px=3)
    sc.prop(lambda d: van(d, 900, 900, 1.05))
    sc.prop(lambda d: [bill(d, x, y, a) for x, y, a in ((780, 560, 0.4), (640, 700, -0.5), (500, 520, 0.2), (360, 660, -0.2), (240, 800, 0.6), (820, 800, -0.3))], rim_px=4)
    sc.label(60, 44, "64 MINUTES LATER", 88)
    sc.label(60, 156, "NEARLY $6 MILLION — GONE", 76, fill=YELLOW)
    sc.save(out(2))


def s03():
    sc = Scene(3)
    bg_card(sc, (40, 60, 140), (30, 46, 110), cy=700)
    sc.prop(lambda d: money_pile(d, 960, 940, cols=9, rows=6, s=1.15))
    sc.prop(lambda d: [bag(d, 330, 950, 1.5), bag(d, 1590, 950, 1.5)])
    sc.prop(lambda d: [bill(d, x, y, a, 1.2) for x, y, a in ((420, 420, 0.4), (1500, 440, -0.4), (960, 400, 0.1), (700, 520, -0.2), (1230, 520, 0.3))], rim_px=4)
    sc.label(960, 60, "BIGGEST CASH ROBBERY", 104, anchor="ma")
    sc.label(960, 190, "IN AMERICAN HISTORY (AT THE TIME)", 64, fill=YELLOW, anchor="ma")
    sc.save(out(3))


def s04():
    sc = Scene(4)
    bg_card(sc, (120, 30, 36), (96, 22, 28))
    def draw(d):
        for i in range(6):
            c = CREW[i]
            portrait(d, 110 + i * 290, 380, "CREW %d" % (i + 1), hat="beanie", hat_color=c["hat_color"], jacket=c["jacket"],
                     masked=True, w=250, h=330, status="x" if i != 3 else None)
    sc.prop(draw)
    sc.label(960, 70, "THE MEN BEHIND IT", 96, anchor="ma")
    sc.label(960, 190, "ALMOST NONE LIVED TO SPEND IT", 76, fill=YELLOW, anchor="ma")
    sc.save(out(4))


def s05():
    sc = Scene(5)
    bg_room(sc, wall=(70, 110, 120), floor=(110, 90, 70))
    sc.man(620, 960, SHRUG, s=1.2, face="scared", **WERNER)
    def hold(d, j):
        hx, hy = j("handR")
        rect(d, hx - 20, hy - 130, hx + 200, hy + 10, fill=(250, 246, 232), outline=INK, width=7, radius=8)
        text(d, hx + 90, hy - 94, "I.O.U.", 36, fill=INK, anchor="mm", stroke=False)
        text(d, hx + 90, hy - 38, "$20,000", 40, fill=RED, anchor="mm", stroke=False)
    sc.man(1300, 960, POINT, s=1.2, face="angry", flip=True, hold=hold, **KRUG)
    sc.label(60, 44, "LOUIS WERNER · CARGO SUPERVISOR", 70)
    sc.label(60, 136, "OWES HIS BOOKIE $20,000", 76, fill=YELLOW)
    sc.save(out(5))


def s06():
    sc = Scene(6)
    vgrad(sc.rgb, (70, 150, 230), (170, 220, 250), 0, 800)
    d = sc.d
    for cx, cy, w_ in ((200, 220, 360), (1300, 160, 300), (800, 560, 320), (1560, 620, 280)):
        rect(d, cx, cy, cx + w_, cy + 60, fill=WHITE, radius=30)
        rect(d, cx + 60, cy - 44, cx + w_ - 70, cy + 30, fill=WHITE, radius=30)
    rect(d, 0, 860, 1920, 1080, fill=(40, 100, 180))
    for wx in range(0, 1920, 160):
        d.arc([p(wx), p(880), p(wx + 160), p(940)], 200, 340, fill=(120, 180, 240), width=p(8))
    sc.prop(lambda d: plane(d, 520, 520, 1.25))
    sc.prop(lambda d: [bill(d, x, y, a, 1.1) for x, y, a in ((420, 640, 0.4), (300, 500, -0.4), (180, 660, 0.2), (460, 380, -0.2))], rim_px=4)
    sc.label(60, 44, "ONCE A MONTH", 96)
    sc.label(60, 164, "CASH FLOWN IN FROM WEST GERMANY", 68, fill=YELLOW)
    sc.save(out(6))


def s07():
    sc = Scene(7)
    bg_vault(sc, open_=False)
    sc.prop(lambda d: money_pile(d, 520, 900, cols=6, rows=5, s=1.1))
    sc.label(60, 44, "UNMARKED. UNTRACEABLE.", 88)
    sc.label(60, 156, "SITTING IN A VAULT AT THE AIRPORT", 66, fill=YELLOW)
    sc.save(out(7))


def s08():
    sc = Scene(8)
    bg_card(sc, (30, 110, 120), (24, 92, 102))
    sc.man(330, 960, POINT, s=1.05, **WERNER)
    sc.man(960, 960, POINT, s=1.05, **KRUG)
    sc.man(1590, 960, HIPS, s=1.05, face="happy", **HILL)
    def arrows(d):
        for x0 in (520, 1150):
            line(d, [(x0, 520), (x0 + 220, 520)], fill=INK, width=30)
            poly(d, [(x0 + 210, 470), (x0 + 300, 520), (x0 + 210, 570)], fill=INK)
            line(d, [(x0, 520), (x0 + 214, 520)], fill=YELLOW, width=16)
            poly(d, [(x0 + 216, 486), (x0 + 284, 520), (x0 + 216, 554)], fill=YELLOW)
    sc.prop(arrows, rim_px=0)
    for x, n in ((330, "WERNER"), (960, "KRUGMAN"), (1590, "HENRY HILL")):
        sc.label(x, 1000, n, 54, anchor="ma")
    sc.label(960, 50, "THE TIP TRAVELS", 96, anchor="ma")
    sc.label(960, 170, "INSIDE MAN  →  BOOKIE  →  MOB ASSOCIATE", 58, fill=YELLOW, anchor="ma")
    sc.save(out(8))


def s09():
    sc = Scene(9)
    bg_bar(sc)
    sc.man(1040, 1010, CROSS, s=1.65, face="angry", **BURKE)
    sc.label(60, 44, 'JIMMY "THE GENT" BURKE', 88)
    sc.label(60, 156, "ROBBING JFK FOR YEARS", 72, fill=YELLOW)
    sc.save(out(9))


def s10():
    sc = Scene(10)
    bg_bar(sc)
    sc.man(430, 950, POINT, s=1.1, face="angry", **BURKE)
    sc.man(1560, 950, HIPS, s=1.05, flip=True, **HILL)
    def table(d):
        rect(d, 640, 720, 1380, 770, fill=(120, 76, 44), outline=INK, width=9, radius=10)
        rect(d, 700, 770, 740, 960, fill=(96, 60, 36), outline=INK, width=7)
        rect(d, 1280, 770, 1320, 960, fill=(96, 60, 36), outline=INK, width=7)
        poly(d, [(700, 720), (1320, 720), (1260, 560), (760, 560)], fill=(70, 130, 220), outline=INK, width=8)
        for x0, y0, x1, y1 in ((800, 600, 960, 690), (990, 590, 1090, 650), (1110, 610, 1230, 700)):
            rect(d, x0, y0, x1, y1, outline=WHITE, width=5)
        line(d, [(840, 700), (880, 640), (1020, 640), (1060, 600)], fill=YELLOW, width=7)
        big_x(d, 1170, 656, r=22, width=8)
    sc.prop(table)
    sc.man(1010, 930, STAND, s=0.95, **crew(0))
    sc.label(60, 44, "THE PLAN", 104)
    sc.label(60, 170, "LAYOUT · ROUTINES · WHERE TO PARK", 62, fill=YELLOW)
    sc.save(out(10))


def s11():
    sc = Scene(11)
    bg_room(sc, wall=(60, 90, 150), floor=(96, 84, 76))
    def cal(d):
        rect(d, 1040, 250, 1800, 760, fill=(250, 246, 232), outline=INK, width=10, radius=14)
        rect(d, 1040, 250, 1800, 350, fill=RED, outline=INK, width=10, radius=14)
        text(d, 1420, 300, "DECEMBER 1978", 56, fill=WHITE, anchor="mm", stroke=False)
        for i, (day, sub) in enumerate((("SAT", "CASH\nLANDS"), ("SUN", "IN THE\nVAULT"), ("MON", "TRUCK\nCOMES"))):
            x0 = 1070 + i * 240
            rect(d, x0, 390, x0 + 220, 720, fill=(255, 236, 150) if i < 2 else WHITE, outline=INK, width=7, radius=10)
            text(d, x0 + 110, 450, day, 60, fill=INK, anchor="mm", stroke=False)
            for k, t in enumerate(sub.split("\n")):
                text(d, x0 + 110, 560 + k * 56, t, 40, fill=(40, 100, 60) if i < 2 else RED, anchor="mm", stroke=False)
    sc.prop(cal)
    def hold(d, j):
        hx, hy = j("handR")
        rect(d, hx - 22, hy - 60, hx + 22, hy + 50, fill=(40, 40, 46), radius=12)
    sc.man(520, 960, PHONE, s=1.3, hold=hold, **WERNER)
    sc.prop(lambda d: bubble(d, 110, 130, "IT'S HERE.", 70, tail="right"))
    sc.label(60, 920, "SATURDAY: THE CALL", 84, fill=YELLOW)
    sc.save(out(11))


def s12():
    sc = Scene(12)
    night_sky(sc)
    control_tower(sc.d, 1640)
    tarmac(sc)
    def fence(d):
        for k in range(-400, 2200, 44):
            line(d, [(k, 860), (k + 400, 460)], fill=(150, 156, 176), width=3)
            line(d, [(k, 460), (k + 400, 860)], fill=(150, 156, 176), width=3)
        for fx in range(0, 1921, 320):
            rect(d, fx - 9, 430, fx + 9, 870, fill=(96, 100, 128), outline=INK, width=4)
        rect(d, 0, 446, 1920, 466, fill=(96, 100, 128), outline=INK, width=4)
        rect(d, 820, 440, 1140, 870, outline=INK, width=16)
        rect(d, 820, 440, 1140, 870, outline=(210, 180, 60), width=8)
        rect(d, 1010, 640, 1100, 720, fill=(230, 190, 60), outline=INK, width=7, radius=10)
        d.arc([p(1028), p(596), p(1082), p(676)], 180, 360, fill=INK, width=p(12))
    sc.prop(fence, rim_px=0)
    def hold(d, j):
        hx, hy = j("handR")
        line(d, [(hx - 40, hy + 60), (hx + 90, hy - 40)], fill=INK, width=22)
        line(d, [(hx - 40, hy + 20), (hx + 90, hy - 10)], fill=INK, width=22)
        line(d, [(hx - 40, hy + 60), (hx + 20, hy + 14)], fill=RED, width=12)
        line(d, [(hx - 40, hy + 20), (hx + 20, hy + 6)], fill=RED, width=12)
    sc.man(760, 960, CARRY, s=1.2, hold=hold, **crew(0))
    sc.man(420, 965, STAND, s=1.1, **crew(1))
    sc.man(180, 970, STAND, s=1.05, **crew(2))
    sc.label(60, 44, "MONDAY · BEFORE DAWN", 88)
    sc.label(60, 156, "THEY CUT THE PADLOCK", 76, fill=YELLOW)
    sc.save(out(12))


def s13():
    sc = Scene(13)
    bg_warehouse(sc)
    sc.man(330, 965, POINT, s=1.2, face="angry", **crew(0))
    sc.man(640, 955, POINT, s=1.15, face="angry", **crew(1))
    for i, x in enumerate((1080, 1340, 1600)):
        sc.man(x, 955 + i * 5, HANDSUP, s=1.1, face="scared", flip=True, **WORKER)
    sc.label(60, 44, "NIGHT SHIFT ROUNDED UP", 84)
    sc.label(60, 150, "NOBODY MOVES", 76, fill=YELLOW)
    sc.save(out(13))


def s14():
    sc = Scene(14)
    bg_vault(sc, open_=False, cx=1300, cy=470)
    def pad(d):
        rect(d, 760, 420, 900, 620, fill=(40, 44, 60), outline=INK, width=8, radius=12)
        rect(d, 778, 438, 882, 480, fill=(120, 230, 140))
        for r_ in range(3):
            for c_ in range(3):
                rect(d, 780 + c_ * 36, 496 + r_ * 38, 808 + c_ * 36, 524 + r_ * 38, fill=(200, 204, 214), radius=5)
    sc.prop(pad, rim_px=0)
    sc.man(640, 960, POINT, s=1.15, face="scared", jacket=(230, 230, 236), hat="hair", hat_color=(120, 120, 130))
    sc.man(300, 965, POINT, s=1.2, face="angry", **crew(2))
    sc.label(60, 44, "THE ONE MAN WHO COULD OPEN IT", 74)
    sc.label(60, 140, "NO ALARM", 96, fill=YELLOW)
    sc.save(out(14))


def s15():
    sc = Scene(15)
    bg_vault(sc, open_=True, cx=1300, cy=470)
    sc.prop(lambda d: money_pile(d, 1300, 720, cols=4, rows=4, s=0.95), rim_px=0)
    sc.prop(lambda d: [money_pile(d, 1200, 960, cols=8, rows=5, s=1.0), gem(d, 1700, 900, 1.5), gem(d, 1790, 950, 1.2, (240, 90, 120)), gem(d, 640, 950, 1.3, (120, 230, 150))])
    sc.man(330, 965, HANDSUP, s=1.2, **crew(0))
    sc.label(60, 44, "EXPECTED: $2 MILLION", 78)
    sc.label(60, 144, "FOUND: $5.8 MILLION", 96, fill=YELLOW)
    sc.save(out(15))


def s16():
    sc = Scene(16)
    bg_airport(sc)
    sc.prop(lambda d: [van(d, -120, 900, 1.0, flip=True), bag(d, 250, 720, 0.6)])
    sc.man(700, 950, POINT, s=1.1, face="angry", flip=True, **BURKE)
    def h2(d, j):
        hx, hy = j("handL")
        bag(d, hx - 56, hy + 96, 1.12)
    sc.man(1120, 945, CARRY, s=1.15, flip=True, hold=h2, **crew(0))
    def h3(d, j):
        hx, hy = j("handR")
        bag(d, hx - 40, hy + 80, 0.9)
    sc.man(1520, 925, RUN, s=1.12, flip=True, hold=h3, **crew(1))
    sc.prop(lambda d: [bill(d, x, y, a) for x, y, a in ((1700, 540, 0.5), (1790, 800, -0.5), (1340, 520, -0.3), (960, 600, 0.35))], rim_px=4)
    sc.label(60, 44, "LOAD THE VAN", 88)
    sc.label(60, 156, '"NOBODY CALLS UNTIL 4:30"', 70, fill=YELLOW)
    sc.save(out(16))


def s17():
    sc = Scene(17)
    bg_card(sc, (24, 26, 40), (34, 36, 54))
    sc.prop(lambda d: bag(d, 960, 900, 2.2))
    def crack(d):
        line(d, [(900, 470), (980, 560), (930, 640), (1010, 730), (960, 820), (1010, 900)], fill=INK, width=22)
        line(d, [(900, 470), (980, 560), (930, 640), (1010, 730), (960, 820), (1010, 900)], fill=RED, width=10)
    sc.prop(crack, rim_px=0)
    sc.label(960, 80, "THE ROBBERY WAS FLAWLESS", 92, anchor="ma")
    sc.label(960, 210, "THEN EVERYTHING FELL APART", 80, fill=RED, anchor="ma")
    sc.save(out(17))


def s18():
    sc = Scene(18)
    bg_junkyard(sc)
    sc.prop(lambda d: van(d, 160, 860, 0.95))
    def arrow(d):
        for k in range(6):
            rect(d, 780 + k * 78, 600, 830 + k * 78, 622, fill=INK, radius=8)
        poly(d, [(1250, 570), (1320, 611), (1250, 652)], fill=INK)
    sc.prop(arrow, rim_px=5)
    sc.label(60, 44, "THE PLAN FOR THE VAN", 84)
    sc.label(60, 150, "STRAIGHT TO THE CRUSHER", 76, fill=YELLOW)
    sc.save(out(18))


def s19():
    sc = Scene(19)
    bg_street(sc, hydrant_x=1060)
    sc.prop(lambda d: van(d, 380, 890, 1.0))
    def zzz(d):
        for k, (x, y, sz) in enumerate(((520, 330, 60), (590, 250, 80), (680, 160, 104))):
            text(d, x, y, "Z", sz, fill=WHITE)
    sc.prop(zzz, rim_px=0)
    sc.label(60, 930, '"STACKS" EDWARDS PARKED IT... AND WENT TO SLEEP', 58, fill=YELLOW)
    sc.label(60, 44, "INSTEAD", 96)
    sc.save(out(19))


def s20():
    sc = Scene(20)
    bg_street(sc, hydrant_x=640)
    sc.prop(lambda d: van(d, -40, 890, 1.0))
    sc.prop(lambda d: [fingerprint(d, 150, 640, 46), fingerprint(d, 300, 720, 40), fingerprint(d, 420, 620, 36)], rim_px=4)
    sc.prop(lambda d: car(d, 1240, 900, 1.0, color=(240, 240, 246), flip=True, police=True))
    sc.glow(lambda g: [circ(g, 1500, 610, 150, fill=(90, 10, 10)), circ(g, 1620, 610, 150, fill=(10, 20, 90))], blur=50) if False else None
    def hold(d, j):
        hx, hy = j("handR")
        circ(d, hx + 34, hy - 30, 46, fill=(170, 220, 244), outline=INK, width=10)
        line(d, [(hx, hy + 10), (hx + 10, hy - 4)], fill=INK, width=14)
    sc.man(900, 960, POINT, s=1.15, flip=True, hold=hold, **COP)
    sc.label(60, 44, "2 DAYS LATER", 96)
    sc.label(60, 164, "POLICE FIND IT — FINGERPRINTS AND ALL", 62, fill=YELLOW)
    sc.save(out(20))


def s21():
    sc = Scene(21)
    bg_card(sc, (120, 30, 36), (96, 22, 28))
    sc.prop(lambda d: portrait(d, 735, 330, "EDWARDS", hat="beanie", hat_color=(70, 70, 84), jacket=(240, 140, 40), w=450, h=600, status=None))
    sc.prop(lambda d: big_x(d, 960, 580, r=190, width=44), rim_px=0)
    sc.label(960, 60, "WITHIN A WEEK", 104, anchor="ma")
    sc.label(960, 190, "THE DRIVER IS DEAD", 80, fill=YELLOW, anchor="ma")
    sc.save(out(21))


def s22():
    sc = Scene(22)
    bg_bar(sc)
    sc.man(480, 960, POINT, s=1.25, face="angry", **BURKE)
    sc.prop(lambda d: bubble(d, 560, 250, "DON'T SPEND\nTHE MONEY!", 66))
    def shop(d, j):
        hx, hy = j("handR")
        rect(d, hx - 50, hy, hx + 50, hy + 130, fill=(240, 120, 170), outline=INK, width=7, radius=8)
        d.arc([p(hx - 30), p(hy - 40), p(hx + 30), p(hy + 30)], 180, 360, fill=INK, width=p(7))
    sc.man(1340, 955, STAND, s=1.1, face="happy", flip=True, hold=shop, **dict(CREW[1], hat="beanie"))
    sc.man(1640, 960, STAND, s=1.1, face="happy", flip=True, hold=shop, **dict(CREW[3], hat="beanie"))
    sc.label(60, 44, "ONE RULE", 100)
    sc.label(60, 164, "NOBODY LISTENED", 76, fill=YELLOW)
    sc.save(out(22))


def s23():
    sc = Scene(23)
    bg_street(sc)
    sc.prop(lambda d: car(d, 250, 900, 1.25, color=(250, 130, 190)))
    sc.man(1180, 960, HANDSUP, s=1.1, face="happy", **dict(CREW[1], hat="beanie"))
    def binoc(d, j):
        hx, hy = j("handR")
        cx, cy = j("head")
        rect(d, cx - 74, cy - 24, cx - 10, cy + 20, fill=(40, 40, 46), outline=INK, width=5, radius=10)
        rect(d, cx - 4, cy - 24, cx + 60, cy + 20, fill=(40, 40, 46), outline=INK, width=5, radius=10)
    sc.man(1700, 965, PHONE, s=1.1, flip=True, hold=binoc, **FBI)
    sc.label(60, 44, "A PINK CADILLAC. FUR COATS.", 80)
    sc.label(60, 146, "AND THE FBI WATCHING 24/7", 74, fill=YELLOW)
    sc.save(out(23))


def board(d, statuses, x0=1210, y0=160, cols=3, w=180, h=186):
    names = ["KRUGMAN", "EDWARDS", "CAFORA", "MANRI", "McMAHON", "EATON"]
    looks = [("hair", (130, 90, 50), (130, 80, 150)), ("beanie", (70, 70, 84), (240, 140, 40)), ("beanie", (240, 190, 40), (60, 130, 80)),
             ("beanie", (214, 60, 50), (36, 96, 150)), ("beanie", (60, 160, 170), (120, 70, 140)), ("cap", (90, 90, 100), (150, 60, 60))]
    for i, st in enumerate(statuses):
        hat, hc, jc = looks[i]
        portrait(d, x0 + (i % cols) * (w + 26), y0 + (i // cols) * (h + 20), names[i], hat=hat, hat_color=hc, jacket=jc, w=w, h=h, status=st)


def s24():
    sc = Scene(24)
    bg_office(sc)
    sc.prop(lambda d: board(d, ["missing", "x", None, None, None, None]), rim_px=0)
    sc.man(880, 960, POINT, s=1.2, **FBI)
    sc.label(60, 620, "JANUARY 1979", 88)
    sc.label(60, 730, "THE BOOKIE VANISHES", 72, fill=YELLOW)
    sc.save(out(24))


def s25():
    sc = Scene(25)
    bg_street(sc, snow=True)
    sc.prop(lambda d: car(d, 120, 900, 1.05, color=(70, 80, 110)))
    def truck(d):
        rect(d, 1020, 480, 1640, 860, fill=(236, 240, 246), outline=INK, width=10, radius=14)
        rect(d, 1640, 600, 1840, 860, fill=(60, 110, 170), outline=INK, width=10, radius=16)
        rect(d, 1700, 630, 1820, 720, fill=(170, 220, 244), outline=INK, width=7, radius=8)
        text(d, 1330, 620, "COLD", 84, fill=(60, 140, 220), anchor="mm", stroke=False)
        text(d, 1330, 730, "STORAGE", 64, fill=(60, 140, 220), anchor="mm", stroke=False)
        for cx in (1160, 1500, 1750):
            circ(d, cx, 870, 62, fill=INK)
            circ(d, cx, 870, 24, fill=(190, 190, 200))
    sc.prop(truck)
    sc.prop(lambda d: [big_x(d, 430, 560, r=70, width=20), big_x(d, 1330, 360, r=70, width=20)], rim_px=5)
    sc.label(60, 44, "ONE BY ONE", 100)
    sc.label(60, 164, "THE CREW DISAPPEARS", 76, fill=YELLOW)
    sc.save(out(25))


def s26():
    sc = Scene(26)
    bg_card(sc, (120, 30, 36), (96, 22, 28))
    def grid(d):
        names = ["EDWARDS", "KRUGMAN", "CAFORA", "MRS CAFORA", "MANRI", "McMAHON", "EATON", "FERRARA"]
        looks = [("beanie", (70, 70, 84), (240, 140, 40)), ("hair", (130, 90, 50), (130, 80, 150)), ("beanie", (240, 190, 40), (60, 130, 80)),
                 ("hair", (230, 190, 90), (230, 110, 160)), ("beanie", (214, 60, 50), (36, 96, 150)), ("beanie", (60, 160, 170), (120, 70, 140)),
                 ("cap", (90, 90, 100), (150, 60, 60)), ("hair", (90, 50, 30), (90, 170, 160))]
        for i in range(8):
            hat, hc, jc = looks[i]
            portrait(d, 150 + (i % 4) * 420, 300 + (i // 4) * 370, names[i], hat=hat, hat_color=hc, jacket=jc, w=330, h=340,
                     status="missing" if i in (1, 2, 3) else "x")
    sc.prop(grid)
    sc.label(960, 40, "BY SUMMER 1979", 84, anchor="ma")
    sc.label(960, 150, "8 DEAD OR MISSING", 104, fill=YELLOW, anchor="ma")
    sc.save(out(26))


def s27():
    sc = Scene(27)
    bg_prison(sc)
    sc.man(985, 960, BARS, s=1.12, face="sad", shadow=False, **dict(WERNER, hat="hair", hat_color=(90, 70, 50), jacket=(240, 130, 40)))
    cell_bars(sc)
    sc.label(60, 44, "THE ONLY ONE CONVICTED", 84)
    sc.label(60, 150, "LOUIS WERNER · 15 YEARS", 80, fill=YELLOW)
    sc.save(out(27))


def s28():
    sc = Scene(28)
    bg_prison(sc)
    sc.man(985, 960, CROSS, s=1.12, face="angry", shadow=False, jacket=(240, 130, 40), hat="hair", hat_color=(160, 160, 166))
    cell_bars(sc)
    sc.label(60, 44, "BURKE: NEVER CHARGED FOR THE HEIST", 70)
    sc.label(60, 136, "DIED IN PRISON · 1996", 84, fill=YELLOW)
    sc.save(out(28))


def s29():
    sc = Scene(29)
    bg_office(sc)
    sc.prop(lambda d: board(d, ["missing", "x", "missing", "x", "x", "x"]), rim_px=0)
    sc.man(560, 960, SIT, s=1.25, face="scared", **HILL)
    def desk(d):
        rect(d, 380, 760, 1160, 800, fill=(120, 76, 44), outline=INK, width=9, radius=8)
        rect(d, 420, 800, 460, 960, fill=(96, 60, 36), outline=INK, width=7)
        rect(d, 1080, 800, 1120, 960, fill=(96, 60, 36), outline=INK, width=7)
        rect(d, 860, 700, 1040, 760, fill=(50, 54, 66), outline=INK, width=7, radius=8)
        circ(d, 910, 730, 18, fill=(200, 204, 214), outline=INK, width=5)
        circ(d, 990, 730, 18, fill=(200, 204, 214), outline=INK, width=5)
    sc.prop(desk)
    sc.man(1420, 960, CROSS, s=1.2, flip=True, **FBI)
    sc.prop(lambda d: bubble(d, 120, 90, "I'LL TELL YOU\nEVERYTHING.", 60))
    sc.label(60, 930, "1980 · HENRY HILL TALKS", 80, fill=YELLOW)
    sc.save(out(29))


def s30():
    sc = Scene(30)
    bg_vault(sc, open_=True, cx=1300, cy=470)
    sc.prop(lambda d: [text(d, x, y, "?", sz, fill=YELLOW, anchor="mm") for x, y, sz in ((1300, 470, 320), (1060, 250, 130), (1560, 300, 150), (1500, 700, 110))], rim_px=0)
    sc.man(480, 965, SHRUG, s=1.25, **FBI)
    sc.label(60, 44, "THE MONEY?", 104)
    sc.label(60, 172, "ALMOST NONE OF IT WAS EVER FOUND", 64, fill=YELLOW)
    sc.save(out(30))


def s31():
    sc = Scene(31)
    bg_airport(sc, door_open=False)
    for i in range(6):
        sc.man(190 + i * 190, 960, STAND, s=0.82, **crew(i))
    sc.prop(lambda d: [big_x(d, 190 + i * 190, 690, r=60, width=18) for i in (0, 1, 2, 4, 5)], rim_px=5)
    sc.label(60, 44, "64 MINUTES TO STEAL IT", 84)
    sc.label(60, 150, "LESS THAN A YEAR TO LOSE EVERYTHING", 66, fill=YELLOW)
    sc.save(out(31))


def s32():
    sc = Scene(32)
    bg_card(sc, (40, 60, 140), (30, 46, 110))
    def btn(d):
        rect(d, 900, 430, 1700, 640, fill=RED, outline=INK, width=12, radius=40)
        text(d, 1300, 535, "SUBSCRIBE", 110, fill=WHITE, anchor="mm", stroke=False)
    sc.prop(btn)
    sc.man(520, 980, POINT, s=1.45, face="happy", **crew(0))
    sc.prop(lambda d: bag(d, 1300, 960, 1.4))
    sc.label(960, 60, "MORE TRUE HEISTS EVERY WEEK", 84, anchor="ma")
    sc.label(960, 180, "THE NEXT ONE IS EVEN STRANGER", 68, fill=YELLOW, anchor="ma")
    sc.save(out(32))


if __name__ == "__main__":
    only = [int(a) for a in sys.argv[2:]] if len(sys.argv) > 2 else range(1, 33)
    for n in only:
        globals()["s%02d" % n]()
        print("ok", n, flush=True)
