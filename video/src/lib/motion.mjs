// Small math helpers used by scenes. Everything is deterministic: a frame
// depends only on `t`, never on wall-clock time, so parallel shards match.

export const clamp = (v, min = 0, max = 1) => Math.min(max, Math.max(min, v));

export const lerp = (a, b, p) => a + (b - a) * p;

/** Map t from [start, end] to 0..1, clamped. */
export const progress = (t, start, end) => clamp((t - start) / (end - start));

export const easeOutCubic = (p) => 1 - Math.pow(1 - p, 3);
export const easeInCubic = (p) => p * p * p;
export const easeInOutCubic = (p) =>
  p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
export const easeOutExpo = (p) => (p === 1 ? 1 : 1 - Math.pow(2, -10 * p));
export const easeOutBack = (p, s = 1.70158) =>
  1 + (s + 1) * Math.pow(p - 1, 3) + s * Math.pow(p - 1, 2);

/** Damped spring, 0 -> 1 with overshoot. */
export const spring = (t) =>
  t <= 0 ? 0 : 1 - Math.exp(-6 * t) * Math.cos(8 * t);

/** Fade in then out inside [a, b]. */
export const fadeWindow = (t, a, b, edge = 0.4) =>
  Math.min(progress(t, a, a + edge), 1 - progress(t, b - edge, b));
