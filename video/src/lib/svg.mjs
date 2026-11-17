// Tiny SVG helpers so scenes stay readable.

export const palette = {
  ink: '#0b1020',
  inkSoft: '#141c33',
  paper: '#f6f7fb',
  muted: '#8f9bb8',
  accent: '#5eead4',
  accent2: '#818cf8',
  accent3: '#f472b6',
  warn: '#fbbf24',
};

export const FONT = "'DejaVu Sans', 'Noto Sans', sans-serif";
export const FONT_MONO = "'DejaVu Sans Mono', monospace";

/** Escape text for use inside SVG markup. */
export const esc = (s) =>
  String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

/**
 * Multiline text block.
 * lines: string[]; opts: { size, weight, fill, lineHeight, anchor }
 */
export function textBlock(lines, x, y, opts = {}) {
  const {
    size = 64,
    weight = 700,
    fill = palette.paper,
    lineHeight = 1.15,
    anchor = 'start',
    family = FONT,
    opacity = 1,
    letterSpacing = 0,
  } = opts;
  return `<text x="${x}" y="${y}" font-family="${family}" font-size="${size}"
    font-weight="${weight}" fill="${fill}" text-anchor="${anchor}"
    opacity="${opacity}" letter-spacing="${letterSpacing}">${lines
    .map(
      (line, i) =>
        `<tspan x="${x}" dy="${i === 0 ? 0 : size * lineHeight * 1}">${esc(
          line,
        )}</tspan>`,
    )
    .join('')}</text>`;
}

export function rect(x, y, w, h, fill, r = 0, extra = '') {
  return `<rect x="${x}" y="${y}" width="${Math.max(0, w)}" height="${Math.max(
    0,
    h,
  )}" rx="${r}" fill="${fill}" ${extra}/>`;
}

export function circle(cx, cy, r, fill, extra = '') {
  return `<circle cx="${cx}" cy="${cy}" r="${Math.max(0, r)}" fill="${fill}" ${extra}/>`;
}

export function line(x1, y1, x2, y2, stroke, width = 2, extra = '') {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${width}" ${extra}/>`;
}

export function svgDoc(width, height, defs, body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"><defs>${defs}</defs>${body}</svg>`;
}
