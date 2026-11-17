import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

KEYWORDS = set("""kıdem tazminatı istifa fesih haklı maaş ücret sigorta prim evlilik askerlik
emeklilik tavan damga vergisi brüt net ihbar izin alacak arabuluculuk zamanaşımı ibra
muvazzaf madde kanun dilekçe belge şart hak hukuk yıl gün ay lira""".split())

HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter,{fs},&H00FFFFFF,&H00FFFFFF,&H00100A08,&H96000000,1,0,0,0,100,100,{sp},0,1,{bo},{sh},2,{ml},{mr},{mv},1
Style: Small,Inter,{sfs},&H00A69E93,&H00A69E93,&H00100A08,&H96000000,0,0,0,0,100,100,1,0,1,3,0,2,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def esc(s):
    return s.replace("{", "(").replace("}", ")")


def is_key(w):
    c = w.lower().strip(".,:;!?»«\"'")
    if any(ch.isdigit() for ch in c):
        return True
    return c in KEYWORDS or c.rstrip("ları").rstrip("ler") in KEYWORDS


def line(words, accent="&H3DC5FF&"):
    out = []
    for wd in words:
        w = esc(wd["w"])
        out.append(f"{{\\c{accent}}}{w}{{\\c&HFFFFFF&}}" if is_key(wd["w"]) else w)
    return " ".join(out)


def build(chunks, out, w, h, fs=92, sp=0.5, bo=10, sh=4, ml=80, mr=80, mv=300):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(HEAD.format(w=w, h=h, fs=fs, sfs=int(fs * 0.42), sp=sp, bo=bo, sh=sh, ml=ml, mr=mr, mv=mv))
        for c in chunks:
            f.write(f"Dialogue: 0,{ts(c['t0'])},{ts(c['t1'])},Cap,,0,0,0,,"
                    f"{{\\fad(90,90)}}{line(c['words'])}\n")
    return out
