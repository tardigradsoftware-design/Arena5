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
  title: 'hukuk4-shorts',
};

const W = meta.width;
const H = meta.height;
const M = 40;
const AMBER = P.warn;
const MINT = P.accent;

/* ------------------------------ metin kalıbı ----------------------------- */

const BEATS = {
  1: {
    mood: 'alert',
    headline: ['DUR!'],
    chunks: ['DUR!', 'Kimliğinle adına', 'şirket kurulabilir', 've senin hiç', 'haberin olmaz.'],
    accentWords: ['DUR!', 'şirket', 'haberin'],
  },
  2: {
    mood: 'serious',
    badge: '01',
    headline: ['ÜÇ ADIM'],
    card: { title: 'Ticaret Sicili', sub: 'Sahibi / ortağı olduğum şirketler', icon: 'building' },
    chunks: ['Üç şeyi şimdi yap.', "Bir: Ticaret", "Sicili'ndeki", 'sahibi veya ortağı', 'olduğum şirketler', 'sorgusunu aç.'],
    accentWords: ['Bir:', 'Ticaret'],
  },
  3: {
    mood: 'serious',
    badge: '02',
    headline: ['ÜSTÜNE KAYITLI HATLAR'],
    card: { title: 'Telefon hatları', sub: 'Üzerine kayıtlı hatları listele', icon: 'phone' },
    chunks: ['İki: Üzerine kayıtlı', 'telefon hatlarını', 'listele.'],
    accentWords: ['İki:', 'telefon'],
  },
  4: {
    mood: 'serious',
    badge: '03',
    headline: ['MERSİS KISITI'],
    card: { title: 'Kısıt koy', sub: 'Ortak / yetkili olunmasına yönelik', icon: 'lock' },
    chunks: ['Üç: Ortak veya yetkili', 'olunmasına yönelik', 'kısıtlama işlemlerinden', 'kısıtı aç.'],
    accentWords: ['Üç:', 'kısıtı'],
  },
  5: {
    mood: 'alert',
    headline: ['TEK HATA'],
    chunks: ['Ama kısıttan sonra', 'yapılan tek bir hata,', 'her şeyi boşa', 'çıkarır.', 'Birazdan anlatıyorum.'],
    accentWords: ['tek', 'hata', 'boşa'],
  },
  6: {
    mood: 'calm',
    headline: ['KONTROL'],
    cta: true,
    chunks: ['Tam kontrol listesi', 've hazır dilekçe için', 'yoruma KONTROL yaz.', 'Kaydet,', 'bir tanıdığına gönder,', "HQK TV'yi takip et."],
    accentWords: ['KONTROL', 'Kaydet'],
  },
};

/* Kare bazlı yardımcılar */

const chars = (s) => s.replace(/\s/g, '').length;

/** Beat süresini parçalara, karakter sayısına göre böler. */
function chunkTimes(beat, chunks) {
  const total = chunks.reduce((a, c) => a + chars(c), 0);
  let t = beat.start;
  return chunks.map((c) => {
    const d = (chars(c) / total) * (beat.end - beat.start);
    const range = [t, t + d];
    t += d;
    return range;
  });
}

function activeBeat(t) {
  for (const n of [1, 2, 3, 4, 5, 6]) {
    const b = B[`b${n}`];
    if (t >= b.start - 0.2 && t <= b.end + 0.35) return n;
  }
  return null;
}

/* --------------------------------- görsel -------------------------------- */

const defs = `
  <radialGradient id="vign" cx="50%" cy="30%" r="72%">
    <stop offset="0%" stop-color="#1b2a52" stop-opacity="1"/>
    <stop offset="100%" stop-color="${P.ink}" stop-opacity="1"/>
  </radialGradient>
  <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="${MINT}"/><stop offset="100%" stop-color="${P.accent3}"/>
  </linearGradient>`;

