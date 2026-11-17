// Düz vektör hukukçu maskotu. 200x270 yerel koordinatta çizilir, dışarıdan
// translate/scale ile yerleştirilir. Konuşma, göz kırpma ve nefes animasyonu
// tamamen `t`'ye bağlı (deterministik).
import { palette as P } from './svg.mjs';

function blink(t) {
  // ~3.1 sn'de bir, 110 ms'lik göz kırpma
  const phase = (t + 0.4) % 3.1;
  return phase < 0.11 ? 0.12 : 1;
}

function mouthOpen(t, talk) {
  if (!talk) return 2.2;
  const v = Math.abs(Math.sin(t * 9.5)) * Math.abs(Math.sin(t * 3.1));
  return 2 + v * 7 * talk;
}

/**
 * @param {object} o
 * @param {number} o.t        zaman (sn)
 * @param {number} o.x        sol üst x
 * @param {number} o.y        sol üst y
 * @param {number} o.scale    ölçek
 * @param {string} o.mood     'alert' | 'calm' | 'serious'
 * @param {number} o.talk     0..1 konuşma yoğunluğu
 * @param {number} o.opacity
 */
export function mascot({ t, x, y, scale = 1, mood = 'calm', talk = 0, opacity = 1 }) {
  const bob = Math.sin(t * 2.1) * 3;
  const tilt = Math.sin(t * 1.3) * 1.6;
  const eyeH = blink(t) * 7;
  const brow = mood === 'alert' ? -9 : mood === 'serious' ? -3 : 0;
  const accent = mood === 'alert' ? P.warn : P.accent;
  const m = mouthOpen(t, talk);

  return `<g transform="translate(${x} ${y}) scale(${scale})" opacity="${opacity}">
    <g transform="translate(0 ${bob}) rotate(${tilt} 100 150)">
      <!-- gövde / ceket -->
      <path d="M100 168 C58 168 34 196 30 232 L30 312 L170 312 L170 232 C166 196 142 168 100 168 Z" fill="#1b2542"/>
      <path d="M100 168 C84 168 70 176 62 188 L100 214 L138 188 C130 176 116 168 100 168 Z" fill="#f6f7fb"/>
      <!-- yaka -->
      <path d="M100 214 L74 182 L58 196 L86 236 Z" fill="#232f52"/>
      <path d="M100 214 L126 182 L142 196 L114 236 Z" fill="#232f52"/>
      <!-- kravat -->
      <path d="M100 206 L110 220 L104 228 L100 262 L96 228 L90 220 Z" fill="${P.accent3}"/>
      <!-- boyun -->
      <rect x="88" y="146" width="24" height="26" rx="10" fill="#e8b48f"/>
      <!-- kulaklar -->
      <circle cx="46" cy="92" r="9" fill="#e8b48f"/>
      <circle cx="154" cy="92" r="9" fill="#e8b48f"/>
      <!-- yüz -->
      <rect x="48" y="34" width="104" height="122" rx="48" fill="#f0c19c"/>
      <!-- saç -->
      <path d="M48 88 C48 40 76 20 100 20 C124 20 152 40 152 88 C144 70 128 62 100 62 C72 62 56 70 48 88 Z" fill="#20283d"/>
      <!-- kaşlar -->
      <rect x="64" y="${64 + brow}" width="26" height="6" rx="3" fill="#20283d" transform="rotate(-4 77 ${67 + brow})"/>
      <rect x="110" y="${64 + brow}" width="26" height="6" rx="3" fill="#20283d" transform="rotate(4 123 ${67 + brow})"/>
      <!-- gözler -->
      <rect x="68" y="${80 - eyeH / 2}" width="18" height="${eyeH}" rx="${eyeH / 2}" fill="#20283d"/>
      <rect x="114" y="${80 - eyeH / 2}" width="18" height="${eyeH}" rx="${eyeH / 2}" fill="#20283d"/>
      <!-- gözlük -->
      <rect x="60" y="68" width="34" height="26" rx="9" fill="none" stroke="#2f3c63" stroke-width="3.5"/>
      <rect x="106" y="68" width="34" height="26" rx="9" fill="none" stroke="#2f3c63" stroke-width="3.5"/>
      <line x1="94" y1="78" x2="106" y2="78" stroke="#2f3c63" stroke-width="3.5"/>
      <!-- ağız -->
      <path d="M84 116 Q100 ${116 + m} 116 116" stroke="${P.ink}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <!-- yaka rozeti: terazi -->
      <g transform="translate(140 226) scale(0.85)">
        <circle r="17" fill="none" stroke="${accent}" stroke-width="2.4"/>
        <line x1="0" y1="-8" x2="0" y2="9" stroke="${accent}" stroke-width="2.2"/>
        <line x1="-9" y1="-5" x2="9" y2="-5" stroke="${accent}" stroke-width="2.2"/>
        <path d="M-13 -5 L-5 -5 L-9 3 Z" fill="none" stroke="${accent}" stroke-width="1.8"/>
        <path d="M5 -5 L13 -5 L9 3 Z" fill="none" stroke="${accent}" stroke-width="1.8"/>
      </g>
    </g>
  </g>`;
}
