#!/usr/bin/env node
/** Join rendered shards into one file (stream copy, no re-encode).
 *
 *   node src/concat.mjs --out out/final.mp4 out/part0.mp4 out/part1.mp4
 *   node src/concat.mjs --out out/final.mp4 --audio voice.mp3 out/part*.mp4
 */
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import ffmpegInstaller from '@ffmpeg-installer/ffmpeg';

const FFMPEG = process.env.FFMPEG_PATH || ffmpegInstaller.path;

const argv = process.argv.slice(2);
const outIndex = argv.indexOf('--out');
const audioIndex = argv.indexOf('--audio');
const out = path.resolve(argv[outIndex + 1]);
const audio = audioIndex >= 0 ? path.resolve(argv[audioIndex + 1]) : null;

const padders = new Set([outIndex, outIndex + 1, audioIndex, audioIndex + 1]);
const parts = argv.filter((a, i) => !a.startsWith('--') && !padders.has(i)).map((p) => path.resolve(p));

if (parts.length === 0) {
  console.error('kullanım: node src/concat.mjs --out out/final.mp4 part0.mp4 part1.mp4');
  process.exit(1);
}

const dir = await mkdtemp(path.join(os.tmpdir(), 'concat-'));
const listFile = path.join(dir, 'list.txt');
await writeFile(listFile, parts.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join('\n') + '\n');

const ffArgs = ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', listFile];
if (audio) ffArgs.push('-i', audio);
ffArgs.push('-c:v', 'copy');
if (audio) ffArgs.push('-map', '0:v:0', '-map', '1:a:0', '-c:a', 'aac', '-b:a', '192k', '-shortest');
ffArgs.push('-movflags', '+faststart', out);

const ff = spawn(FFMPEG, ffArgs, { stdio: 'inherit' });
const [code] = await once(ff, 'close');
await rm(dir, { recursive: true, force: true });
if (code !== 0) process.exit(code);
console.log(`✓ ${path.relative(process.cwd(), out)} (${parts.length} parça)`);
