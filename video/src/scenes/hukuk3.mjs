import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { progress, easeOutCubic, easeOutExpo, spring, clamp, lerp } from '../lib/motion.mjs';
import { palette as P, rect, line, svgDoc, esc, FONT_MONO } from '../lib/svg.mjs';
import { mascot } from '../lib/mascot.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const timing = JSON.parse(readFileSync(path.join(here, 'hukuk3-timing.json'), 'utf8'));
const B = timing.beats;

export const meta = {
  fps: timing.fps,
  width: timing.width,
  height: timing.height,
  duration: timing.duration,
  title: 'hukuk3-sirket-kurulusu',
};

const W = meta.width;
const H = meta.height;
const M = 44;
const ACCENT = P.accent;

const defs = `
  <radialGradient id="vign" cx="50%" cy="34%" r="70%">
    <stop offset="0%" stop-color="#1a2748" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="${P.ink}" stop-opacity="1"/>
  </radialGradient>
  <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="${P.accent}"/><stop offset="100%" stop-color="${P.accent3}"/>
  </linearGradient>
  <linearGradient id="warnbar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="${P.warn}"/><stop offset="100%" stop-color="${P.accent3}"/>
  </linearGradient>`;

function background(t) {
  const grid = [];
  for (let y = 0; y <= H; y += 80) grid.push(line(0, y, W, y, '#ffffff', 1, 'opacity="0.025"'));
  for (let x = 0; x <= W; x += 80) grid.push(line(x, 0, x, H, '#ffffff', 1, 'opacity="0.025"'));
  const glow = Math.sin(t * 0.5) * 40;
  return `${rect(0, 0, W, H, 'url(#vign)')}${grid.join('')}
    <circle cx="${W / 2 + glow}" cy="300" r="320" fill="${ACCENT}" opacity="0.05"/>`;
}

function chrome(t) {
  const p = clamp(t / meta.duration);
  return `
    ${rect(0, 0, W, 6, '#1b2542')}
    ${rect(0, 0, W * p, 6, 'url(#bar)')}
    ${rect(M, 46, 118, 40, '#141c33', 20, 'stroke="#2a3557" stroke-width="1.5"')}
    <text x="${M + 59}" y="${73}" font-family="${FONT_MONO}" font-size="19" fill="${ACCENT}" text-anchor="middle">HQK TV</text>`;
}

/** Büyük başlık satırları; her satır gecikmeli girer. */
function caption(t, lines, { start = 0, size = 60, color = P.paper, y = 210, weight = 800 } = {}) {
  return lines
    .map((ln, i) => {
      const p = easeOutCubic(progress(t, start + i * 0.12, start + 0.55 + i * 0.12));
      if (p <= 0) return '';
      const dy = (1 - p) * 26;
      const fill = typeof ln === 'string' ? color : ln.color || color;
      const text = typeof ln === 'string' ? ln : ln.text;
      return `<text x="${M}" y="${y + i * (size * 1.16) + dy}" opacity="${p}"
        font-family="'DejaVu Sans'" font-size="${size}" font-weight="${weight}" fill="${fill}">${esc(text)}</text>`;
    })
    .join('');
}

function stepCard(t, start, num, title, sub, accent = ACCENT) {
  const p = spring(clamp((t - start) / 0.75));
  if (p <= 0.001) return '';
  const y = 690 + (1 - clamp(p)) * 34;
  return `<g opacity="${clamp(p)}">
    ${rect(M, y, W - M * 2, 210, '#141c33', 26, 'stroke="#2a3557" stroke-width="2"')}
    ${rect(M, y, 8, 210, accent, 4)}
    <text x="${M + 34}" y="${y + 78}" font-family="${FONT_MONO}" font-size="34" fill="${accent}">${num}</text>
    <text x="${M + 96}" y="${y + 80}" font-family="'DejaVu Sans'" font-size="42" font-weight="700" fill="${P.paper}">${esc(title)}</text>
    <text x="${M + 96}" y="${y + 140}" font-family="'DejaVu Sans'" font-size="27" fill="${P.muted}">${esc(sub)}</text>
  </g>`;
}

function mascotLayer(t, mood, talk) {
  const appear = easeOutExpo(progress(t, 0.25, 1.2));
  const hook = t < B.b1.end;                       // kancada daha yakın plan
  const target = hook ? 1.34 : 1.12;
  const scale = lerp(1.0, target, clamp((t - 0.2) / 1.4));
  return mascot({
    t,
    x: (W - 200 * scale) / 2,
    y: 1310 - 312 * scale,
    scale,
    mood,
    talk,
    opacity: appear,
  });
}

