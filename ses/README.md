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
