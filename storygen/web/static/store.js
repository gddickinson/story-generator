// Shared state for the pages: the generator content (/api/spec), the current story (generated in the browser by
// story_engine.js) and the reader's progress, saved to localStorage (wrapped in try/catch: storage can be missing or
// blocked) and shareable as #/play?seed=N&branches=B links.
import { api } from './core.js';
import { generateStory, MAX_SEED } from './story_engine.js';

const KEY = 'storygen.save.v1';
export const DEFAULT = { seed: 42, branches: 3 };

let spec = null;
export async function getSpec() { return spec || (spec = await api('/spec')); }

export function loadSave() {
  try {
    const s = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (s && Number.isSafeInteger(s.seed) && Number.isInteger(s.branches) && Array.isArray(s.path)) return s;
  } catch (e) { /* no storage: start fresh */ }
  return null;
}

export function save(state) {
  try { localStorage.setItem(KEY, JSON.stringify(state)); return true; } catch (e) { return false; }
}

export function clearSave() { try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ } }

// Seed and branch count from a route query, else the saved game, else the default.
export async function pickStory(query = {}) {
  const sp = await getSpec();
  const saved = loadSave();
  const q = query.seed != null ? +query.seed : NaN;
  const seed = Number.isSafeInteger(q) && q >= 0 ? q : saved ? saved.seed : DEFAULT.seed;
  const qb = query.branches != null ? +query.branches : NaN;
  let branches = Number.isInteger(qb) ? qb : saved && saved.seed === seed ? saved.branches : DEFAULT.branches;
  branches = Math.min(sp.max_branches, Math.max(1, branches));
  return { spec: sp, story: generateStory(sp, seed, branches), saved };
}

export const randomSeed = () => Math.floor(Math.random() * 1e6);
export const clampSeed = v => Math.min(MAX_SEED, Math.max(0, Math.trunc(+v || 0)));

export function shareLink(seed, branches, page = 'play') {
  return `${location.origin}${location.pathname}#/${page}?seed=${seed}&branches=${branches}`;
}

// Seed / branches / buttons used by the play, world and story pages. onChange(seed, branches) regenerates.
export function controlsHtml(story, maxBranches) {
  return `<div class="row ctlrow">
    <div><label for="seed">Seed</label><input id="seed" type="number" min="0" step="1" value="${story.seed}"></div>
    <div><label for="branches">Branches <b id="bval">${story.branches}</b></label>
      <input id="branches" type="range" min="1" max="${maxBranches}" value="${story.branches}"></div>
    <div class="btns"><button id="go">Generate</button><button id="rnd" class="alt">Random seed</button>
      <button id="share" class="alt" title="Copy a link to this story">Share link</button></div>
  </div><p id="sharemsg" class="small mute" aria-live="polite"></p>`;
}

export function wireControls(root, story, page, onChange) {
  const seedEl = root.querySelector('#seed'), brEl = root.querySelector('#branches');
  brEl.addEventListener('input', () => { root.querySelector('#bval').textContent = brEl.value; });
  const fire = seed => onChange(clampSeed(seed), +brEl.value);
  root.querySelector('#go').addEventListener('click', () => fire(seedEl.value));
  seedEl.addEventListener('keydown', e => { if (e.key === 'Enter') fire(seedEl.value); });
  brEl.addEventListener('change', () => fire(seedEl.value));
  root.querySelector('#rnd').addEventListener('click', () => fire(randomSeed()));
  root.querySelector('#share').addEventListener('click', async () => {
    const link = shareLink(story.seed, story.branches, page), msg = root.querySelector('#sharemsg');
    try { await navigator.clipboard.writeText(link); msg.textContent = 'Link copied: ' + link; }
    catch (e) { msg.textContent = 'Share this link: ' + link; }
  });
}
