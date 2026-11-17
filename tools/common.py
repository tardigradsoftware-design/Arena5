import json, os, re, subprocess, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import shutil
FF = shutil.which("ffmpeg") or os.path.join(ROOT, "node_modules/@ffmpeg-installer/linux-x64/ffmpeg")
try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()   # xfade / modern filtreler
except Exception:
    pass
FP = FF
FONT_DIR = os.path.join(ROOT, "node_modules/@expo-google-fonts/inter")
F = {
    "black": os.path.join(FONT_DIR, "900Black/Inter_900Black.ttf"),
    "xb": os.path.join(FONT_DIR, "800ExtraBold/Inter_800ExtraBold.ttf"),
    "b": os.path.join(FONT_DIR, "700Bold/Inter_700Bold.ttf"),
    "sb": os.path.join(FONT_DIR, "600SemiBold/Inter_600SemiBold.ttf"),
    "m": os.path.join(FONT_DIR, "500Medium/Inter_500Medium.ttf"),
    "r": os.path.join(FONT_DIR, "400Regular/Inter_400Regular.ttf"),
}
BG = (10, 13, 18)
CARD = (22, 27, 35)
WHITE = (255, 255, 255)
MUTED = (147, 158, 174)
ACCENT = (255, 197, 61)
RED = (255, 90, 95)
GREEN = (52, 211, 153)


def dur(path):
    out = subprocess.run([FP, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    if not m:
        raise RuntimeError("no duration: " + path)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    return float(out.strip())


def words_of(text):
    return [w for w in re.split(r"\s+", text.strip()) if w]


def build_timing(text, total, start=0.0):
    """Distribute words over a block duration, weighted by length + sentence pauses."""
    ws = words_of(text)
    weights = []
    for i, w in enumerate(ws):
        base = max(2.0, len(w) + 1.0)
        if w.endswith((".", "!", "?", ":")):
            base += 4.0
        if w.endswith(","):
            base += 2.0
        weights.append(base)
    tot = sum(weights)
    t = start
    out = []
    for w, wt in zip(ws, weights):
        d = total * wt / tot
        out.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)})
        t += d
    return out


def chunks(words, max_words=3, max_chars=30):
    """Group word dicts into caption chunks."""
    out, cur = [], []
    for wd in words:
        trial = cur + [wd]
        txt = " ".join(x["w"] for x in trial)
        if len(trial) > max_words or len(txt) > max_chars:
            if cur:
                out.append(cur)
            cur = [wd]
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out


def find(words, phrase, start=0):
    """Index of first word starting a phrase."""
    p = words_of(phrase)
    for i in range(start, len(words) - len(p) + 1):
        if all(words[i + k]["w"].lower().strip(".,:;!?") == p[k].lower().strip(".,:;!?")
               for k in range(len(p))):
            return i
    raise ValueError("not found: " + phrase)


def t_at(words, phrase, start=0):
    return words[find(words, phrase, start)]["s"]