function background(t) {
  const g = [];
  for (let y = 0; y <= H; y += 72) g.push(line(0, y, W, y, '#ffffff', 1, 'opacity="0.022"'));
  for (let x = 0; x <= W; x += 72) g.push(line(x, 0, x, H, '#ffffff', 1, 'opacity="0.022"'));
  return `${rect(0, 0, W, H, 'url(#vign)')}${g.join('')}
    <circle cx="${W / 2 + Math.sin(t * 0.6) * 30}" cy="250" r="300" fill="${MINT}" opacity="0.045"/>`;
}

function chrome(t) {
  const p = clamp(t / meta.duration);
  return `${rect(0, 0, W, 5, '#1b2542')}${rect(0, 0, W * p, 5, 'url(#bar)')}
    ${rect(M, 40, 108, 36, '#141c33', 18, 'stroke="#2a3557" stroke-width="1.5"')}
    <text x="${M + 54}" y="${64}" font-family="${FONT_MONO}" font-size="17" fill="${MINT}" text-anchor="middle">HQK TV</text>`;
}

function icon(kind, cx, cy) {
  const s = 'stroke="#0b1020" stroke-width="2.6" stroke-linejoin="round"';
  const body = {
    building: `${rect(cx - 16, cy - 18, 32, 34, 'none', 4, s)}
      ${line(cx - 8, cy - 8, cx - 2, cy - 8, '#0b1020', 2.6)}
      ${line(cx + 2, cy - 8, cx + 8, cy - 8, '#0b1020', 2.6)}
      ${line(cx - 8, cy + 2, cx - 2, cy + 2, '#0b1020', 2.6)}
      ${line(cx + 2, cy + 2, cx + 8, cy + 2, '#0b1020', 2.6)}`,
    phone: `${rect(cx - 11, cy - 18, 22, 36, 'none', 5, s)}
      ${line(cx - 5, cy - 12, cx + 5, cy - 12, '#0b1020', 2.2)}
      <circle cx="${cx}" cy="${cy + 11}" r="2.6" fill="#0b1020"/>`,
    lock: `${rect(cx - 13, cy - 4, 26, 22, 'none', 4, s)}
      <path d="M ${cx - 7} ${cy - 4} v -7 a 7 7 0 0 1 14 0 v 7" fill="none" stroke="#0b1020" stroke-width="2.6"/>`,
  }[kind];
  return `<circle cx="${cx}" cy="${cy}" r="30" fill="${MINT}" opacity="0.18"/>
    <circle cx="${cx}" cy="${cy}" r="30" fill="none" stroke="${MINT}" stroke-width="1.6" opacity="0.5"/>${body}`;
}

function headlineSpeak(t, beat, cfg) {
  const p = easeOutCubic(progress(t, beat.start - 0.1, beat.start + 0.45));
  if (p <= 0) return '';
  return cfg.headline
    .map(
      (ln, i) => `<text x="${M}" y="${190 + i * 64}" opacity="${p}"
        transform="translate(0 ${(1 - p) * 18})"
        font-family="'DejaVu Sans'" font-size="60" font-weight="800"
        fill="${i === 0 ? AMBER : P.paper}" letter-spacing="-1">${esc(ln)}</text>`,
    )
    .join('');
}

function stepCard(t, beat, card) {
  const p = spring(clamp((t - beat.start - 0.5) / 0.7));
  if (p <= 0.01) return '';
  const y = 360 + (1 - clamp(p)) * 30;
  return `<g opacity="${clamp(p)}">
    ${rect(M, y, W - M * 2, 190, '#141c33', 24, 'stroke="#2a3557" stroke-width="2"')}
    ${rect(M, y, 7, 190, MINT, 4)}
    <text x="${M + 96}" y="${y + 82}" font-family="'DejaVu Sans'" font-size="40" font-weight="700" fill="${P.paper}">${esc(card.title)}</text>
    <text x="${M + 96}" y="${y + 136}" font-family="'DejaVu Sans'" font-size="25" fill="${P.muted}">${esc(card.sub)}</text>
    ${icon(card.icon, M + 52, y + 100)}
  </g>`;
}

