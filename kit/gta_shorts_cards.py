"""Cards for three GTA 6 Shorts: hacker, sales record, race update. Text, icons and silhouettes only."""
src = open("/home/claude/heist-frames/kit/race_cards.py").read()
exec(src.split("N(1,")[0].replace('OUT = "race/cards"', 'OUT = "gtas/cards"'))
import os; os.makedirs("gtas/cards", exist_ok=True)
R = (240, 60, 60); G = (90, 220, 120)
def tv(c, x, y, w):
    c.rect(x, y, x + w, y + w * .58, fill=(10, 6, 18), outline=TEAL, w=5, r=14); c.rect(x + w * .45, y + w * .58, x + w * .55, y + w * .66, fill=TEAL); c.rect(x + w * .3, y + w * .66, x + w * .7, y + w * .69, fill=TEAL)
    c.rect(x + w * .78, y + w * .6, x + w * .98, y + w * .66, fill=PINK, r=6)
def phone(c, x, y, h): c.rect(x, y, x + h * .5, y + h, fill=(10, 6, 18), outline=PINK, w=5, r=26)
# hacker
N(101, lambda c: (tv(c, 1060, 300, 640), c.text(120, 300, "HE LEAKED", 100), c.text(120, 420, "GTA 6", 130, R), c.text(120, 580, "from a hotel room", 52, TEAL, f=FR))).save("h01")
N(102, big("AGE 18", "member of the Lapsus$ hacking gang", "2022", R)).save("h02")
N(103, big("ON BAIL", "under police protection at a Travelodge", "ALREADY", R)).save("h03")
def nocomp(c):
    c.rect(660, 300, 1260, 640, fill=(10, 6, 18), outline=(150, 140, 170), w=6, r=16); c.rect(580, 640, 1340, 680, fill=(150, 140, 170), r=10)
    c.d.line([(p(600), p(260)), (p(1320), p(720))], fill=R, width=p(22)); c.text(960, 820, "police had taken his computer", 56, anchor="mm")
N(104, nocomp).save("h04")
N(105, lambda c: (phone(c, 300, 300, 420), tv(c, 700, 330, 560), c.text(960, 200, "HIS TOOLS", 60, TEAL, anchor="mm"), c.text(960, 860, "phone  ·  hotel TV  ·  Fire Stick", 56, anchor="mm"))).save("h05")
N(106, big("90 CLIPS", "almost an hour of unfinished GTA 6", "STOLEN", R)).save("h06")
def slack(c):
    c.text(960, 200, "POSTED IN ROCKSTAR'S OWN SLACK", 52, TEAL, anchor="mm")
    c.rect(360, 330, 1560, 700, fill=(18, 10, 30), outline=(120, 90, 160), w=4, r=24); c.rect(410, 380, 500, 470, fill=R, r=14)
    c.text(540, 380, "the hacker (paraphrased)", 40, (200, 190, 220)); c.text(540, 460, "contact me within 24 hours", 52); c.text(540, 540, "or I release the source code", 52, R)
N(107, slack).save("h07")
N(108, big("$5 MILLION", "plus thousands of hours of staff time", "WHAT ROCKSTAR SAYS IT COST", R)).save("h08")
N(109, lambda c: (c.rect(560, 330, 1360, 560, outline=R, w=8, r=20), c.text(960, 445, "GUILTY", 160, R, anchor="mm"), c.text(960, 690, "now 21  ·  pleaded guilty Nov 16, 2026", 52, anchor="mm"))).save("h09")
N(110, big("SENTENCING", "expected in the coming days", "WHAT'S NEXT", TEAL)).save("h10")
# sales
N(201, big("$3.79 BILLION", "in ONE day", "GTA 6 LAUNCH DAY", G)).save("s01")
N(202, big("32.5M", "copies sold through preorders alone", "BEFORE ANYONE PLAYED", G)).save("s02")
N(203, big("~8 MILLION", "watching GTA 6 streams at the same time", "PEAK LIVE VIEWERS", TEAL)).save("s03")
def cmp(c):
    c.text(960, 140, "FIRST WEEKEND vs FIRST DAY", 52, TEAL, anchor="mm")
    bar(c, 360, 380, 1200, 1.2 / 3.79, (170, 150, 200), "Avengers: Endgame (weekend)", "$1.2B", 80)
    bar(c, 360, 640, 1200, 1.0, G, "GTA 6 (one day)", "$3.79B", 80)
N(204, cmp).save("s04")
N(205, big("13 YEARS", "since GTA 5", "THE WAIT", PINK)).save("s05")
N(206, lambda c: (c.palms(), c.text(960, 380, "ARE YOU", 140, anchor="mm"), c.text(960, 540, "PLAYING IT?", 140, G, anchor="mm"))).save("s06")
# race update
N(301, lambda c: (c.palms(), c.text(960, 330, "IT'S OFFICIAL", 150, anchor="mm"), c.text(960, 500, "2 streamers have beaten GTA 6", 64, PINK, anchor="mm"))).save("r01")
N(302, big("39:38", "#1  ·  New Zealand head start, no sleep", "BrycexD", Y)).save("r02")
N(303, big("52:30", "#2 to finish", "iShowSpeed", PINK)).save("r03")
N(304, big("THE ENDING?", "emotional, but let down", "iShowSpeed", PINK)).save("r04")
ROWS2 = [("BrycexD", 1.0, Y, "39:38 ✓"[:5]), ("iShowSpeed", 1.0, PINK, "52:30"), ("N3on", .2, TEAL, "CHAPTER 1"), ("Kai Cenat", .0, (170, 150, 200), "GOING 100%")]
N(305, lambda c: board(c, ROWS2, "STANDINGS · NOV 21")).save("r05")
N(306, lambda c: (c.palms(), c.text(960, 330, "WHO'S", 150, anchor="mm"), c.text(960, 500, "THIRD?", 170, PINK, anchor="mm"), c.text(960, 650, "drop your guess in the comments", 50, TEAL, anchor="mm"))).save("r06")
print("ok")
