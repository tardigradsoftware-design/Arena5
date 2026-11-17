# video/ — kodla video üretim hattı

Tarayıcısız, lisanssız, deterministik render hattı.

```
sahne kodu (JS)  →  her kare için SVG  →  sharp (raster)  →  ffmpeg (pipe)  →  MP4
```

- **Remotion/Revideo gerekmez.** Chromium indirme derdi yok; sunucuda, konteynerde,
  CI'da aynı sonucu verir.
- **Deterministik.** Kare N her zaman aynı görüntüyü üretir, bu yüzden zaman çizelgesi
  parçalara (shard) bölünüp paralel render edilebilir.
- **Sıfır maliyet.** Tek bağımlılık: `sharp` (npm) + `@ffmpeg-installer/ffmpeg` (npm'den
  statik ffmpeg binary'si).

## Hızlı başlangıç

```bash
cd video
npm install
npm run render:demo            # out/demo.mp4 (14 sn, sesli değil)
```

Ses eklemek için:

```bash
node src/render.mjs --scene demo --out out/demo.mp4 --audio assets/voice-tr-14s.m4a
```

Paralel render (shard) + birleştirme:

```bash
for i in 0 1 2 3; do node src/render.mjs --scene demo --shard $i/4 --out out/part-$i.mp4 & done; wait
node src/concat.mjs --out out/final.mp4 --audio assets/voice-tr-14s.m4a out/part-*.mp4
```

## Yeni sahne yazmak

`src/scenes/<isim>.mjs` dosyası iki şey export eder:

```js
export const meta = { fps: 30, width: 1280, height: 720, duration: 10 };
export function frame(t, ctx) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">…</svg>`;
}
```

`frame(t)` **saf fonksiyon** olmalı: sadece `t`'ye (saniye) ve `ctx`'e bakmalı, saat/tarih
gibi dış duruma bakmamalı. `src/lib/motion.mjs` (easing, spring) ve `src/lib/svg.mjs`
(metin, şekil, palet yardımcıları) hazır.

## Bayraklar

| Bayrak | Anlamı |
|---|---|
| `--scene demo` | `src/scenes/demo.mjs` |
| `--out out/x.mp4` | çıktı |
| `--audio a.mp3` | sesi mux'la (AAC 192k, `-shortest`) |
| `--shard 2/6` | zaman çizelgesinin 3. dilimi |
| `--from/--to` | kare aralığı |
| `--width/--height/--fps/--duration` | meta'yı ez |
| `--crf/--preset` | x264 kalite/hız |
| `--workers` | paralel kare sayısı (varsayılan: CPU, en fazla 8) |

## Hız (ölçüldü)

| Ortam | Çekirdek | 14 sn / 720p30 | Not |
|---|---|---|---|
| Bu sandbox | 2 vCPU | **13 s** (~32 kare/sn) | gerçek zamanlıdan hızlı |
| Tipik dizüstü | 8–16 | ~4–6 s | |
| GitHub Actions | 4 vCPU × 6 shard | ~3–5 s toplam | ücretsiz, paralel |

## GitHub Actions

`.github/workflows/render.yml` — `workflow_dispatch` ile çalışır: 6 shard paralel render
eder, `stitch` işi birleştirip `video` artifact'ı olarak yükler.

```bash
gh workflow run render.yml -f scene=demo
gh run watch
gh run download --name video -D out
```

## Ses (seslendirme)

TTS çıktısı doğrudan kullanılıyor, ama gerektiğinde ffmpeg ile gerçek bir tını
dönüşümü uygulanıyor (iddia değil, ölçümle doğrulanıyor):

```bash
# ham TTS -> çocuk sesi (f0 ~250 Hz, 7 yaş aralığı), süre korunur
ffmpeg -i raw.mp3 -af "asetrate=44100*2.5,aresample=44100,atempo=0.6166,atempo=0.6166,highpass=f=140,treble=g=3" -c:a libmp3lame -b:a 96k child.mp3

# doğrulama: medyan f0 ve tını merkezi
python3 tools/voice-stats.py demo.mp4
```

Ölçülen değerler: yetişkin erkek ~104 Hz, çocuk sürümü ~250 Hz (p10–p90: 193–327 Hz).

### Ses kalitesi (önemli)

TTS çıktısını **mp3 olarak istemeyin**: 24 kHz / 32 kbps geliyor ve boğuk,
işlenmiş duyuluyor. `.wav` isteyin → 44.1 kHz / 16-bit. Video kodlaması zaten AAC
192k olduğu için tekrar sıkıştırma kaybı da olmuyor.

```bash
# adayları aynı cümleyle, ses seviyesi eşitlenmiş tek dosyada karşılaştır
python3 tools/voice-stats.py ../audio/aday-*.wav
```
