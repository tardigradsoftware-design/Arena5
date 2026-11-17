#!/usr/bin/env python3
"""Build labelled voice options: pitch-shift a base take to N targets and
stitch label + sample pairs into one comparison file.

    python3 tools/make-voice-options.py --base ../audio/base-v05.mp3 \
        --out ../audio/secenekler.mp3 \
        --options 1.0 ../audio/label1.mp3 1.15 ../audio/label2.mp3 1.35 ../audio/label3.mp3
"""
import argparse
import json
import math
import subprocess
import tempfile

FFMPEG = json.loads(
    subprocess.check_output(
        ["node", "-e", "import('@ffmpeg-installer/ffmpeg').then(m=>console.log(JSON.stringify({p:m.default.path})))"],
        text=True,
    )
)["p"]


def sample_rate(path):
    """Read the real sample rate from ffmpeg's banner (TTS files are often 24 kHz)."""
    out = subprocess.run(
        [FFMPEG, "-hide_banner", "-i", path], capture_output=True, text=True
    ).stderr
    for line in out.splitlines():
        if "Audio:" in line and " Hz" in line:
            return int(line.split(" Hz")[0].split(",")[-1].strip())
    return 44100


def shift(input_path, output_path, factor):
    """Pitch shift by `factor` while keeping the original duration."""
    sr = sample_rate(input_path)
    if abs(factor - 1.0) < 1e-6:
        af = "highpass=f=120,treble=g=3"
    else:
        tempo = 1 / factor
        if tempo >= 0.5:
            af = f"asetrate={sr}*{factor},aresample=44100,atempo={tempo:.6f},highpass=f=120,treble=g=3"
        else:
            s = math.sqrt(tempo)
            af = (
                f"asetrate={sr}*{factor},aresample=44100,"
                f"atempo={s:.6f},atempo={s:.6f},highpass=f=120,treble=g=3"
            )
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", input_path,
         "-af", af, "-c:a", "libmp3lame", "-b:a", "96k", output_path],
        check=True,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument(
        "--options", nargs="+", required=True,
        help="pairs: factor labelfile factor labelfile ...",
    )
    a = ap.parse_args()

    pairs = list(zip(a.options[0::2], a.options[1::2]))
    tmp = tempfile.mkdtemp()
    segments = []
    for i, (factor, label) in enumerate(pairs):
        sample = f"{tmp}/opt{i}.mp3"
        shift(a.base, sample, float(factor))
        segments += [label, sample]

    inputs, filters = [], []
    for i, seg in enumerate(segments):
        inputs += ["-i", seg]
        filters.append(f"[{i}:a]")
    graph = "".join(filters) + f"concat=n={len(segments)}:v=0:a=1[a]"
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", *inputs,
         "-filter_complex", graph, "-map", "[a]",
         "-c:a", "libmp3lame", "-b:a", "96k", a.out],
        check=True,
    )
    print(f"✓ {a.out} ({len(pairs)} seçenek)")


if __name__ == "__main__":
    main()
