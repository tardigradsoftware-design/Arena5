# Yayın metinleri — @hukuknotu

## 1) Dikey (48 sn) — `out/01_dikey_istifa-kidem.mp4`

**Kapak:** İSTİFA ETTİN, KIDEM GİTTİ SANDIN (üstü çizili "KIDEM TAZMİNATI" + YANLIŞ damgası)

**Açıklama:**
İstifa eden işçi kıdem tazminatı alamaz — ama kanun 4 kapı açık bırakıyor:
1) maaş ödenmiyorsa, 2) sigorta eksikse, 3) evlilik (1 yıl içinde), 4) askerlik. + emeklilik şartı.
Şart: aynı işverende 1 yıl. Hesap: her yıl 30 gün. Tavan 73.729,87 TL.
Bilgilendirme amaçlıdır, hukuki tavsiye değildir.

**Yorum kelimeleri (DM otomasyonu):** `maaş` · `sigorta` · `evlilik` · `askerlik` · `emeklilik`
**DM:** "Merhaba! Hukuk Notu belge listesi + fesih dilekçesi örneği 👇 (bilgilendirme amaçlıdır)"

**Etiketler:** #kıdemtazminatı #işhukuku #istifa #işçihakları #hukuk #kanun #tazminat #sgk

## 2) Yatay (3:54) — `out/02_yatay_istifa-kidem-detayli.mp4`

**Başlık:** İstifa Eden İşçi Kıdem Tazminatı Alabilir mi? | 4 İstisna, Hesap, Tavan, Dilekçe (2026)

**Açıklama (bölümler):**
00:00 Giriş · 00:10 Kural · 00:19 Dört kapı · 00:42 Ücret · 01:02 Sigorta · 01:08 Evlilik
01:20 Askerlik/emeklilik · 01:38 Hesap · 02:07 Tavan · 02:17 Örnek · 02:30 İhbar
02:45 İzin · 02:54 Usul/dilekçe · 03:10 Çıkış kodu · 03:15 Arabuluculuk · 03:25 Özet
Kaynak: 1475 s.K. m.14 (yürürlükte kalan hüküm), 4857 s.K. m.24, arabuluculuk (7036 s.K.).
Bilgilendirme amaçlıdır, hukuki tavsiye değildir; dosyanız için avukata danışın.

## Üretim hattı (yeniden üretmek için)
```
python3 tools/timing.py     # ses bloklarını hizala + kelime zamanları (content/timing.json)
python3 tools/render_v.py   # dikey 1080x1920
python3 tools/render_h.py   # yatay 1920x1080
```
senaryo: `tools/scripts.py` · dikey sahneler: `tools/scenes_v.py` · yatay sahneler: `tools/scenes_h.py`
ses: `content/*.mp3` (İstanbul Türkçesi erkek eğitimci sesi, voice-01)
