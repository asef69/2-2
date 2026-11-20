"""code_shots.py — renders every compiled TF-practice Java file (java/<bundle>/*.java) as a PNG screenshot."""
import glob, os, re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "code_screenshots")
F = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 20)
FB = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 20)
FT = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 18)
KW = set("abstract assert boolean break byte case catch char class continue default do double else enum extends final finally float for if implements import instanceof int interface long new package private protected public return short static super switch synchronized this throw throws try void volatile while null true false var".split())
COL = dict(bg=(250, 251, 252), bar=(232, 237, 242), fg=(36, 41, 47), kw=(0, 92, 197), st=(3, 120, 70), cm=(120, 130, 140), nu=(176, 80, 0), ty=(111, 66, 193), ln=(160, 168, 176))
TOK = re.compile(r'(//.*$)|("(?:\\.|[^"\\])*")|(\'(?:\\.|[^\'\\])\')|(\b\d+(?:\.\d+)?[fLd]?\b)|(@\w+)|([A-Za-z_]\w*)')
CW = F.getlength("M")
LH = 27
PAD = 22
for path in sorted(glob.glob(os.path.join(HERE, "java", "*", "*.java"))):
    bundle, name = os.path.basename(os.path.dirname(path)), os.path.basename(path)
    lines = open(path, encoding="utf-8").read().rstrip("\n").replace("\t", "    ").split("\n")
    w = int(max(900, 70 + CW * max(len(l) for l in lines) + PAD * 2))
    top = 44
    im = Image.new("RGB", (w, top + len(lines) * LH + PAD * 2), COL["bg"])
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, top - 6], fill=COL["bar"])
    d.text((PAD, 8), f"{name}   ·   CSE 213 TF practice ({bundle})", font=FT, fill=COL["fg"])
    in_block = False
    for i, ln in enumerate(lines):
        y = top + PAD + i * LH
        d.text((PAD, y), f"{i + 1:>3}", font=F, fill=COL["ln"])
        x = PAD + 60
        if in_block or ln.strip().startswith(("/*", "*")):
            d.text((x, y), ln, font=F, fill=COL["cm"])
            in_block = "*/" not in ln if ("/*" in ln or in_block) else False
            continue
        pos = 0
        for m in TOK.finditer(ln):
            if m.start() > pos:
                d.text((x + pos * CW, y), ln[pos:m.start()], font=F, fill=COL["fg"])
            t = m.group(0)
            c, f = COL["fg"], F
            if m.group(1): c = COL["cm"]
            elif m.group(2) or m.group(3): c = COL["st"]
            elif m.group(4): c = COL["nu"]
            elif m.group(5): c = COL["ty"]
            elif t in KW: c, f = COL["kw"], FB
            elif t[0].isupper(): c = COL["ty"]
            d.text((x + m.start() * CW, y), t, font=f, fill=c)
            pos = m.end()
        if pos < len(ln):
            d.text((x + pos * CW, y), ln[pos:], font=F, fill=COL["fg"])
    od = os.path.join(OUT, bundle)
    os.makedirs(od, exist_ok=True)
    im.save(os.path.join(od, name.replace(".java", ".png")), optimize=True)
    print(bundle, name, im.size)
