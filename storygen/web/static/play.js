// Play: read the story as a gamebook. The introduction is the crossroads (one path per branch); each path runs
// development -> climax -> resolution. Progress (path, visited events, endings found) is saved in localStorage and
// the story is shareable by seed. The story map shows every branch, lit where you have been.
import { route, app, esc, tags, onLeave, go } from './core.js';
import { children, eventById, endings, branchOf, parseConsequence, mentions } from './story_engine.js';
import { pickStory, save, clearSave, controlsHtml, wireControls } from './store.js';
import { storyMap } from './svg.js';

const PHASE_LABEL = { introduction: 'Introduction', development: 'Development', climax: 'Climax', resolution: 'Resolution' };

function parents(story) {
  const p = {};
  for (const [a, b] of story.edges) p[b] = a;
  return p;
}
const chainTo = (par, id) => { const out = [id]; while (par[out[0]]) out.unshift(par[out[0]]); return out; };

function eventCard(story, e) {
  const m = mentions(story, e);
  const who = [...m.characters.map(c => [c, 'b']), ...m.locations.map(l => [l, 'c']), ...m.items.map(i => [i, 'a'])];
  const cons = e.consequences.map(parseConsequence)
    .map(c => `<span class="tag cons ${c.dir}">${c.dir === 'increase' ? '+' : '-'} ${esc(c.theme)}</span>`).join('');
  return `<p class="kicker">${PHASE_LABEL[e.phase]}${e.phase === 'introduction' ? '' : ` · path ${branchOf(e.id) + 1}`} · ${esc(e.id)}</p>
    <p class="scene">${esc(e.text)}</p>
    <div class="meta"><span class="tag mood">mood: ${esc(e.mood)}</span>
      <span class="tbar" title="tension ${e.tension.toFixed(1)}"><i style="width:${Math.round(e.tension * 100)}%"></i></span>
      <span class="small mute">tension ${e.tension.toFixed(1)}</span></div>
    ${who.length ? `<div class="who">${who.map(([n, c]) => `<span class="tag ${c}">${esc(n)}</span>`).join('')}</div>` : ''}
    <div class="cons-row"><span class="small mute">consequences:</span> ${cons}</div>`;
}

route('play', async (args, query) => {
  const { spec, story, saved } = await pickStory(query);
  const ev = eventById(story), ch = children(story), par = parents(story), ends = endings(story);
  let st = saved && saved.seed === story.seed && saved.branches === story.branches
    ? { ...saved } : { seed: story.seed, branches: story.branches, path: ['start'], visited: ['start'] };
  st.path = st.path.filter(id => id === 'start' || ev[id]);
  if (!st.path.length) st.path = ['start'];
  if (query.at && (st.visited.includes(query.at) || query.at === 'start')) {
    st.path = chainTo(par, query.at);
    history.replaceState(null, '', `#/play?seed=${story.seed}&branches=${story.branches}`);
  }
  const root = app();
  root.innerHTML = `<p class="kicker">Seed ${story.seed} · ${story.branches} branch${story.branches > 1 ? 'es' : ''}</p>
    <h1 class="glow">${esc(story.title)}</h1>
    ${controlsHtml(story, spec.max_branches)}
    <div class="playgrid"><section class="panel reader" aria-live="polite" id="reader"></section>
      <aside class="panel mapbox"><h3>Story map</h3><div id="map"></div>
        <p class="small mute" id="found"></p><button class="alt small-btn" id="forget">Forget progress</button></aside></div>
    <h2>Journal</h2><ol class="journal" id="journal"></ol>`;
  wireControls(root, story, 'play', (seed, branches) => go(`#/play?seed=${seed}&branches=${branches}`));

  const step = id => {
    st.path = chainTo(par, id);
    if (!st.visited.includes(id)) st.visited.push(id);
    save(st);
    draw();
    root.querySelector('#reader').focus({ preventScroll: true });
  };

  function choicesHtml(cur) {
    const next = ch[cur] || [];
    if (cur === 'start') return `<button data-to="event_0" class="choice">Begin the story</button>`;
    if (!next.length) {
      const found = ends.filter(id => st.visited.includes(id)).length;
      return `<p class="theend">The end. Ending ${ends.indexOf(cur) + 1} of ${ends.length}; you have found ${found} of ${ends.length}.</p>
        ${ends.length > 1 ? '<button data-to="event_0" class="choice">Back to the crossroads</button>' : ''}
        <button data-to="start" class="choice alt">Start over</button>`;
    }
    const head = next.length > 1 ? '<h3>Choose a path</h3>' : '';
    return head + next.map((id, i) => {
      const seen = st.visited.includes(id);
      return `<button data-to="${id}" class="choice${seen ? ' seen' : ''}"><span class="num">${i + 1}</span>
        ${esc(ev[id].text)}${seen ? ' <small>(visited)</small>' : ''}</button>`;
    }).join('');
  }

  function draw() {
    const cur = st.path[st.path.length - 1];
    const body = cur === 'start'
      ? `<p class="kicker">Story start</p><p class="scene">A story of ${story.world.locations.length} places,
          ${story.world.characters.length} characters and ${story.world.items.length} objects.</p>
         <h3>Places</h3>${tags(story.world.locations, 'c')}<h3>Characters</h3>${tags(story.world.characters, 'b')}
         <h3>Objects</h3>${tags(story.world.items, 'a')}`
      : eventCard(story, ev[cur]);
    const reader = root.querySelector('#reader');
    reader.tabIndex = -1;
    reader.innerHTML = body + `<div class="choices">${choicesHtml(cur)}</div>`;
    reader.querySelectorAll('[data-to]').forEach(b => b.addEventListener('click', () => step(b.dataset.to)));
    const vis = new Set(st.visited);
    root.querySelector('#map').innerHTML = storyMap(story, {
      visited: vis, current: cur, href: id => `#/play?seed=${story.seed}&branches=${story.branches}&at=${id}`,
    });
    const found = ends.filter(id => vis.has(id)).length;
    root.querySelector('#found').textContent = `${vis.size - 1} of ${story.events.length} events visited · ${found} of ${ends.length} endings found`;
    root.querySelector('#journal').innerHTML = st.path.filter(id => id !== 'start')
      .map(id => `<li><span class="tag">${PHASE_LABEL[ev[id].phase]}</span> ${esc(ev[id].text)}</li>`).join('')
      || '<li class="mute">Nothing yet: press "Begin the story".</li>';
  }
  root.querySelector('#forget').addEventListener('click', () => {
    clearSave();
    st = { seed: story.seed, branches: story.branches, path: ['start'], visited: ['start'] };
    draw();
  });

  // Number keys pick a choice (when not typing in a field).
  const onKey = e => {
    if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || '')) return;
    const n = +e.key;
    if (n >= 1 && n <= 9) { const b = root.querySelectorAll('.choices [data-to]')[n - 1]; if (b) b.click(); }
  };
  document.addEventListener('keydown', onKey);
  onLeave(() => document.removeEventListener('keydown', onKey));
  draw();
});
