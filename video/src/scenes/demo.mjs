import {
  progress,
  easeOutCubic,
  easeOutExpo,
  spring,
  clamp,
  lerp,
} from '../lib/motion.mjs';
import {
  palette as P,
  textBlock,
  rect,
  circle,
  line,
  svgDoc,
  esc,
  FONT_MONO,
} from '../lib/svg.mjs';

export const meta = {
  fps: 30,
  width: 1280,
  height: 720,
  duration: 14,
  title: 'pipeline-demo',
};

/** Dark backdrop with a slow drifting glow and faint grid. */
function background(t) {
  const drift = Math.sin(t * 0.45) * 90;
  const drift2 = Math.cos(t * 0.32) * 70;
  const grid = [];
  for (let x = 0; x <= meta.width; x += 80) grid.push(line(x, 0, x, meta.height, '#ffffff', 1, 'opacity="0.035"'));
  for (let y = 0; y <= meta.height; y += 80) grid.push(line(0, y, meta.width, y, '#ffffff', 1, 'opacity="0.035"'));
  return `
    ${grid.join('')}
    <circle cx="${240 + drift}" cy="${180 + drift2}" r="340" fill="url(#glowA)"/>
    <circle cx="${1060 - drift}" cy="${600 + drift2}" r="300" fill="url(#glowB)"/>`;
}

const defs = `
  <radialGradient id="glowA"><stop offset="0%" stop-color="${P.accent}" stop-opacity="0.20"/><stop offset="100%" stop-color="${P.accent}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowB"><stop offset="0%" stop-color="${P.accent2}" stop-opacity="0.22"/><stop offset="100%" stop-color="${P.accent2}" stop-opacity="0"/></radialGradient>
  <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="${P.accent}"/><stop offset="100%" stop-color="${P.accent2}"/></linearGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="${P.accent}"/><stop offset="100%" stop-color="${P.accent3}"/></linearGradient>`;

/** 0 - 4s : kinetic title */
function titleBlock(t) {
  const a = easeOutCubic(progress(t, 0.15, 1.1));
  if (a <= 0) return '';
  const out = progress(t, 3.3, 4.0);
  const y = lerp(46, 0, easeOutExpo(progress(t, 0.15, 1.3))) - out * 30;
  const fade = 1 - out;
  const words = ['Kodla', 'video', 'üretimi'];
  const spans = words
    .map((w, i) => {
      const p = easeOutCubic(progress(t, 0.2 + i * 0.12, 0.9 + i * 0.12));
      return `<tspan x="120" dy="${i === 0 ? 0 : 80}" opacity="${p}" fill="${P.paper}">${esc(w)}</tspan>`;
    })
    .join('');
  const underline = easeOutExpo(progress(t, 0.9, 1.7)) * 300;
  return `
    <g opacity="${fade}" transform="translate(0 ${y + 72})">
      <text y="150" font-family="'DejaVu Sans'" font-size="70" font-weight="700" letter-spacing="-1">${spans}</text>
      ${rect(120, 352, underline, 6, 'url(#sweep)', 3)}
      <text x="120" y="406" font-family="'DejaVu Sans'" font-size="26" fill="${P.muted}" opacity="${easeOutCubic(progress(t, 1.1, 1.9))}">
        Kare kare çizim, tek dosya film · lisans ücreti yok
      </text>
    </g>`;
}

