"""Neon leaderboard cards for 'The Race to Beat GTA 6'. Names and numbers only, no likeness or footage."""
import sys
src = open("/home/claude/heist-frames/kit/bc_cards.py").read()
exec(src.split("def neon_title")[0].replace('OUT = sys.argv[1] if len(sys.argv) > 1 else "bonnie/cards"', 'OUT = "race/cards"'))
Y = (255, 214, 60)
def bar(c, x, y, w, frac, col, label, val, h=56):
    c.text(x, y - 62, label, 46); c.text(x + w, y - 62, val, 46, col, anchor="ra")
    c.rect(x, y, x + w, y + h, fill=(40, 22, 60), r=h // 2)
    if frac > 0: c.rect(x, y, x + max(h, w * frac), y + h, fill=col, r=h // 2)
def board(c, rows, title="LIVE STANDINGS"):
    c.text(960, 110, title, 56, TEAL, anchor="mm")
    for i, (n, f, col, v) in enumerate(rows): bar(c, 360, 260 + i * 160, 1200, f, col, n, v)
ROWS = [("BrycexD", 1.0, Y, "FINISHED"), ("iShowSpeed", .82, PINK, "82%"), ("N3on", .2, TEAL, "CHAPTER 1"), ("Kai Cenat", .0, (170, 150, 200), "GOING 100%")]
def N(seed, f):
    c = Card("neon", seed); f(c); return c
def big(s1, s2, k=None, col=PINK):
    def f(c):
        if k: c.text(960, 230, k, 52, TEAL, anchor="mm")
        c.text(960, 430, s1, 170, (255, 255, 255), anchor="mm"); c.text(960, 610, s2, 64, col, anchor="mm")
    return f
N(1, lambda c: (c.palms(), c.text(960, 330, "THE RACE", 170, anchor="mm"), c.text(960, 500, "TO BEAT GTA 6", 110, PINK, anchor="mm"), c.text(960, 640, "DAY 2 STANDINGS", 50, TEAL, anchor="mm"))).save("g01")
N(2, big("~80 HOURS", "Rockstar's Rob Nelson, his own playthrough", "THE BENCHMARK", TEAL)).save("g02")
N(3, lambda c: board(c, [(n, 0, col, "?") for n, f, col, v in ROWS], "THE RACE")).save("g03")
N(4, big("7 HOURS?", "the clip that went viral", "N3on")).save("g04")
def ch(c):
    c.text(960, 200, "WHAT HE ACTUALLY FINISHED", 52, TEAL, anchor="mm")
    for i in range(5):
        x = 300 + i * 270; c.rect(x, 380, x + 240, 620, fill=PINK if i == 0 else (40, 22, 60), r=24); c.text(x + 120, 500, f"CH {i+1}", 60, (255, 255, 255) if i == 0 else (120, 100, 150), anchor="mm")
    c.text(960, 730, "5 chapters · 90+ main missions", 50, anchor="mm")
N(5, ch).save("g05")
N(6, big("39:38:22", "first reported full finish", "BrycexD", Y)).save("g06")
N(7, big("50+ HOURS", "awake, no breaks", "BrycexD", Y)).save("g07")
N(8, lambda c: (c.text(960, 300, "WORLD RECORD #1", 60, Y, anchor="mm"), c.rect(560, 380, 1360, 640, outline=Y, w=6, r=30), c.text(960, 470, "BrycexD", 90, anchor="mm"), c.text(960, 570, "39:38:22", 70, Y, anchor="mm"), c.text(960, 740, "expect it to fall fast", 48, TEAL, f=FR, anchor="mm"))).save("g08")
N(9, lambda c: (c.text(960, 230, "iShowSpeed", 90, anchor="mm"), bar(c, 360, 520, 1200, .82, PINK, "main story", "82%", 80))).save("g09")
N(10, big("40 HOURS", "straight, no sleep", "iShowSpeed")).save("g10")
N(11, big("392K", "watching live at the peak", "iShowSpeed", TEAL)).save("g11")
N(12, big("\"12 MORE HOURS\"", "his own prediction", "iShowSpeed")).save("g12")
N(13, big("100%", "every mission, every side activity", "Kai Cenat", (190, 170, 230))).save("g13")
N(14, lambda c: board(c, ROWS)).save("g14")
N(15, lambda c: (board(c, ROWS), c.rect(1380, 40, 1880, 170, fill=PINK, r=20), c.text(1630, 105, "AS OF NOV 20", 44, (255, 255, 255), anchor="mm"))).save("g15")
N(16, lambda c: (c.palms(), c.text(960, 330, "WHO FINISHES", 140, anchor="mm"), c.text(960, 480, "NEXT?", 160, PINK, anchor="mm"), c.text(960, 640, "tell me in the comments", 52, TEAL, anchor="mm"))).save("g16")
print("ok")
