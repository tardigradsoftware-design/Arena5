# -*- coding: utf-8 -*-
"""Dikey 1080x1920 sahneler. Her sahne bir cümleyle eşleşir (timing.py phrase ile bulur)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from common import WHITE, MUTED, ACCENT, RED, GREEN, CARD
from design import canvas, font, rr, text, para, wrap, strike, stamp

W, H = 1080, 1920
ZONE = (250, 1270)
BRAND = "@hukuknotu"


def header(img, d, label):
    text(d, (72, 88), BRAND, font("b", 40), MUTED)
    d.line([(72, 148), (W - 72, 148)], fill=(36, 43, 55), width=2)
    f = font("sb", 34)
    tw = f.getlength(label)
    rr(d, (72, 170, 72 + tw + 44, 228), 29, fill=(30, 37, 48))
    text(d, (94, 199), label, f, ACCENT, anchor="lm")


def footer(d, note="Bilgilendirme amaçlıdır. Hukuki tavsiye değildir."):
    d.line([(72, H - 236), (W - 72, H - 236)], fill=(36, 43, 55), width=2)
    text(d, (W // 2, H - 196), note, font("m", 30), (110, 122, 138), anchor="mm")
    text(d, (W // 2, H - 132), "hukuknotu  •  yorumlara yaz, dm'den al", font("sb", 32), (150, 160, 175), anchor="mm")


def big(d, xy, s, size=120, key="black", fill=WHITE, anchor="la", lh=1.06, maxw=940):
    f = font(key, size)
    x, y = xy
    for line_ in wrap(s, f, maxw):
        d.text((x, y), line_, font=f, fill=fill, anchor=anchor)
        y += int(size * lh)
    return y


def card(d, y, h, fill=CARD, outline=(44, 53, 68)):
    rr(d, (72, y, W - 72, y + h), 26, fill=fill, outline=outline, width=3)


def gate(d, y, no, title, ref, color=ACCENT):
    card(d, y, 132)
    rr(d, (104, y + 28, 180, y + 104), 38, fill=color)
    text(d, (142, y + 66), no, font("black", 46), (10, 13, 18), anchor="mm")
    text(d, (200, y + 34), title, font("black", 44), WHITE)
    text(d, (200, y + 88), ref, font("sb", 30), MUTED)


# ---------- sahneler ----------

def s_hook(img, d):
    big(d, (72, 270), "İstifa ettin.", 100, "b", MUTED)
    f = font("black", 118)
    d.text((72, 400), "Kıdem", font=f, fill=WHITE)
    d.text((72, 545), "tazminatı", font=f, fill=WHITE)
    strike(img, d, (56, 660, 700, 528))
    para(d, (72, 730), "gitti sandın.", font("black", 118), MUTED, maxw=800, lh=1.06)
    stamp(img, d, (800, 330), "YANLIŞ", RED, 54, -9)


def s_kural(img, d):
    big(d, (72, 280), "Doğru değil.", 100, "black", ACCENT)
    y = 430
    card(d, y, 150)
    text(d, (108, y + 34), "Kendin ayrıldıysan kıdem yok.", font("b", 44), WHITE)
    text(d, (108, y + 96), "1475 sayılı Kanun · m. 14", font("sb", 34), MUTED)
    card(d, y + 190, 190, fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (108, y + 226), "AMA", font("sb", 30), (220, 190, 90))
    text(d, (108, y + 274), "4 istisna var", font("black", 76), ACCENT)


def s_teaser(img, d):
    big(d, (72, 300), "Kanun dört", 96, "b", MUTED)
    big(d, (72, 400), "kapı açık", 128, "black", WHITE)
    big(d, (72, 540), "bırakıyor.", 128, "black", ACCENT)
    for i in range(4):
        x = 72 + i * 236
        rr(d, (x, 760, x + 200, 1010), 24, fill=CARD, outline=(44, 53, 68), width=3)
        rr(d, (x + 22, 786, x + 78, 842), 28, fill=ACCENT)
        text(d, (x + 50, 814), str(i + 1), font("black", 34), (10, 13, 18), anchor="mm")
        text(d, (x + 100, 900), ["MAAŞ", "SİGORTA", "EVLİLİK", "ASKER"][i],
             font("sb", 26), MUTED, anchor="mm")


def s_iki(img, d):  # kapı 1 + 2
    big(d, (72, 262), "1 · 2", 88, "black", ACCENT)
    gate(d, 400, "1", "Maaşın ödenmiyorsa", "4857 · m. 24/II-e")
    gate(d, 550, "2", "Sigortan eksik yatıyorsa", "4857 · m. 24")
    card(d, 720, 130, fill=(28, 20, 26), outline=(70, 34, 40))
    text(d, (108, 752), "Geç ödeme de, eksik ödeme de", font("sb", 32), (240, 200, 200))
    text(d, (108, 800), "haklı fesih sebebi.", font("b", 38), RED)


def s_uc(img, d):  # kapı 3 + 4
    big(d, (72, 262), "3 · 4", 88, "black", ACCENT)
    gate(d, 400, "3", "Evlilik: 1 yıl içinde", "1475 · m. 14")
    gate(d, 550, "4", "Askerlik: sevk belgesi", "1475 · m. 14")
    card(d, 720, 160, fill=(18, 30, 26), outline=(30, 70, 58))
    text(d, (108, 750), "Emeklilik: 15 yıl + 3600 gün", font("sb", 34), (190, 230, 210))
    text(d, (108, 800), "şartını tamamlayan da kıdem alır.", font("m", 28), GREEN)


def s_madde(img, d):
    big(d, (72, 280), "Haklı fesih", 100, "black", WHITE)
    card(d, 440, 240, fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (108, 480), "4857 sayılı İş Kanunu", font("sb", 32), (220, 190, 90))
    text(d, (108, 528), "m. 24", font("black", 96), ACCENT)
    text(d, (108, 636), "işçiye derhal fesih hakkı", font("m", 28), (210, 195, 150))
    big(d, (72, 720), "İstifa değil,", 76, "b", MUTED)
    big(d, (72, 812), "haklı fesih.", 96, "black", WHITE)
    stamp(img, d, (760, 1010), "KIDEM VAR", GREEN, 42, -7)


def s_sart(img, d):
    big(d, (72, 280), "Şart", 76, "b", MUTED)
    big(d, (72, 350), "Aynı işverende", 78, "black", WHITE)
    big(d, (72, 450), "en az 1 yıl", 120, "black", ACCENT)
    card(d, 620, 150)
    text(d, (108, 656), "Hesap", font("sb", 32), MUTED)
    text(d, (108, 700), "Her tam yıl için 30 gün", font("black", 52), WHITE)
    text(d, (108, 762), "giydirilmiş brüt ücret (yol, yemek, ikramiye dahil)",
         font("m", 26), (200, 210, 225))


def s_tavan(img, d):
    big(d, (72, 280), "2026/2 tavanı", 68, "b", MUTED)
    card(d, 360, 260, fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (108, 400), "Kıdem tazminatı tavanı", font("sb", 32), (220, 190, 90))
    text(d, (108, 450), "73.729,87 TL", font("black", 88), ACCENT)
    text(d, (108, 552), "Tavanı aşan kısım ödenmez.", font("m", 28), (210, 195, 150))
    card(d, 660, 170, fill=(18, 30, 26), outline=(30, 70, 58))
    text(d, (108, 692), "Kesinti: yalnızca damga vergisi", font("sb", 32), (190, 230, 210))
    text(d, (108, 740), "binde 7,59 · gelir vergisi yok", font("m", 26), GREEN)
    text(d, (108, 790), "SGK primi kesilmez.", font("m", 26), GREEN)


def s_ornek(img, d):
    big(d, (72, 262), "Örnek", 88, "black", WHITE)
    rows = [("Kıdem", "5 yıl 4 ay"), ("Giydirilmiş brüt", "40.000 TL"),
            ("Kıdem tazminatı", "≈213.000 TL"), ("Kesinti", "damga vergisi")]
    y = 390
    for i, (k, v) in enumerate(rows):
        col = ACCENT if i == 2 else WHITE
        rr(d, (72, y, W - 72, y + 112), 20, fill=CARD if i != 2 else (40, 32, 12))
        text(d, (104, y + 56), k, font("sb", 34), MUTED, anchor="lm")
        text(d, (W - 104, y + 56), v, font("b", 38), col, anchor="rm")
        y += 126


def s_cta(img, d):
    big(d, (72, 280), "Sen hangi", 88, "b", MUTED)
    big(d, (72, 370), "kapıdasın?", 120, "black", WHITE)
    y = 530
    for label in ["maaş", "sigorta", "evlilik", "askerlik"]:
        f = font("black", 48)
        tw = int(f.getlength(label) + 72)
        rr(d, (72, y, 72 + tw, y + 92), 46, fill=(30, 37, 48), outline=ACCENT, width=3)
        text(d, (72 + tw // 2, y + 46), label, f, ACCENT, anchor="mm")
        y += 108
    card(d, y + 8, 168)
    text(d, (104, y + 40), "Yorumlara yaz →", font("sb", 32), MUTED)
    text(d, (104, y + 84), "Belge listesi + dilekçe", font("b", 38), WHITE)
    text(d, (104, y + 132), "DM'den geliyor.", font("m", 28), MUTED)


# (cümle başlangıcı, fonksiyon, üst etiket)
SCENES = [
    (None, s_hook, "KIDEM TAZMİNATI"),
    ("Doğru değil", s_kural, "KURAL"),
    ("Ama kanun", s_teaser, "4 KAPI"),
    ("Bir:", s_iki, "KAPI 1 · 2"),
    ("Üç:", s_uc, "KAPI 3 · 4"),
    ("Maaş ve sigorta", s_madde, "MADDE"),
    ("Şart:", s_sart, "ŞART"),
    ("Tavan yetmiş", s_tavan, "TAVAN"),
    ("Şimdi yorumlara", s_cta, "SIRA SENDE"),
]