/** Karaoke altyazı: geçmiş parça sönük, aktif parça büyük + kelime vurgusu. */
function karaoke(t, beat, cfg, yTop = 742) {
  const times = chunkTimes(beat, cfg.chunks);
  const idx = times.findIndex(([a, b]) => t >= a - 0.05 && t <= b + 0.1);
  if (idx < 0) return '';

  const [a, b] = times[idx];
  const words = cfg.chunks[idx].split(' ');
  const per = (b - a) / Math.max(1, words.length);
  const activeWord = Math.min(words.length - 1, Math.floor((t - a) / per));

  const prev = idx > 0 ? cfg.chunks[idx - 1] : '';
  const scale = 1 + 0.06 * (1 - easeOutExpo(progress(t, a, a + 0.22)));
  const lines = [];
  const size = 34;
  const maxChars = 22;
  let line = '';
  const outLines = [];
  words.forEach((w) => {
    if ((line + ' ' + w).trim().length > maxChars) {
      outLines.push(line.trim());
      line = w;
    } else {
      line = (line + ' ' + w).trim();
    }
  });
  if (line) outLines.push(line.trim());

  let gi = 0;
  const fill = outLines
    .map((ln, li) => {
      const tspans = ln.split(' ').map((w) => {
        const isActive = gi === activeWord;
        const isAccent = cfg.accentWords?.some((aw) => w.replace(/[.,!:]/g, '').toLowerCase() === aw.replace(/[.,!:]/g, '').toLowerCase());
        gi += 1;
        const color = isActive ? (isAccent ? AMBER : MINT) : P.paper;
        return `<tspan fill="${color}" opacity="${isActive ? 1 : 0.82}">${esc(w)} </tspan>`;
      });
      return `<text x="${W / 2}" y="${yTop + li * 46}" text-anchor="middle" font-family="'DejaVu Sans'"
        font-size="${size + 2}" font-weight="700" stroke="${P.ink}" stroke-width="7" stroke-linejoin="round"
        paint-order="stroke" xml:space="preserve">${tspans.join('')}</text>`;
    })
    .join('');

  const prevLine = prev
    ? `<text x="${W / 2}" y="${yTop - 52}" text-anchor="middle" font-family="'DejaVu Sans'" font-size="24"
        fill="${P.muted}" stroke="${P.ink}" stroke-width="6" stroke-linejoin="round" paint-order="stroke" xml:space="preserve">${esc(prev)}</text>`
    : '';

  return `<g transform="translate(${W / 2} 0) scale(${scale}) translate(${-W / 2} 0)">${prevLine}${fill}</g>`;
}


