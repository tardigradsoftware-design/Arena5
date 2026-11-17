# -*- coding: utf-8 -*-
"""Yatay 1920x1080 adım adım anlatım sahneleri."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from common import WHITE, MUTED, ACCENT, RED, GREEN, CARD
from design import canvas, font, rr, text, para, wrap, stamp

W, H = 1920, 1080
BRAND = "@hukuknotu"
M = 110


def head(d, kicker, title, sub=None):
    f = font("sb", 30)
    tw = f.getlength(kicker)
    rr(d, (M, 108, M + tw + 46, 158), 25, fill=(30, 37, 48))
    text(d, (M + 23, 133), kicker, f, ACCENT, anchor="lm")
    y = 190
    ff = font("black", 78)
    for line_ in wrap(title, ff, W - 2 * M):
        d.text((M, y), line_, font=ff, fill=WHITE)
        y += 88
    if sub:
        y += 6
        for line_ in wrap(sub, font("m", 34), W - 2 * M):
            d.text((M, y), line_, font=font("m", 34), fill=MUTED)
            y += 44
    return y + 14


def card(d, box, fill=CARD, outline=(44, 53, 68), r=22, w=3):
    rr(d, box, r, fill=fill, outline=outline, width=w)


def chip(d, xy, label, color=ACCENT, size=32, pad=26):
    f = font("sb", size)
    tw = f.getlength(label)
    rr(d, (xy[0], xy[1], xy[0] + tw + pad * 2, xy[1] + size + 28), (size + 28) // 2, fill=(30, 37, 48), outline=color, width=2)
    text(d, (xy[0] + pad, xy[1] + (size + 28) // 2), label, f, color, anchor="lm")
    return xy[0] + tw + pad * 2 + 18


def table(d, x, y, w, cols, rows, colw=None, rh=64, hl=None, fs=30):
    colw = colw or [w / len(cols)] * len(cols)
    d.line([(x, y), (x + w, y)], fill=(56, 66, 84), width=2)
    cx = x
    for i, c in enumerate(cols):
        text(d, (cx + 18, y + 20), c, font("sb", fs - 2), MUTED)
        cx += colw[i]
    y += rh - 6
    for ri, row in enumerate(rows):
        hlrow = hl is not None and ri == hl
        if hlrow:
            rr(d, (x - 12, y - 10, x + w + 12, y + rh - 14), 14, fill=(40, 32, 12))
        cx = x
        for ci, cell in enumerate(row):
            col = ACCENT if hlrow and ci else (WHITE if ci == 0 else (205, 214, 228))
            text(d, (cx + 18, y + 8), str(cell), font("sb" if ci == 0 else "m", fs), col)
            cx += colw[ci]
        y += rh
        d.line([(x, y - 12), (x + w, y - 12)], fill=(38, 46, 60), width=1)
    return y


def steps(d, x, y, items, w=1180, rh=96, fs=36):
    for i, (n, t_, s_) in enumerate(items):
        yy = y + i * (rh + 14)
        card(d, (x, yy, x + w, yy + rh))
        rr(d, (x + 18, yy + 22, x + 70, yy + 74), 26, fill=ACCENT)
        text(d, (x + 44, yy + 48), str(n), font("black", 30), (10, 13, 18), anchor="mm")
        text(d, (x + 92, yy + 22), t_, font("sb", fs), WHITE)
        text(d, (x + 92, yy + 64), s_, font("m", 26), MUTED)


# ---------------- sahneler ----------------

def s_intro(img, d):
    text(d, (M, 96), "HUKUK NOTU  ·  İŞ HUKUKU", font("sb", 30), MUTED)
    y = 180
    f = font("black", 104)
    for line_ in ["İstifa eden işçi", "kıdem tazminatı", "alabilir mi?"]:
        d.text((M, y), line_, font=f, fill=WHITE if y != 180 else WHITE)
        y += 118
    d.text((M, y + 10), "alabilir mi?", font=f, fill=ACCENT) if False else None
    rr(d, (M, 640, M + 12, 900), 6, fill=ACCENT)
    para(d, (M + 44, 660), "1475 sayılı Kanun m. 14  ·  4857 sayılı Kanun m. 24",
         font("sb", 36), (215, 224, 236), maxw=1500, lh=1.5)
    para(d, (M + 44, 770), "Kural, dört istisna, hesap, tavan, dilekçe ve usul — sırayla.",
         font("m", 32), MUTED, maxw=1500)
    card(d, (1330, 620, 1810, 900), fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (1370, 660), "2026/2 tavanı", font("sb", 28), (220, 190, 90))
    text(d, (1370, 706), "73.729,87 TL", font("black", 62), ACCENT)
    text(d, (1370, 800), "Her yıl 30 gün", font("sb", 34), WHITE)
    text(d, (1370, 846), "Kesinti: damga vergisi", font("m", 26), MUTED)


def s_kural(img, d):
    y = head(d, "1 · KURAL", "Kural net: kendin ayrıldıysan kıdem yok")
    table(d, M, y + 20, 1120, ["Ayrılma biçimi", "Kıdem", "Dayanak"], [
        ("Sebepsiz istifa", "YOK", "1475 m. 14"),
        ("Haklı fesih (m. 24)", "VAR", "4857 m. 24"),
        ("Evlilik (1 yıl içinde)", "VAR", "1475 m. 14"),
        ("Askerlik", "VAR", "1475 m. 14"),
        ("Emeklilik şartı", "VAR", "1475 m. 14"),
    ], colw=[520, 220, 380], rh=78, hl=None, fs=32)
    card(d, (1290, y + 20, 1810, y + 400), fill=(28, 20, 26), outline=(70, 34, 40))
    text(d, (1330, y + 60), "En sık hata", font("sb", 28), (240, 200, 200))
    text(d, (1330, y + 108), "İstifa", font("black", 64), WHITE)
    text(d, (1330, y + 186), "dilekçesini", font("black", 64), WHITE)
    text(d, (1330, y + 264), "imzalamak.", font("black", 64), RED)
    text(d, (1330, y + 344), "Hak varsa da kaybettirir.", font("m", 26), MUTED)


def s_dort(img, d):
    y = head(d, "2 · İSTİSNALAR", "Kıdem hakkı doğuran dört kapı")
    items = [("1", "Ücret ödenmiyor", "4857 m. 24/II-e"),
             ("2", "Sigorta primi eksik", "4857 m. 24"),
             ("3", "Evlilik — 1 yıl", "1475 m. 14"),
             ("4", "Muvazzaf askerlik", "1475 m. 14")]
    bw = (W - 2 * M - 3 * 30) // 4
    for i, (n, t_, s_) in enumerate(items):
        x = M + i * (bw + 30)
        card(d, (x, y + 20, x + bw, y + 330))
        text(d, (x + 30, y + 50), n, font("black", 88), ACCENT)
        para(d, (x + 30, y + 170), t_, font("b", 40), WHITE, maxw=bw - 60, lh=1.2)
        text(d, (x + 30, y + 272), s_, font("m", 26), MUTED)
    card(d, (M, y + 366, W - M, y + 470), fill=(18, 30, 26), outline=(30, 70, 58))
    text(d, (M + 40, y + 396), "+ Emeklilik: 15 yıl sigortalılık ve 3600 prim günü şartını tamamlayan işçi de kıdem alır.",
         font("sb", 32), GREEN)


def s_kapi1(img, d):
    y = head(d, "3 · KAPI 1", "Ücretin ödenmemesi", "4857 sayılı İş Kanunu m. 24/II-e")
    steps(d, M, y + 20, [
        ("1", "Ücret geç ödeniyor", "Ödeme günü geçti, para gelmedi"),
        ("2", "Ücret eksik ödeniyor", "Maaş, fazla mesai veya prim eksik yatıyor"),
        ("3", "Yazılı bildirim yap", "Sebebi açıkça yaz: ücret ödenmediği için fesih"),
    ])
    card(d, (1330, y + 20, 1810, y + 360), fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (1370, y + 56), "Sonuç", font("sb", 28), (220, 190, 90))
    text(d, (1370, y + 100), "Haklı fesih", font("black", 54), ACCENT)
    text(d, (1370, y + 176), "İstifa değil.", font("sb", 32), WHITE)
    text(d, (1370, y + 220), "Kıdem + ihbar", font("sb", 32), WHITE)
    text(d, (1370, y + 264), "tazminatı doğar.", font("sb", 32), WHITE)
    text(d, (1370, y + 318), "İşsizlik ödeneği de mümkün.", font("m", 24), MUTED)


def s_kapi2(img, d):
    y = head(d, "4 · KAPI 2", "Sigorta primlerinin eksik yatırılması")
    steps(d, M, y + 20, [
        ("1", "SGK hizmet dökümünü al", "e-Devlet → 4A Hizmet Dökümü"),
        ("2", "Gün ve kazançları karşılaştır", "Çalıştığın gün sayısı ile ekrandaki gün tutuyor mu?"),
        ("3", "Farkı yazılı bildir", "Eksik prim nedeniyle haklı fesih + kıdem talebi"),
    ])
    card(d, (1330, y + 20, 1810, y + 330))
    text(d, (1370, y + 56), "Neye bakılır", font("sb", 28), MUTED)
    for i, t_ in enumerate(["Prim gün sayısı", "Bildirilen kazanç", "İşe giriş / çıkış tarihi"]):
        text(d, (1370, y + 110 + i * 56), "•  " + t_, font("m", 30), (210, 220, 234))
    text(d, (1370, y + 292), "Kanıt: hizmet dökümü + banka kaydı", font("m", 24), MUTED)


def s_kapi3(img, d):
    y = head(d, "5 · KAPI 3", "Evlilik nedeniyle ayrılma", "Kadın işçiye tanınan özel hak — 1475 m. 14")
    card(d, (M, y + 20, 900, y + 340), fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (M + 40, y + 54), "Süre", font("sb", 28), (220, 190, 90))
    text(d, (M + 40, y + 100), "1 yıl", font("black", 110), ACCENT)
    text(d, (M + 40, y + 240), "Evlilik tarihinden itibaren", font("m", 30), (215, 205, 170))
    card(d, (950, y + 20, 1810, y + 340), fill=(28, 20, 26), outline=(70, 34, 40))
    text(d, (990, y + 54), "Dikkat", font("sb", 28), (240, 200, 200))
    text(d, (990, y + 100), "1 yıl geçerse", font("black", 60), WHITE)
    text(d, (990, y + 176), "hak düşer.", font("black", 60), RED)
    text(d, (990, y + 270), "Evlilik belgesi (aile cüzdanı) ile bildirim yapılır.", font("m", 26), MUTED)
    card(d, (M, y + 372, W - M, y + 466), fill=CARD)
    text(d, (M + 40, y + 402), "Not: Bu hak cinsiyete özgüdür; erkek işçi evlilik nedeniyle kıdem alamaz. Askerlik ayrı bir başlıktır.",
         font("m", 30), (200, 210, 225))


def s_kapi4(img, d):
    y = head(d, "6 · KAPI 4", "Askerlik ve emeklilik")
    steps(d, M, y + 20, [
        ("1", "Muvazzaf askerlik", "1475 m. 14 — bedelli askerlik de Yargıtay içtihadıyla kapsamda"),
        ("2", "Sevk belgesini ibraz et", "İşverene yazılı bildirim + belge"),
        ("3", "Emeklilik şartı", "15 yıl sigortalılık + 3600 prim günü → SGK yazısı ile ayrılış"),
    ], w=1200)
    card(d, (1370, y + 20, 1810, y + 330))
    text(d, (1410, y + 56), "Belgeler", font("sb", 28), MUTED)
    for i, t_ in enumerate(["Askerlik sevk belgesi", "SGK hizmet dökümü", "Yazılı fesih bildirimi"]):
        text(d, (1410, y + 108 + i * 56), "•  " + t_, font("m", 28), (210, 220, 234))


def s_sart(img, d):
    y = head(d, "7 · HESAP", "Kıdem tazminatının iki şartı")
    card(d, (M, y + 20, 940, y + 300))
    text(d, (M + 40, y + 54), "Şart 1", font("sb", 28), MUTED)
    text(d, (M + 40, y + 98), "Aynı işverende en az 1 yıl", font("b", 46), WHITE)
    text(d, (M + 40, y + 176), "Ara verilerek çalışılan dönemler de eklenir.", font("m", 28), MUTED)
    card(d, (960, y + 20, 1810, y + 300), fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (1000, y + 54), "Şart 2", font("sb", 28), (220, 190, 90))
    text(d, (1000, y + 98), "Kanunda sayılan sebeple ayrılış", font("b", 46), ACCENT)
    text(d, (1000, y + 176), "Haklı fesih, evlilik, askerlik, emeklilik.", font("m", 28), (215, 205, 170))
    card(d, (M, y + 336, W - M, y + 470))
    text(d, (M + 40, y + 362), "Hesap: her tam yıl için 30 günlük giydirilmiş brüt ücret — artan süreler orantılı.",
         font("sb", 34), WHITE)
    text(d, (M + 40, y + 418), "Giydirilmiş = çıplak ücret + yol + yemek + ikramiye + düzenli yan haklar.",
         font("m", 28), MUTED)


def s_tavan(img, d):
    y = head(d, "8 · TAVAN VE KESİNTİ", "Tavan aşan kısım ödenmez")
    card(d, (M, y + 20, 1060, y + 330), fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (M + 40, y + 56), "2026 ikinci yarı kıdem tavanı (brüt)", font("sb", 30), (220, 190, 90))
    text(d, (M + 40, y + 110), "73.729,87 TL", font("black", 96), ACCENT)
    text(d, (M + 40, y + 250), "Tavan, yüksek ücretli çalışanı ilgilendirir.", font("m", 28), (215, 205, 170))
    card(d, (1080, y + 20, 1810, y + 330), fill=(18, 30, 26), outline=(30, 70, 58))
    text(d, (1120, y + 56), "Kesinti", font("sb", 30), (160, 220, 195))
    text(d, (1120, y + 106), "Yalnızca damga vergisi", font("b", 40), WHITE)
    text(d, (1120, y + 168), "binde 7,59", font("sb", 36), GREEN)
    text(d, (1120, y + 226), "Gelir vergisi ve SGK primi kesilmez.", font("m", 28), (190, 230, 210))
    card(d, (M, y + 366, W - M, y + 466))
    text(d, (M + 40, y + 396), "İhbar tazminatından ise gelir vergisi + damga vergisi kesilir. İki kalem aynı değildir.",
         font("m", 30), (205, 214, 228))


def s_ornek(img, d):
    y = head(d, "9 · ÖRNEK", "5 yıl 4 ay çalışan işçi")
    table(d, M, y + 20, 1120, ["Kalem", "Tutar"], [
        ("Giydirilmiş brüt ücret", "40.000 TL"),
        ("Kıdem süresi", "5 yıl 4 ay"),
        ("30 gün × 5,33 yıl", "≈ 213.200 TL"),
        ("Damga vergisi (binde 7,59)", "≈ 1.618 TL"),
        ("Net kıdem tazminatı", "≈ 211.600 TL"),
    ], colw=[720, 400], rh=76, hl=4, fs=32)
    card(d, (1290, y + 20, 1810, y + 350), fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (1330, y + 56), "Tavan kontrolü", font("sb", 28), (220, 190, 90))
    text(d, (1330, y + 100), "40.000 < 73.729", font("b", 38), WHITE)
    text(d, (1330, y + 160), "Tavan devreye girmez.", font("m", 28), (215, 205, 170))
    text(d, (1330, y + 226), "Ücret tavanın üstündeyse", font("m", 26), MUTED)
    text(d, (1330, y + 266), "hesap tavan üzerinden yapılır.", font("m", 26), MUTED)


def s_ihbar(img, d):
    y = head(d, "10 · DİĞER HAKLAR", "İhbar tazminatı: kıdeme göre bildirim süresi")
    table(d, M, y + 20, 1120, ["Çalışma süresi", "Bildirim", "Gün"], [
        ("6 aydan az", "2 hafta", "14"),
        ("6 ay – 1,5 yıl", "4 hafta", "28"),
        ("1,5 – 3 yıl", "6 hafta", "42"),
        ("3 yıldan fazla", "8 hafta", "56"),
    ], colw=[520, 320, 280], rh=80, hl=None, fs=32)
    card(d, (1290, y + 20, 1810, y + 380))
    text(d, (1330, y + 56), "Kural", font("sb", 28), MUTED)
    text(d, (1330, y + 100), "Süreye uymayan", font("sb", 32), WHITE)
    text(d, (1330, y + 146), "taraf öder.", font("sb", 32), WHITE)
    text(d, (1330, y + 212), "İşveren işçiyi çıkarırken", font("m", 26), MUTED)
    text(d, (1330, y + 250), "bildirim süresi vermezse", font("m", 26), MUTED)
    text(d, (1330, y + 288), "ihbar tazminatı doğar.", font("m", 26), MUTED)
    text(d, (1330, y + 336), "Tavan yok, gelir vergisi var.", font("sb", 26), ACCENT)


def s_izin(img, d):
    y = head(d, "11 · DİĞER HAKLAR", "Yıllık izin ve ücret alacakları")
    steps(d, M, y + 20, [
        ("1", "Kullanılmayan yıllık izin", "1–5 yıl: 14 gün · 5–15 yıl: 20 gün · 15 yıl+: 26 gün"),
        ("2", "Sözleşme sonunda nakit ödenir", "İzin ücreti zamanaşımına dikkat: 5 yıl"),
        ("3", "Fazla mesai ve ücret alacakları", "Yıllık 270 saat sınırı, %50 zamlı ödeme"),
    ], w=1200)
    card(d, (1370, y + 20, 1810, y + 370), fill=(28, 20, 26), outline=(70, 34, 40))
    text(d, (1410, y + 56), "Sakla", font("sb", 28), (240, 200, 200))
    for i, t_ in enumerate(["Bordrolar", "Banka kayıtları", "Giriş-çıkış kayıtları", "İzin formları"]):
        text(d, (1410, y + 104 + i * 52), "•  " + t_, font("m", 28), (235, 215, 215))
    text(d, (1410, y + 320), "İspat yükü çoğu kalemde işverende.", font("m", 24), MUTED)


def s_usul(img, d):
    y = head(d, "12 · USUL", "Dilekçe nasıl yazılır?")
    card(d, (M, y + 20, 1180, y + 520), fill=(247, 248, 250), outline=(210, 216, 226))
    text(d, (M + 40, y + 50), "İSTİFA DEĞİL — FESİH BİLDİRİMİ", font("sb", 26), (90, 100, 115))
    d.line([(M + 40, y + 96), (1180 - 40, y + 96)], fill=(215, 220, 230), width=2)
    body = ("İşverenliğinizde ... tarihinden bu yana çalışmaktayım. "
            "Ücretimin ... tarihinden itibaren ödenmemesi nedeniyle, 4857 sayılı İş Kanunu "
            "m. 24/II-e uyarınca iş sözleşmemi haklı nedenle sona erdiriyorum. "
            "Kıdem tazminatı, ihbar tazminatı, yıllık izin ve ücret alacaklarımın ödenmesini talep ederim.")
    para(d, (M + 40, y + 120), body, font("r", 30), (35, 42, 54), maxw=1000, lh=1.55)
    text(d, (M + 40, y + 430), "Ad Soyad / İmza / Tarih", font("sb", 26), (90, 100, 115))
    text(d, (M + 40, y + 470), "Tebliğ: noter veya iki tanık / e-posta ile", font("m", 26), (120, 130, 145))
    card(d, (1210, y + 20, 1810, y + 520), fill=(28, 20, 26), outline=(70, 34, 40))
    text(d, (1250, y + 56), "Yapma", font("sb", 28), (240, 200, 200))
    for i, t_ in enumerate(["“İstifa ediyorum” yazmak", "Sebepsiz dilekçe imzalamak",
                           "İbra / “tüm haklarımı aldım”", "Sözlü bildirimle ayrılmak"]):
        yy = y + 118 + i * 56
        d.line([(1250, yy - 10), (1268, yy + 8)], fill=(240, 120, 120), width=4)
        d.line([(1268, yy - 10), (1250, yy + 8)], fill=(240, 120, 120), width=4)
        text(d, (1286, yy), t_, font("m", 28), (240, 205, 205))
    text(d, (1250, y + 380), "Sonradan ispat çok zorlaşır.", font("sb", 28), RED)


def s_sgk(img, d):
    y = head(d, "13 · ÇIKIŞ KODU", "SGK çıkış kodu her şeyi belirler")
    table(d, M, y + 20, 1120, ["Kod", "Anlamı", "Kıdem"], [
        ("03", "İstifa (kendi ayrılış)", "YOK"),
        ("24", "Haklı fesih (işçi)", "VAR"),
        ("08", "Emeklilik", "VAR"),
        ("12", "Askerlik", "VAR"),
    ], colw=[200, 620, 300], rh=82, hl=0, fs=32)
    card(d, (1290, y + 20, 1810, y + 380), fill=(40, 32, 12), outline=(120, 96, 20))
    text(d, (1330, y + 56), "Kontrol et", font("sb", 28), (220, 190, 90))
    text(d, (1330, y + 100), "e-Devlet →", font("m", 28), (215, 205, 170))
    text(d, (1330, y + 140), "SGK Tescil ve", font("sb", 32), WHITE)
    text(d, (1330, y + 184), "Hizmet Dökümü", font("sb", 32), WHITE)
    text(d, (1330, y + 250), "Kod yanlışsa düzeltme talep et.", font("m", 26), MUTED)
    text(d, (1330, y + 300), "Süre: 5 yıl zamanaşımı.", font("sb", 26), ACCENT)


def s_arabulucu(img, d):
    y = head(d, "14 · YOL HARİTASI", "Dava değil, önce arabuluculuk")
    steps(d, M, y + 20, [
        ("1", "İşverene yazılı başvuru", "Alacakları kalem kalem yaz, süre ver"),
        ("2", "Arabuluculuk (zorunlu)", "İşçi alacaklarında dava şartı"),
        ("3", "Anlaşma olmazsa iş mahkemesi", "Zamanaşımı: fesih tarihinden 5 yıl"),
    ], w=1200)
    card(d, (1370, y + 20, 1810, y + 340))
    text(d, (1410, y + 56), "Süreler", font("sb", 28), MUTED)
    text(d, (1410, y + 104), "Arabuluculuk: 3 hafta", font("m", 28), (210, 220, 234))
    text(d, (1410, y + 150), "Dava: 5 yıl zamanaşımı", font("m", 28), (210, 220, 234))
    text(d, (1410, y + 214), "Haklı fesihte 6 iş günü", font("sb", 26), ACCENT)
    text(d, (1410, y + 252), "içinde fesih bildirimi", font("m", 24), MUTED)


def s_ozet(img, d):
    y = head(d, "15 · ÖZET", "Tek ekranda tüm cevap")
    table(d, M, y + 20, 1700, ["Durum", "Kıdem", "Hesap / not"], [
        ("Sebepsiz istifa", "YOK", "1475 m. 14 — kural"),
        ("Ücret / sigorta ihlali", "VAR", "4857 m. 24 · haklı fesih"),
        ("Evlilik (1 yıl içinde)", "VAR", "1475 m. 14"),
        ("Askerlik / emeklilik", "VAR", "Sevk belgesi / SGK yazısı"),
        ("Hesap", "30 gün / yıl", "Tavan 73.729,87 TL · damga vergisi"),
    ], colw=[620, 300, 780], rh=76, hl=None, fs=32)


def s_cta(img, d):
    d.text((M, 150), "Sen hangi durumdasın?", font=font("black", 90), fill=WHITE)
    xs = M
    for label in ["maaş", "sigorta", "evlilik", "askerlik", "emeklilik"]:
        xs = chip(d, (xs, 360), label, ACCENT, 34)
    card(d, (M, 520, 1180, 760))
    text(d, (M + 40, 560), "Yorumlara yaz → DM'den gönderiyorum", font("sb", 34), MUTED)
    text(d, (M + 40, 606), "Belge listesi + fesih dilekçesi örneği", font("b", 44), WHITE)
    text(d, (M + 40, 672), "Hangi kanun maddesi, hangi belge, hangi sıra — hepsi tek sayfada.", font("m", 28), MUTED)
    card(d, (1210, 520, 1810, 760), fill=(28, 20, 26), outline=(70, 34, 40))
    text(d, (1250, 556), "Hatırlatma", font("sb", 28), (240, 200, 200))
    para(d, (1250, 600), "Bu video bilgilendirme amaçlıdır, hukuki tavsiye değildir. Dosyan için avukata danış.",
         font("m", 26), (235, 215, 215), maxw=520, lh=1.4)
    text(d, (M, 830), "Hakkını bilmeyen, hakkını arayamaz.", font("black", 56), ACCENT)


SCENES = [
    (None, s_intro, "GİRİŞ"),
    ("Önce en kritik cümle", s_kural, "1 · KURAL"),
    ("Ama aynı kanun dört durumda", s_dort, "2 · İSTİSNALAR"),
    ("Birinci kapı", s_kapi1, "3 · KAPI 1"),
    ("İkinci kapı", s_kapi2, "4 · KAPI 2"),
    ("Üçüncü kapı", s_kapi3, "5 · KAPI 3"),
    ("Dördüncü kapı", s_kapi4, "6 · KAPI 4"),
    ("Şimdi hesap", s_sart, "7 · HESAP"),
    ("Tavanı aşan kısım", s_tavan, "8 · TAVAN"),
    ("Örnek: beş yıl", s_ornek, "9 · ÖRNEK"),
    ("İhbar tazminatı", s_ihbar, "10 · İHBAR"),
    ("İkincisi, kullanılmayan", s_izin, "11 · İZİN"),
    ("Şimdi usul", s_usul, "12 · USUL"),
    ("SGK çıkış", s_sgk, "13 · ÇIKIŞ KODU"),
    ("Alacaklar için arabuluculuk", s_arabulucu, "14 · YOL HARİTASI"),
    ("Özet:", s_ozet, "15 · ÖZET"),
    ("Hangi durumda olduğunu", s_cta, "KAPANIŞ"),
]
