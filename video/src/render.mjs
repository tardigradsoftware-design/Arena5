#!/usr/bin/env node
/**
 * Frame-accurate video renderer.
 *
 *   scene module  ->  SVG string per frame
 *                 ->  sharp rasterises to raw RGB (no browser needed)
 *                 ->  ffmpeg encodes MP4 straight from a pipe
 *
 * Deterministic by design: frame N always looks the same, so a timeline can be
 * split across machines (see GitHub Actions matrix in .github/workflows).
 *
 * Usage:
 *   node src/render.mjs --scene demo --out out/demo.mp4
 *   node src/render.mjs --scene demo --out out/demo.mp4 --audio voice.mp3
 *   node src/render.mjs --scene demo --out out/part0.mp4 --shard 0/4
 */
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { mkdir, writeFile } from 'node:fs/promises';
import { statSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import sharp from 'sharp';
import ffmpegInstaller from '@ffmpeg-installer/ffmpeg';

const FFMPEG = process.env.FFMPEG_PATH || ffmpegInstaller.path;

/* ---------------------------------- args --------------------------------- */

function parseArgs(argv) {
  const args = { scene: 'demo', out: 'out/video.mp4', crf: 20, preset: 'veryfast', workers: 0 };
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (!key.startsWith('--')) continue;
    const name = key.slice(2);
    const next = argv[i + 1];
    const val = next && !next.startsWith('--') ? next : 'true';
    if (next && !next.startsWith('--')) i++;
    args[name] = val;
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

/* --------------------------------- scene --------------------------------- */

const scenePath = path.resolve(
  args.scene.endsWith('.mjs') ? args.scene : `src/scenes/${args.scene}.mjs`,
);
const scene = await import(scenePath);
const meta = scene.meta;
const frameFn = scene.frame;

if (typeof frameFn !== 'function' || !meta) {
  throw new Error(`Scene ${scenePath} must export { meta, frame }`);
}

const fps = Number(args.fps || meta.fps || 30);
const width = Number(args.width || meta.width || 1920);
const height = Number(args.height || meta.height || 1080);
const totalFrames = Math.round((Number(args.duration || meta.duration) || 5) * fps);

/* --------------------------------- shard --------------------------------- */

let from = 0;
let to = totalFrames;
if (args.shard) {
  const [index, count] = String(args.shard).split('/').map(Number);
  const per = Math.ceil(totalFrames / count);
  from = index * per;
  to = Math.min(totalFrames, from + per);
} else if (args.from || args.to) {
  from = Number(args.from || 0);
  to = Number(args.to || totalFrames);
}
const shardFrames = Math.max(0, to - from);

/* -------------------------------- render --------------------------------- */

const workers = Number(args.workers) || Math.max(1, Math.min(os.cpus().length, 8));

async function rasterise(svg) {
  // librsvg keeps text as vectors, so we get crisp glyphs at any size.
  return sharp(Buffer.from(svg), { limitInputPixels: false })
    .flatten({ background: '#0b1020' })
    .raw()
    .toBuffer();
}

async function frameBuffer(i) {
  const t = i / fps;
  const svg = frameFn(t, { i, fps, width, height, totalFrames, meta });
  return rasterise(svg);
}

async function renderShard(outFile) {
  await mkdir(path.dirname(path.resolve(outFile)), { recursive: true });

  const ffArgs = [
    '-hide_banner', '-loglevel', 'error', '-y',
    '-f', 'rawvideo',
    '-pix_fmt', 'rgb24',
    '-s', `${width}x${height}`,
    '-r', String(fps),
    '-i', 'pipe:0',
  ];

  if (args.audio) {
    ffArgs.push('-i', path.resolve(args.audio));
  }

  ffArgs.push(
    '-c:v', 'libx264',
    '-preset', String(args.preset),
    '-crf', String(args.crf),
    '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart',
  );

  if (args.audio) {
    ffArgs.push('-map', '0:v:0', '-map', '1:a:0', '-c:a', 'aac', '-b:a', '192k', '-shortest');
  }

  ffArgs.push(path.resolve(outFile));

  const ff = spawn(FFMPEG, ffArgs, { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = once(ff, 'close');

  const started = Date.now();
  const window = workers;
  const pending = new Map();
  for (let i = from; i < Math.min(to, from + window); i++) pending.set(i, frameBuffer(i));

  for (let i = from; i < to; i++) {
    const buf = await pending.get(i);
    pending.delete(i);
    const nextIndex = i + window;
    if (nextIndex < to) pending.set(nextIndex, frameBuffer(nextIndex));

    if (!ff.stdin.write(buf)) await once(ff.stdin, 'drain');

    const rendered = i - from + 1;
    if (rendered % Math.max(1, Math.round(shardFrames / 12)) === 0 || rendered === shardFrames) {
      const pct = ((rendered / shardFrames) * 100).toFixed(0);
      const fpsNow = rendered / ((Date.now() - started) / 1000);
      process.stdout.write(`\r  kare ${String(rendered).padStart(4)}/${shardFrames}  %${pct}  ${fpsNow.toFixed(1)} kare/sn   `);
    }
  }

  ff.stdin.end();
  const [code] = await done;
  process.stdout.write('\n');
  if (code !== 0) throw new Error(`ffmpeg exited with ${code}`);

  const seconds = (shardFrames / fps).toFixed(2);
  const size = statSync(path.resolve(outFile)).size;
  console.log(`✓ ${path.relative(process.cwd(), outFile)} — ${seconds}s, ${(size / 1024 / 1024).toFixed(2)} MB, ${workers} worker, ${((Date.now() - started) / 1000).toFixed(1)}s render`);
}

console.log(`▸ scene=${args.scene} ${width}x${height} @${fps}fps · ${shardFrames} kare (${(shardFrames / fps).toFixed(2)}s) · ${workers} worker`);
if (args['write-meta']) {
  await writeFile(
    path.resolve(args['write-meta']),
    JSON.stringify({ width, height, fps, totalFrames, duration: totalFrames / fps }, null, 2),
  );
}
await renderShard(args.out);
