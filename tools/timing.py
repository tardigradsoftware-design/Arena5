import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, FF, dur, build_timing, words_of
from scripts import V_BLOCKS, H_BLOCKS


def silences(path, noise=-32, d=0.18):
    p = subprocess.run([FF, "-hide_banner", "-i", path, "-af",
                        f"silencedetect=noise={noise}dB:d={d}", "-f", "null", "-"],
                       capture_output=True, text=True)
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", p.stderr)]
    se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", p.stderr)]
    iv = []
    for i, s in enumerate(ss):
        e = se[i] if i < len(se) else None
        if e:
            iv.append(((s + e) / 2, e - s))
    return iv


def snap(words, mids, total, start):
    """Cümle sınırlarını gerçek sessizlik ortalarına yasla."""
    idx = [i for i, w in enumerate(words) if w["w"].endswith((".", "!", "?", ":"))]
    if not idx:
        return words
    for i in idx[:-1]:
        t = words[i]["e"]
        if not mids:
            break
        best = min(mids, key=lambda m: abs(m[0] - t))
        if abs(best[0] - t) < 1.2 and start < best[0] < start + total:
            delta = best[0] - t
            for w in words[i + 1:]:
                w["s"] += delta
                w["e"] += delta
            words[i]["e"] += delta
    return words


def lay(blocks, pad=0.30):
    t, out = 0.0, []
    for b in blocks:
        path = os.path.join(ROOT, b["f"])
        d = dur(path)
        words = build_timing(b["text"], d, t)
        words = snap(words, silences(path), d, t)
        out.append(dict(b, d=round(d, 3), start=round(t, 3), words=words))
        t += d + pad
    return out, round(t, 3)


if __name__ == "__main__":
    vb, vt = lay(V_BLOCKS)
    hb, ht = lay(H_BLOCKS)
    for name, bl, tt in (("DIKEY", vb, vt), ("YATAY", hb, ht)):
        print(f"=== {name} {tt}s")
        for b in bl:
            print(f"  {b['start']:6.2f}-{b['start']+b['d']:6.2f} {b.get('sec','-'):12s} {len(b['words']):3d}w")
    json.dump({"v": vb, "vt": vt, "h": hb, "ht": ht},
              open(os.path.join(ROOT, "content/timing.json"), "w"), ensure_ascii=False, indent=1)
