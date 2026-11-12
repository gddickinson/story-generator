// Check: the in-browser generator against stories made by the Python package. The sample stories (/api/samples) are
// exported with the static site; on the local app any seed can be checked live against /api/story/<seed>.
import { route, app, esc, api, isStatic, needsServer } from './core.js';
import { generateStory, diffStories } from './story_engine.js';
import { getSpec, clampSeed } from './store.js';

function compare(spec, want) {
  const got = generateStory(spec, want.seed, want.branches);
  const textual = diffStories({ ...got, relationships: null }, { ...want, relationships: null }, 0);
  let maxRel = 0;
  got.relationships.forEach((r, i) => {
    maxRel = Math.max(maxRel, Math.abs(r[2] - want.relationships[i][2]) / Math.max(1e-300, Math.abs(want.relationships[i][2])));
  });
  return { got, textual, maxRel, ok: !textual.length && maxRel < 1e-12 };
}

const rowHtml = (want, c) => `<tr><td class="mono">${want.seed}</td><td class="mono">${want.branches}</td>
  <td>${esc(want.title)}</td><td class="${c.textual.length ? 'err' : 'ok'}">${c.textual.length ? esc(c.textual[0]) : 'identical'}</td>
  <td class="mono ${c.maxRel < 1e-12 ? 'ok' : 'err'}">${c.maxRel ? c.maxRel.toExponential(1) : '0'}</td>
  <td><a href="#/play?seed=${want.seed}&branches=${want.branches}">play</a></td></tr>`;

route('verify', async () => {
  const [spec, S] = await Promise.all([getSpec(), api('/samples')]);
  const results = S.stories.map(w => [w, compare(spec, w)]);
  const nOk = results.filter(([, c]) => c.ok).length;
  const root = app();
  root.innerHTML = `<p class="kicker">JS vs Python</p><h1 class="glow">Same seed, same story</h1>
    <p class="lead">The generator on this site is a JavaScript port of <code>storygen</code>. It reproduces CPython's
      <code>random.Random</code> (Mersenne Twister) for every choice and NumPy's <code>default_rng</code> (PCG64 and the
      ziggurat normal) for the relationship strengths, drawing in the same order as the Python code.</p>
    <div class="tiles"><div class="tile"><b>${nOk}/${results.length}</b><span>sample stories match</span></div>
      <div class="tile"><b>${S.seeds.length}</b><span>seeds</span></div><div class="tile"><b>${S.branches.join(', ')}</b><span>branch counts</span></div></div>
    <p class="small mute">Titles, event texts, moods, tensions, consequences and the branch structure must be identical.
      Relationship strengths are compared with a relative tolerance of 1e-12: NumPy's ARM64 build computes
      <code>0.5 + 0.2 * z</code> with a fused multiply-add, which can differ from the plain formula in the last bit.</p>
    <div id="live" class="panel"></div>
    <div class="scroll panel"><table><thead><tr><th>Seed</th><th>Branches</th><th>Python title</th><th>Text, choices, structure</th>
      <th>Max rel. diff (relationships)</th><th></th></tr></thead><tbody>${results.map(([w, c]) => rowHtml(w, c)).join('')}</tbody></table></div>`;
  const live = root.querySelector('#live');
  if (isStatic()) { live.innerHTML = `<h3>Check any seed</h3>${needsServer('Checking an arbitrary seed against Python')}`; return; }
  live.innerHTML = `<h3>Check any seed against the Python server</h3><div class="row">
    <div><label for="vseed">Seed</label><input id="vseed" type="number" min="0" value="${Math.floor(Math.random() * 1e6)}"></div>
    <div><label for="vbr">Branches</label><input id="vbr" type="number" min="1" max="${spec.max_branches}" value="3"></div>
    <div><button id="vgo">Check</button></div></div><div id="vout" aria-live="polite"></div>`;
  root.querySelector('#vgo').addEventListener('click', async () => {
    const seed = clampSeed(root.querySelector('#vseed').value), br = Math.min(spec.max_branches, Math.max(1, +root.querySelector('#vbr').value || 3));
    const want = await api(`/story/${seed}?branches=${br}`);
    root.querySelector('#vout').innerHTML = `<table><tbody>${rowHtml(want, compare(spec, want))}</tbody></table>`;
  });
});
