// JS port of storygen (world.py + generator.py): NarrativeGenerator(seed) -> initialize_world() ->
// generate_story_structure(branches) -> tell_story(), drawing from the same random streams in the same order
// (Python's random.Random for choices, numpy default_rng for relationship strengths). Same seed, same story as the
// Python package: checked against tests/fixtures/stories.json by story_engine.test.mjs.
// The content (templates, themes, emotions, world lists) is not duplicated here: it comes from /api/spec.
import { PyRandom } from './py_random.js';
import { Generator } from './np_random.js';

export const PHASES = ['introduction', 'development', 'climax', 'resolution'];
export const MAX_SEED = Number.MAX_SAFE_INTEGER;

const pyTitle = s => s.replace(/[A-Za-z]+/g, w => w[0].toUpperCase() + w.slice(1).toLowerCase());
const fill = (template, vals) => template.replace(/\{(location|character|item)\}/g, (_, k) => vals[k]);

export function generateStory(spec, seed, branches = 3) {
  if (!Number.isSafeInteger(seed) || seed < 0) throw new Error('seed must be a whole number from 0 to 2^53-1');
  if (!Number.isInteger(branches) || branches < 1) throw new Error('num_branches must be >= 1');
  const py = new PyRandom(seed), np = new Generator(seed);
  const { locations, characters, items, themes, emotions, templates } = spec;

  // initialize_world(): a strength for every ordered pair, stored symmetrically (later pairs overwrite earlier)
  const rel = new Map();
  const key = (a, b) => (characters.indexOf(a) < characters.indexOf(b) ? `${a}|${b}` : `${b}|${a}`);
  for (const c1 of characters) for (const c2 of characters) if (c1 !== c2) rel.set(key(c1, c2), np.normal(0.5, 0.2));

  const events = [];
  const generateEvent = (phase, tension) => {
    if (!templates[phase]) throw new Error(`Unknown story phase: ${phase}`);
    const template = py.choice(templates[phase]);
    const text = fill(template, { location: py.choice(locations), character: py.choice(characters), item: py.choice(items) });
    const consequences = [];
    for (let i = 0, n = Math.max(1, Math.trunc(tension * 3)); i < n; i++) {
      const direction = py.random() < tension ? 'increase' : 'decrease';
      consequences.push(`tension_${direction}_${py.choice(themes)}`);
    }
    const ev = { id: `event_${events.length}`, phase, text, mood: py.choice(emotions), tension, consequences };
    events.push(ev);
    return ev;
  };

  // generate_story_structure(): networkx DiGraph; edges listed per source node in node-insertion order
  const adj = new Map([['start', []]]);
  const addEdge = (a, b) => { if (!adj.has(a)) adj.set(a, []); if (!adj.has(b)) adj.set(b, []); adj.get(a).push(b); };
  const intro = generateEvent('introduction', 0.3);
  addEdge('start', intro.id);
  for (let b = 0; b < branches; b++) {
    let current = intro.id, tension = 0.3;
    for (const phase of PHASES.slice(1)) {
      tension += 0.2;
      const ev = generateEvent(phase, tension);
      addEdge(current, ev.id);
      current = ev.id;
    }
  }
  const edges = [...adj].flatMap(([a, bs]) => bs.map(b => [a, b]));

  // tell_story(): the title draws two more choices
  const title = `The ${pyTitle(py.choice(themes))} of the ${py.choice(items)}`;
  const relationships = [];
  characters.forEach((a, i) => characters.slice(i + 1).forEach(b => relationships.push([a, b, rel.get(key(a, b))])));
  return {
    seed, branches, title,
    world: { locations: [...locations], characters: [...characters], items: [...items] },
    relationships, events, edges,
  };
}

// NarrativeGenerator.tell_story(): the story_data.json format written by story_generator.py.
export function tellStory(story) {
  return {
    title: story.title,
    world: story.world,
    events: Object.fromEntries(story.events.map(e => [e.id, { text: e.text, mood: e.mood, tension: e.tension }])),
    structure: { nodes: ['start', ...story.events.map(e => e.id)], edges: story.edges },
  };
}

// --- helpers for the reader ------------------------------------------------------------------------------------
export function children(story) {
  const m = { start: [] };
  for (const e of story.events) m[e.id] = [];
  for (const [a, b] of story.edges) m[a].push(b);
  return m;
}

export const eventById = story => Object.fromEntries(story.events.map(e => [e.id, e]));

// Which world names an event's text mentions (for the world graph and the event cards).
export function mentions(story, ev) {
  const w = story.world, has = n => ev.text.includes(n);
  return { locations: w.locations.filter(has), characters: w.characters.filter(has), items: w.items.filter(has) };
}

// The ending events (resolutions) and the branch index each event belongs to (introduction: -1).
export function branchOf(eventId) {
  const n = +eventId.split('_')[1];
  return n === 0 ? -1 : Math.floor((n - 1) / 3);
}
export const endings = story => story.events.filter(e => e.phase === 'resolution').map(e => e.id);

// "tension_increase_love" -> { dir: 'increase', theme: 'love' }
export function parseConsequence(c) {
  const [, dir, theme] = c.split('_');
  return { dir, theme };
}

// Compare two stories field by field (floats with a relative tolerance); returns a list of differences.
export function diffStories(a, b, rtol = 1e-12) {
  const out = [];
  const close = (x, y) => Math.abs(x - y) <= rtol * Math.max(1, Math.abs(x), Math.abs(y));
  const walk = (x, y, path) => {
    if (typeof x === 'number' && typeof y === 'number') { if (!close(x, y)) out.push(`${path}: ${x} != ${y}`); return; }
    if (Array.isArray(x) && Array.isArray(y)) {
      if (x.length !== y.length) { out.push(`${path}: length ${x.length} != ${y.length}`); return; }
      x.forEach((v, i) => walk(v, y[i], `${path}[${i}]`)); return;
    }
    if (x && y && typeof x === 'object' && typeof y === 'object') {
      const ks = new Set([...Object.keys(x), ...Object.keys(y)]);
      for (const k of ks) walk(x[k], y[k], path ? `${path}.${k}` : k);
      return;
    }
    if (x !== y) out.push(`${path}: ${JSON.stringify(x)} != ${JSON.stringify(y)}`);
  };
  walk(a, b, '');
  return out;
}
