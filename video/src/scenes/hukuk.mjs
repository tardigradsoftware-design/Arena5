import { progress, easeOutCubic, easeOutExpo, spring, clamp, lerp } from '../lib/motion.mjs';
import { palette as P, rect, line, svgDoc, esc, FONT_MONO } from '../lib/svg.mjs';

// 9:16 dikey kısa video — genç hukukçu karakteri, kira sözleşmesi üç maddesi.
export const meta = {
  fps: 30,
  width: 1080,
  height: 1920,
  duration: 16,
  title: 'hukuk-kirak',
};

const defs = `
  <radialGradient id="glow" cx="50%" cy="28%" r="62%">
    <stop offset="0%" stop-color="${P.accent2}" stop-opacity="0.20"/>
    <stop offset="100%" stop-color="${P.accent2}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="${P.accent}"/><stop offset="100%" stop-color="${P.accent3}"/>
  </linearGradient>`;

function background(t) {
  const g = [];
  for (let y = 0; y <= meta.height; y += 96) g.push(line(0, y, meta.width, y, '#ffffff', 1, 'opacity="0.03"'));
  for (let x = 0; x <= meta.width; x += 96) g.push(line(x, 0, x, meta.height, '#ffffff', 1, 'opacity="0.03"'));
  return `${g.join('')}<rect width="${meta.width}" height="${meta.height}" fill="url(#glow)"/>`;
}

function header(t) {
  const p = easeOutCubic(progress(t, 0.2, 1.2));
  const out = progress(t, 3.6, 4.2);
  return `<g opacity="${p * (1 - out)}" transform="translate(0 ${(1 - p) * 26})">
    <text x="96" y="300" font-family="'DejaVu Sans'" font-size="44" fill="${P.accent}" letter-spacing="6">HUKUK · 60 SANİYE</text>
    <text x="96" y="420" font-family="'DejaVu Sans'" font-size="92" font-weight="700" fill="${P.paper}">Kira</text>
    <text x="96" y="522" font-family="'DejaVu Sans'" font-size="92" font-weight="700" fill="${P.paper}">sözleşmesi</text>
    ${rect(96, 570, 300 * easeOutExpo(progress(t, 0.9, 1.8)), 8, 'url(#bar)', 4)}
    <text x="96" y="660" font-family="'DejaVu Sans'" font-size="40" fill="${P.muted}">İmzadan önce üç madde</text>
  </g>`;
}

const items = [
  { n: '01', title: 'Kira artışı', sub: 'Yıllık artış oranı yazılı mı?' },
  { n: '02', title: 'Depozito', sub: 'Ne kadar, ne zaman geri?' },
  { n: '03', title: 'Tahliye şartı', sub: 'Hangi durumda çıkabilirsin?' },
];

function cards(t) {
  return items
    .map((it, i) => {
      const start = 4.4 + i * 2.1;
      const p = spring(clamp((t - start) / 0.9));
      const out = progress(t, 12.2, 12.8);
      const y = 760 + i * 300 + (1 - clamp(p)) * 40;
      return `<g opacity="${clamp(p) * (1 - out)}">
        ${rect(96, y, 888, 240, '#141c33', 28, 'stroke="#2a3557" stroke-width="2"')}
        ${rect(96, y, 10, 240, 'url(#bar)', 5)}
        <text x="146" y="${y + 92}" font-family="${FONT_MONO}" font-size="46" fill="${P.accent}">${it.n}</text>
        <text x="230" y="${y + 96}" font-family="'DejaVu Sans'" font-size="62" font-weight="700" fill="${P.paper}">${esc(it.title)}</text>
        <text x="146" y="${y + 176}" font-family="'DejaVu Sans'" font-size="36" fill="${P.muted}">${esc(it.sub)}</text>
      </g>`;
    })
    .join('');
}

function outro(t) {
  const p = easeOutCubic(progress(t, 12.6, 13.6));
  if (p <= 0) return '';
  const y = lerp(30, 0, easeOutExpo(progress(t, 12.6, 13.8)));
  return `<g opacity="${p}" transform="translate(0 ${y})">
    <text x="${meta.width / 2}" y="900" font-family="'DejaVu Sans'" font-size="76" font-weight="700" fill="${P.paper}" text-anchor="middle">İmzadan önce oku,</text>
    <text x="${meta.width / 2}" y="992" font-family="'DejaVu Sans'" font-size="76" font-weight="700" fill="${P.accent}" text-anchor="middle">sonra güven.</text>
    ${rect(meta.width / 2 - 120 * easeOutExpo(progress(t, 13.2, 14.2)), 1040, 240 * easeOutExpo(progress(t, 13.2, 14.2)), 6, 'url(#bar)', 3)}
    <text x="${meta.width / 2}" y="1140" font-family="'DejaVu Sans'" font-size="34" fill="${P.muted}" text-anchor="middle">Bilgi amaçlıdır, hukuki danışmanlık değildir</text>
  </g>`;
}

export function frame(t) {
  return svgDoc(meta.width, meta.height, defs, background(t) + header(t) + cards(t) + outro(t));
}