/** 3.6 - 8.4s : pipeline diagram */
function pipelineBlock(t) {
  const appear = progress(t, 3.5, 3.9);
  if (appear <= 0) return '';
  const out = progress(t, 8.0, 8.6);
  const fade = 1 - out;
  const nodes = ['Sahne kodu', 'Kareler', 'FFmpeg', 'MP4'];
  const boxW = 220;
  const boxH = 96;
  const gap = 60;
  const totalW = nodes.length * boxW + (nodes.length - 1) * gap;
  const startX = (meta.width - totalW) / 2;
  const y = 300;
  const parts = [];
  const dot = easeInOutCubicLite(progress(t, 4.4, 7.6));

  nodes.forEach((label, i) => {
    const p = spring(clamp((t - 3.6 - i * 0.28) / 0.9));
    const x = startX + i * (boxW + gap);
    const active = dot * 3; // 0..3 position along the chain
    const near = Math.max(0, 1 - Math.abs(active - i)) * 0.9;
    parts.push(`
      <g opacity="${clamp(p) * fade}" transform="translate(0 ${(1 - clamp(p)) * 24})">
        ${rect(x, y, boxW, boxH, near > 0.05 ? '#1d2a4d' : P.inkSoft, 18, `stroke="${near > 0.05 ? P.accent : '#2a3557'}" stroke-width="${near > 0.05 ? 2.5 : 1.5}"`)}
        <text x="${x + boxW / 2}" y="${y + boxH / 2 + 9}" font-family="'DejaVu Sans'" font-size="24" font-weight="700" fill="${near > 0.05 ? P.paper : '#c7d0e6'}" text-anchor="middle">${esc(label)}</text>
      </g>`);
    if (i < nodes.length - 1) {
      const ax = x + boxW + 14;
      const grow = easeOutCubic(progress(t, 3.9 + i * 0.28, 4.3 + i * 0.28));
      parts.push(line(ax, y + boxH / 2, ax + (gap - 28) * grow, y + boxH / 2, '#3b4870', 2));
      if (grow > 0.9) {
        parts.push(`<path d="M ${ax + gap - 40} ${y + boxH / 2 - 6} l 10 6 l -10 6 z" fill="#3b4870"/>`);
      }
    }
  });

  const dotX = startX + dot * (totalW - boxW) + boxW / 2;
  parts.push(circle(dotX, y - 18, 7, P.accent, `opacity="${fade * clamp(progress(t, 4.4, 4.8))}"`));
  parts.push(
    `<text x="${meta.width / 2}" y="${y + 190}" font-family="'DejaVu Sans'" font-size="25" fill="${P.muted}" text-anchor="middle" opacity="${fade * easeOutCubic(progress(t, 5.0, 5.8))}">Tarayıcı yok · her kare aynı, iki çekirdekte bile hızlı</text>`,
  );
  return `<g opacity="${fade}">${parts.join('')}</g>`;
}

/** local helper so we do not import twice */
function easeInOutCubicLite(p) {
  return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
}

/** 8.2 - 11.4s : stat cards with count-up */
function statsBlock(t) {
  const appear = progress(t, 8.2, 8.6);
  if (appear <= 0) return '';
  const out = progress(t, 11.0, 11.6);
  const fade = 1 - out;
  const stats = [
    { value: Math.round(meta.duration * meta.fps * easeOutCubic(progress(t, 8.4, 9.6))), suffix: '', label: 'kare' },
    { value: Math.round(30 * easeOutCubic(progress(t, 8.5, 9.7))), suffix: '', label: 'fps' },
    { value: 0, suffix: '', label: 'TL lisans' },
  ];
  const cardW = 300;
  const cardH = 170;
  const gap = 40;
  const totalW = stats.length * cardW + (stats.length - 1) * gap;
  const startX = (meta.width - totalW) / 2;
  return stats
    .map((s, i) => {
      const p = spring(clamp((t - 8.25 - i * 0.15) / 0.9));
      const x = startX + i * (cardW + gap);
      const y = 300 + (1 - clamp(p)) * 26;
      return `<g opacity="${clamp(p) * fade}">
        ${rect(x, y, cardW, cardH, P.inkSoft, 20, 'stroke="#2a3557" stroke-width="1.5"')}
        <text x="${x + 32}" y="${y + 100}" font-family="'DejaVu Sans'" font-size="64" font-weight="700" fill="${[P.accent, P.accent2, P.accent3][i]}">${s.value}${s.suffix}</text>
        <text x="${x + 32}" y="${y + 138}" font-family="${FONT_MONO}" font-size="20" fill="${P.muted}">${esc(s.label)}</text>
      </g>`;
    })
    .join('');
}

/** 11.2 - 14s : outro */
function outroBlock(t) {
  const p = easeOutCubic(progress(t, 11.3, 12.2));
  if (p <= 0) return '';
  const y = lerp(30, 0, easeOutExpo(progress(t, 11.3, 12.4)));
  return `<g opacity="${p}" transform="translate(0 ${y + 72})">
    <text x="${meta.width / 2}" y="330" font-family="'DejaVu Sans'" font-size="54" font-weight="700" fill="${P.paper}" text-anchor="middle">Hat hazır.</text>
    <text x="${meta.width / 2}" y="390" font-family="'DejaVu Sans'" font-size="24" fill="${P.muted}" text-anchor="middle">video/ klasörü · npm run render -- --scene demo</text>
    ${rect(meta.width / 2 - 60 * easeOutExpo(progress(t, 11.8, 12.8)), 424, 120 * easeOutExpo(progress(t, 11.8, 12.8)), 4, 'url(#sweep)', 2)}
  </g>`;
}

export function frame(t, ctx) {
  const body = [
    background(t),
    titleBlock(t),
    pipelineBlock(t),
    statsBlock(t),
    outroBlock(t),
  ].join('');
  return svgDoc(meta.width, meta.height, defs, body);
}
