import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from common import F, BG, CARD, WHITE, MUTED, ACCENT, RED, GREEN

_fc = {}


def font(key, size):
    k = (key, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(F[key], size)
    return _fc[k]


def canvas(w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    # subtle dot grid
    for y in range(0, h, 48):
        for x in range(0, w, 48):
            d.point((x, y), fill=(20, 25, 34))
    return img, d


def glow(img, box, color=ACCENT, alpha=64, blur=160):
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse(box, fill=tuple(int(c * alpha / 255) for c in color))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.blend(img, Image.blend(img, layer, 0.0), 0.0) if False else Image.composite(
        Image.blend(img, layer, 1.0), img, Image.new("L", img.size, 255)) if False else _add(img, layer)


def _add(base, layer):
    from PIL import ImageChops
    return ImageChops.add(base, layer)


def rr(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def text(d, xy, s, f, fill=WHITE, anchor="la", spacing=0):
    if spacing == 0:
        d.text(xy, s, font=f, fill=fill, anchor=anchor)
        return
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill, anchor=anchor)
        x += f.getlength(ch) + spacing


def wrap(s, f, maxw):
    out, line = [], ""
    for w in s.split():
        t = (line + " " + w).strip()
        if f.getlength(t) <= maxw or not line:
            line = t
        else:
            out.append(line)
            line = w
    if line:
        out.append(line)
    return out


def para(d, xy, s, f, fill=WHITE, maxw=800, lh=1.25, anchor="la"):
    x, y = xy
    for line in wrap(s, f, maxw):
        d.text((x, y), line, font=f, fill=fill, anchor=anchor)
        y += int(f.size * lh)
    return y


def strike(img, d, box, color=RED, w=9):
    d.line([(box[0], box[3] - 14), (box[2], box[1] + 14)], fill=color, width=w)


def stamp(img, d, center, label, color=RED, size=54, ang=8):
    f = font("black", size)
    tw = int(f.getlength(label) + 60)
    th = int(size * 1.9)
    lay = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    rr(ld, (0, 0, tw - 1, th - 1), 14, outline=color + (255,), width=7)
    ld.text((tw // 2, th // 2), label, font=f, fill=color + (255,), anchor="mm")
    lay = lay.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(lay, (center[0] - lay.width // 2, center[1] - lay.height // 2), lay)