/** Kart olmayan beat'lerde orta boşluğu dolduran illüstrasyon. */
function visualPanel(t, beat, kind) {
  const p = spring(clamp((t - beat.start - 0.25) / 0.7));
  if (p <= 0.01) return '';
  const cy = 806;
  const cx = W / 2;
  const pop = 1 + 0.04 * (1 - clamp(p));
  let art = '';

  if (kind === 'id') {
    // kimlik kartı
    art = `${rect(cx - 120, cy - 78, 240, 150, '#182143', 16, 'stroke="#3b4870" stroke-width="2"')}
      ${rect(cx - 100, cy - 56, 62, 78, '#243059', 8)}
      <circle cx="${cx - 69}" cy="${cy - 32}" r="15" fill="#8f9bb8"/>
      <path d="M ${cx - 88} ${cy + 8} q 19 -26 38 0" fill="#8f9bb8" opacity="0.9"/>
      ${rect(cx - 24, cy - 50, 118, 12, '#3b4870', 6)}
      ${rect(cx - 24, cy - 26, 92, 10, '#2f3c63', 5)}
      ${rect(cx - 24, cy - 6, 104, 10, '#2f3c63', 5)}
      <text x="${cx + 84}" y="${cy + 58}" font-family="${FONT_MONO}" font-size="16" fill="${AMBER}" text-anchor="end">KİMLİK</text>`;
  } else if (kind === 'warn') {
    art = `<g transform="translate(${cx} ${cy}) scale(${pop})">
      <path d="M0 -62 L64 52 L-64 52 Z" fill="none" stroke="${AMBER}" stroke-width="6" stroke-linejoin="round"/>
      <rect x="-6" y="-24" width="12" height="42" rx="6" fill="${AMBER}"/>
      <circle cx="0" cy="34" r="7" fill="${AMBER}"/>
    </g>`;
  } else if (kind === 'bubble') {
    art = `<g transform="translate(${cx} ${cy}) scale(${pop})">
      ${rect(-118, -66, 236, 118, '#182143', 26, 'stroke="#3b4870" stroke-width="2"')}
      <path d="M -34 52 L -34 86 L 2 52 Z" fill="#182143" stroke="#3b4870" stroke-width="2"/>
      <text x="0" y="4" text-anchor="middle" font-family="'DejaVu Sans'" font-size="34" font-weight="700" fill="${AMBER}">KONTROL</text>
      <text x="0" y="38" text-anchor="middle" font-family="'DejaVu Sans'" font-size="15" fill="${P.muted}">yorum bırak</text>
    </g>`;
  }
  return `<g opacity="${clamp(p)}">${art}</g>`;
}

function ctaBox(t, beat) {
  const p = easeOutCubic(progress(t, beat.start + 3.2, beat.start + 3.8));
  if (p <= 0) return '';
  return `<g opacity="${p}">
    ${rect(M, 300, W - M * 2, 150, '#141c33', 22, 'stroke="#2a3557" stroke-width="2"')}
    <text x="${M + 28}" y="352" font-family="'DejaVu Sans'" font-size="26" fill="${P.muted}">Tam kontrol listesi + hazır dilekçe</text>
    <text x="${M + 28}" y="402" font-family="'DejaVu Sans'" font-size="30" font-weight="700" fill="${P.paper}">Kaydet · Paylaş · Takip et</text>
  </g>`;
}

function mascotLayer(t, mood, talk, beatNum) {
  const appear = easeOutExpo(progress(t, 0.2, 1.1));
  const punch = beatNum ? 0.05 * spring(clamp(progress(t, B[`b${beatNum}`].start, B[`b${beatNum}`].start + 0.5))) : 0;
  const base = beatNum === 1 ? 1.16 : 1.02;
  const scale = base + punch;
  return mascot({
    t,
    x: (W - 200 * scale) / 2,
    y: 1305 - 312 * scale,
    scale,
    mood,
    talk,
    opacity: appear,
  });
}

export function frame(t) {
  const n = activeBeat(t);
  const cfg = n ? BEATS[n] : null;
  const beat = n ? B[`b${n}`] : null;

  let body = '';
  if (cfg) {
    body += headlineSpeak(t, beat, cfg);
    if (cfg.card) body += stepCard(t, beat, cfg.card);
    if (n === 1) body += visualPanel(t, beat, 'id');
    if (n === 5) body += visualPanel(t, beat, 'warn');
    if (n === 6) body += visualPanel(t, beat, 'bubble');
    if (cfg.cta) body += ctaBox(t, beat);
    body += karaoke(t, beat, cfg, cfg.card || cfg.cta ? 742 : 640);
  }

  // uyarı beat'inde hafif sarsıntı
  const shake = n === 5 ? Math.sin(t * 42) * 1.6 * (1 - progress(t, beat.start, beat.start + 1.4)) : 0;

  return svgDoc(W, H, defs, background(t) + chrome(t) +
    `<g transform="translate(${shake} 0)">${body}</g>` +
    mascotLayer(t, cfg?.mood || 'calm', cfg ? 1 : 0.2, n));
}
