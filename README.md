# Arena5

## Kilitli ses (değişmez kural)

Tüm videolar **voice-11** ile seslendirilir — genç hukukçu karakteri.
Ayrıntılar ve işlem zinciri: `ses/karakter-hukukcu.json`

```bash
# ses
python: generate_speech(voice_id="voice-11", text=..., file_path="ses/ham-<konu>.wav")  # .wav iste, mp3 değil
ffmpeg -i ses/ham-<konu>.wav -af "$(jq -r .islem_zinciri ses/karakter-hukukcu.json)" -ar 44100 ses/karakter-<konu>.wav
# video
cd video && node src/render.mjs --scene hukuk --out hukuk.mp4 --audio ../ses/karakter-<konu>.wav
```

Kurallar: ses her videoda aynı; pitch/tını oynatma yok; metin tamamen Türkçe; kısa cümleler.
