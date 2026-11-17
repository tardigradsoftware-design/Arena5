# ses/ — aksansız Türkçe seslendirme

## Sorun

Bu ortamdaki hazır sesler **bölgesel (tr-TR) model içermiyor**. Denendi:

```
generate_speech(language="tr-TR") -> "Voice cannot honor the accent/region requested"
```

Yani mevcut havuzda İstanbul Türkçesi modeli yok; aksan sonradan EQ/kompresörle
düzeltilemez. Kısır döngünün sebebi buydu.

## Çözüm: yerel Piper (ücretsiz, açık kaynak, gerçek Türkçe)

Piper modelleri Hugging Face'ten geliyor; **bu sandbox'ta HF kapalı**. Kendi
bilgisayarında tek komutla kurulur, model bir kez iner, sonrası tamamen çevrimdışı.

```bash
# 1) kurulum + mevcut Türkçe sesleri listele
bash ses/piper/setup.sh

# 2) beğendiğin sesi indir (ör. fahrettin / dfki / fettah — liste kurulumda çıkar)
bash ses/piper/setup.sh fahrettin

# 3) tek cümle test et
bash ses/piper/say.sh "Merhaba, bugün kira sözleşmesini konuşuyoruz." fahrettin
```

Üretilen WAV doğrudan video hattına girer:

```bash
cd video
node src/render.mjs --scene demo --out demo.mp4 --audio ../ses/piper/out/fahrettin.wav
```

`say.sh` metni cümlelere bölüp parça parça sentezler (uzun metinde prosodi
bozulmasın diye), sonra birleştirir. Çıktı 22.05 kHz WAV; hattaki AAC 192k encode
için fazlasıyla yeterli.

## Alternatifler

| Yol | Aksan | Not |
|---|---|---|
| Piper (yerel) | Doğal Türkçe | Ücretsiz, çevrimdışı, ses seçilebilir — **önerilen** |
| Hazır platform sesleri | Aksanlı | Bu ortamda tr-TR modeli yok |
| Kendi kaydın | Kusursuz | `--audio` ile herhangi bir WAV/MP3 girer |
| Ticari TTS (ElevenLabs vb.) | Doğal | Ücretli, anahtar gerekir |

## Kurallar (tutarlılık)

- Ses her videoda aynı model dosyasıyla üretilir (`ses/piper/voices/*.onnx`).
- Metin cümle cümle sentezlenir; hız/ton modelin kendi varsayılanıdır.
- Video kodlaması: AAC 192 kbps. Ses dosyası asla mp3 32 kbps'e düşürülmez.

## hukuk3 — konuşma senkronlu sahne

`ses/hukuk3/` altında cümle cümle seslendirme var. `build_audio.py` bunları
temizleyip birleştiriyor ve **zaman çizelgesini** üretiyor:

```
ses/hukuk3/sN.wav            -> ham TTS (voice-11)
ses/hukuk3/build_audio.py    -> temizlik + birleştirme + timing
ses/hukuk3/ses.wav           -> final ses
video/src/scenes/hukuk3-timing.json  -> sahnenin okuduğu beat zamanları
```

Sahne `frame(t)` içinde bu beat'lere bakarak başlık, kart ve maskot ifadesini
değiştirir. Yeni video için: metni cümlelere böl → `sN.wav` üret → betiği çalıştır
→ `node src/render.mjs --scene hukuk3 --out x.mp4 --audio ../ses/hukuk3/ses.wav`.

## hukuk4 — "shorts" stili (karaoke altyazı + efekt)

- `video/src/scenes/hukuk4.mjs`: kelime kelime vurgulanan karaoke altyazı, kısa
  kanca başlığı, adım kartları (ikonlu), maskot punch-in, uyarı beat'inde
  hafif sarsıntı, CTA balonu.
- `ses/hukuk3/mix_sfx.py`: whoosh / pop / ding efektlerini numpy ile miksler
  (`ses/hukuk3/ses-sfx.wav`). Eski ffmpeg'de `amix normalize` olmadığı için
  karıştırma ffmpeg yerine doğrudan örnek toplama ile yapılıyor.