/** Orta boşluğu dolduran dev, soluk numara/ikon. */
function watermark(t, text, start, opacity = 0.055) {
  const p = easeOutCubic(progress(t, start, start + 0.8));
  return `<text x="${W / 2}" y="560" opacity="${p * opacity}" text-anchor="middle"
    font-family="'DejaVu Sans'" font-size="300" font-weight="700" fill="#ffffff">${esc(text)}</text>`;
}

export function frame(t) {
  const b = (n) => B[`b${n}`];
  const wrap = (beat, edge = 0.35) =>
    Math.min(progress(t, beat.start - 0.15, beat.start + edge), 1 - progress(t, beat.end - edge, beat.end + 0.25));

  const inBeat = (n) => t >= b(n).start - 0.15 && t <= b(n).end + 0.3;

  let body = '';
  let mood = 'calm';
  let talk = 0;

  if (t < b(1).end + 0.3) {
    // 1) Kanca
    mood = 'alert';
    talk = 1;
    body += caption(
      t,
      [
        { text: 'DUR!' },
        { text: 'Kimliğinle şirket' },
        { text: 'kurulabilir.', color: P.warn },
        { text: 'Haberin olmaz.', color: P.muted },
      ],
      { start: b(1).start, size: 62, y: 180 },
    );
    body += watermark(t, '?!', b(1).start + 0.5, 0.05);
  }

  if (inBeat(2)) {
    mood = 'serious';
    talk = 1;
    body += caption(t, ['Üç şeyi', 'şimdi yap.'], { start: b(2).start, size: 64, y: 180 });
    body += watermark(t, '1', b(2).start + 0.4);
    body += stepCard(t, b(2).start + 1.0, '01', 'Ticaret Sicili', 'Sahibi / ortağı olduğum şirketler');
  }

  if (inBeat(3)) {
    mood = 'serious';
    talk = 1;
    body += caption(t, ['Üstüne kayıtlı', 'hatları gör.'], { start: b(3).start, size: 64, y: 180 });
    body += watermark(t, '2', b(3).start + 0.3);
    body += stepCard(t, b(3).start + 0.5, '02', 'Telefon hatları', 'Üzerine kayıtlı hatları listele', P.accent2);
  }

  if (inBeat(4)) {
    mood = 'serious';
    talk = 1;
    body += caption(t, ['MERSİS', 'kısıtlaması.'], { start: b(4).start, size: 64, y: 180 });
    body += watermark(t, '3', b(4).start + 0.3);
    body += stepCard(t, b(4).start + 0.6, '03', 'Kısıt koy', 'Ortak / yetkili olunmasına yönelik', P.accent3);
  }

  if (inBeat(5)) {
    mood = 'alert';
    talk = 1;
    body += caption(
      t,
      [
        { text: 'Kısıttan sonra' },
        { text: 'tek bir hata', color: P.warn },
        { text: 'her şeyi boşa' },
        { text: 'çıkarır.', color: P.warn },
      ],
      { start: b(5).start, size: 58, y: 170 },
    );
  }

  if (t >= b(6).start - 0.15) {
    mood = 'calm';
    talk = 1;
    body += caption(
      t,
      [
        { text: 'Yoruma' },
        { text: 'KONTROL yaz', color: ACCENT },
      ],
      { start: b(6).start, size: 62, y: 170 },
    );
    const p = easeOutCubic(progress(t, b(6).start + 1.4, b(6).start + 2.1));
    body += `<g opacity="${p}">
      ${rect(M, 380, W - M * 2, 132, '#141c33', 24, 'stroke="#2a3557" stroke-width="2"')}
      <text x="${M + 32}" y="430" font-family="'DejaVu Sans'" font-size="28" fill="${P.muted}">Tam kontrol listesi + hazır dilekçe</text>
      <text x="${M + 32}" y="478" font-family="'DejaVu Sans'" font-size="32" font-weight="700" fill="${P.paper}">Kaydet · Paylaş · Takip et</text>
    </g>`;
    const q = easeOutCubic(progress(t, b(6).start + 2.6, b(6).start + 3.2));
    body += `<text x="${M}" y="586" opacity="${q}" font-family="'DejaVu Sans'" font-size="26" fill="${P.muted}">Bilgi amaçlıdır, hukuki danışmanlık değildir.</text>`;
  }

  // Geçişlerde kartlar üst üste binmesin diye beat dışındakiler soluklaşır.
  body = `<g>${body}</g>`;
  return svgDoc(W, H, defs, background(t) + chrome(t) + body + mascotLayer(t, mood, talk));
}
