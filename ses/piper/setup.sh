#!/usr/bin/env bash
# Piper kurulumu — tamamen yerel, ücretsiz, gerçek Türkçe sesler.
# Bu sandbox'ta Hugging Face kapalı olduğu için burada çalışmaz; kendi
# bilgisayarında çalıştır (internet açık).
#
#   bash ses/piper/setup.sh            # kurulum + Türkçe ses listesi
#   bash ses/piper/setup.sh fahrettin  # belirli bir sesi indir
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HERE/.venv"
VOICES="$HERE/voices"
mkdir -p "$VOICES"

if [ ! -d "$VENV" ]; then
  echo "▸ sanal ortam kuruluyor: $VENV"
  python3 -m venv "$VENV"
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "▸ piper-tts kuruluyor"
pip install --quiet --upgrade pip
pip install --quiet piper-tts

echo
echo "▸ Hugging Face'teki Türkçe (tr_TR) sesler:"
python3 - "$VOICES" <<'PY'
import json, sys, urllib.request
out = urllib.request.urlopen(
    "https://huggingface.co/api/models/rhasspy/piper-voices/tree/main/tr/tr_TR"
).read()
items = json.loads(out)
for it in items:
    if it["path"].endswith(".onnx"):
        print("  -", it["path"].split("tr_TR/")[-1].replace(".onnx", ""))
PY

WANT="${1:-}"
if [ -z "$WANT" ]; then
  echo
  echo "Bir ses seç ve indir, örn:"
  echo "  bash ses/piper/setup.sh fahrettin"
  exit 0
fi

MODEL="tr_TR-${WANT}-medium"
BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main/tr/tr_TR/${MODEL}"
echo "▸ indiriliyor: $MODEL"
curl -fL --progress-bar "$BASE.onnx" -o "$VOICES/$MODEL.onnx"
curl -fL --progress-bar "$BASE.onnx.json" -o "$VOICES/$MODEL.onnx.json"

echo
echo "✓ hazır. Test:"
echo "  bash ses/piper/say.sh \"Merhaba, bugün kira sözleşmesini konuşuyoruz.\" ${WANT}"
