#!/usr/bin/env bash
# Yerel Piper ile Türkçe seslendirme üret.
#
#   bash ses/piper/say.sh "Metin" fahrettin            -> ses/piper/out/fahrettin.wav
#   bash ses/piper/say.sh "Metin" fahrettin hikaye.wav  -> ses/piper/out/hikaye.wav
#
# Çıktı 22.05 kHz WAV'dır; video hattı bunu doğrudan --audio ile kullanır:
#   cd video && node src/render.mjs --scene demo --out demo.mp4 --audio ../ses/piper/out/hikaye.wav
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HERE/.venv"
MODEL_NAME="${2:?kullanım: say.sh \"metin\" <ses-adı> [çıktı.wav]}"
MODEL="$HERE/voices/tr_TR-${MODEL_NAME}-medium.onnx"
OUT="${3:-$HERE/out/${MODEL_NAME}.wav}"

TEXT="${1:?kullanım: say.sh \"metin\" <ses-adı> [çıktı.wav]}"

if [ ! -f "$MODEL" ]; then
  echo "✗ model yok: $MODEL" >&2
  echo "  önce: bash ses/piper/setup.sh ${MODEL_NAME}" >&2
  exit 1
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"
mkdir -p "$(dirname "$OUT")"

# Uzun metni cümlelere bölüp sırayla sentezleyip birleştiriyoruz; tek seferde
# uzun metin verildiğinde prosodi bozulabiliyor.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "$TEXT" | python3 - "$TMP" <<'PY'
import re, sys, pathlib
tmp = pathlib.Path(sys.argv[1])
text = sys.stdin.read().strip()
parts = [p.strip() for p in re.split(r'(?<=[.!?…])\s+', text) if p.strip()]
for i, p in enumerate(parts):
    (tmp / f"{i:03d}.txt").write_text(p, encoding="utf-8")
print(f"{len(parts)} cümle")
PY

i=0
for f in "$TMP"/*.txt; do
  echo "$(cat "$f")" | piper -m "$MODEL" -f "$TMP/$(printf '%03d' "$i").wav" >/dev/null 2>&1
  i=$((i+1))
done

python3 - "$TMP" "$OUT" <<'PY'
import sys, wave, pathlib
tmp, out = pathlib.Path(sys.argv[1]), sys.argv[2]
files = sorted(tmp.glob("*.wav"))
with wave.open(out, "wb") as w:
    params = None
    for f in files:
        with wave.open(str(f), "rb") as r:
            if params is None:
                params = r.getparams()
                w.setparams(params)
            w.writeframes(r.readframes(r.getnframes()))
print(f"✓ {out}")
PY
