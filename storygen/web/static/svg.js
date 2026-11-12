// SVG drawings: the character relationship graph and the story map (branch tree with visited nodes).
import { esc } from './core.js';
import { branchOf } from './story_engine.js';

const fmt = v => v.toFixed(2);
// Relationship strength -> colour: low (magenta, accent2) through mid (violet) to high (accent3 teal).
export function relColour(v) {
  const t = Math.min(1, Math.max(0, v));
  return t < 0.5 ? `color-mix(in srgb, var(--accent2) ${Math.round((1 - t * 2) * 100)}%, var(--mid))`
    : `color-mix(in srgb, var(--accent3) ${Math.round((t * 2 - 1) * 100)}%, var(--mid))`;
}

export function relationshipGraph(story, { size = 460, highlight = [] } = {}) {
  const chars = story.world.characters, n = chars.length, c = size / 2, r = size * 0.33;
  const pos = chars.map((_, i) => {
    const a = -Math.PI / 2 + (2 * Math.PI * i) / n;
    return [c + r * Math.cos(a), c + r * Math.sin(a)];
  });
  const idx = Object.fromEntries(chars.map((ch, i) => [ch, i]));
  const lines = story.relationships.map(([a, b, v]) => {
    const [x1, y1] = pos[idx[a]], [x2, y2] = pos[idx[b]], w = 1 + 7 * Math.min(1, Math.max(0, v));
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
    return `<g class="rel"><title>${esc(a)} and ${esc(b)}: ${fmt(v)}</title>
      <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${relColour(v)}" stroke-width="${w.toFixed(1)}" stroke-linecap="round"/>
      <text x="${mx}" y="${my}" class="rv">${fmt(v)}</text></g>`;
  }).join('');
  const nodes = chars.map((ch, i) => {
    const [x, y] = pos[i], on = highlight.includes(ch);
    const lx = x + (x - c) * 0.32, ly = y + (y - c) * 0.22 + 4;
    return `<g class="cnode${on ? ' on' : ''}"><circle cx="${x}" cy="${y}" r="14"/>
      <text x="${lx}" y="${ly}" text-anchor="middle">${esc(ch.replace(/^The /, ''))}</text></g>`;
  }).join('');
  return `<svg class="relgraph" viewBox="0 0 ${size} ${size}" role="img"
    aria-label="Relationship strengths between ${n} characters">${lines}${nodes}</svg>`;
}

// Story map: start and introduction at the top, one column per branch below. Visited nodes are lit, the current one
// glows; visited nodes are links (keyboard focusable) that jump back to that point.
export function storyMap(story, { visited = new Set(), current = null, href = () => null } = {}) {
  const B = story.branches, colW = 74, L = 58, W = Math.max(280, B * colW + L + 10), rowH = 62, H = 5 * rowH + 20;
  const mid = L + (W - L - 10) / 2;
  const xOf = id => (id === 'start' || id === 'event_0' ? mid : L + colW / 2 + branchOf(id) * colW + (W - L - 10 - B * colW) / 2);
  const rowOf = id => (id === 'start' ? 0 : id === 'event_0' ? 1 : 2 + ((+id.split('_')[1] - 1) % 3));
  const P = id => [xOf(id), 22 + rowOf(id) * rowH];
  const ev = Object.fromEntries(story.events.map(e => [e.id, e]));
  const edges = story.edges.map(([a, b]) => {
    const [x1, y1] = P(a), [x2, y2] = P(b), lit = visited.has(a) && visited.has(b);
    return `<path d="M${x1},${y1} C${x1},${(y1 + y2) / 2} ${x2},${(y1 + y2) / 2} ${x2},${y2}" class="edge${lit ? ' lit' : ''}"/>`;
  }).join('');
  const ids = ['start', ...story.events.map(e => e.id)];
  const nodes = ids.map(id => {
    const [x, y] = P(id), seen = visited.has(id), e = ev[id];
    const label = id === 'start' ? 'Story start' : `${e.phase}: ${seen ? e.text : 'not visited yet'}`;
    const cls = `node ${e ? e.phase : 'start'}${seen ? ' seen' : ''}${id === current ? ' cur' : ''}`;
    const shape = e && e.phase === 'resolution'
      ? `<rect x="${x - 11}" y="${y - 11}" width="22" height="22" rx="4"/>` : `<circle cx="${x}" cy="${y}" r="${id === 'start' ? 8 : 11}"/>`;
    const link = seen ? href(id) : null;
    const inner = `<title>${esc(label)}</title>${shape}${id === 'start' ? '' : `<text x="${x}" y="${y + 4}">${+id.split('_')[1]}</text>`}`;
    return link ? `<a href="${esc(link)}" class="${cls}" aria-label="${esc('Go back to ' + label)}">${inner}</a>`
      : `<g class="${cls}">${inner}</g>`;
  }).join('');
  const rows = ['', 'intro', 'develop', 'climax', 'ending'].map((t, i) =>
    t ? `<text x="4" y="${26 + i * rowH}" class="rowlab">${t}</text>` : '').join('');
  return `<svg class="storymap" viewBox="0 0 ${W} ${H}" role="img" aria-label="Story map: ${visited.size - 1} of ${ids.length - 1} events visited">${rows}${edges}${nodes}</svg>`;
}
