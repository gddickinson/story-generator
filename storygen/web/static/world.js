// World: the characters' relationship graph (a strength for every pair, from numpy default_rng(seed).normal(0.5, 0.2)
// as in StoryWorld.set_relationship) and which events mention each place, character and object.
import { route, app, esc, go } from './core.js';
import { mentions, branchOf } from './story_engine.js';
import { pickStory, controlsHtml, wireControls } from './store.js';
import { relationshipGraph, relColour } from './svg.js';

route('world', async (args, query) => {
  const { spec, story } = await pickStory(query);
  const root = app();
  const rels = [...story.relationships].sort((a, b) => b[2] - a[2]);
  const appear = { locations: {}, characters: {}, items: {} };
  for (const e of story.events) {
    const m = mentions(story, e);
    for (const k of Object.keys(appear)) for (const n of m[k]) (appear[k][n] ||= []).push(e);
  }
  const at = id => `#/play?seed=${story.seed}&branches=${story.branches}`;
  const block = (k, title, cls) => `<div class="panel"><h3>${title}</h3><table><tbody>${story.world[k].map(n => {
    const es = appear[k][n] || [];
    return `<tr><td><span class="tag ${cls}">${esc(n)}</span></td><td class="small">${es.length
      ? es.map(e => `<span title="${esc(e.text)}">${esc(e.id)}${e.phase === 'introduction' ? '' : ` (path ${branchOf(e.id) + 1})`}</span>`).join(', ')
      : '<span class="mute">not in this story</span>'}</td></tr>`;
  }).join('')}</tbody></table></div>`;

  root.innerHTML = `<p class="kicker">World · seed ${story.seed}</p><h1 class="glow">${esc(story.title)}</h1>
    <p class="lead">Every pair of characters has a relationship strength drawn when the world is initialised
      (normal distribution, mean ${spec.relationship.mean}, sd ${spec.relationship.sd}). Thicker, tealer lines are
      stronger bonds; thin magenta lines are weak or negative ones. The generator does not yet use them in the plot.</p>
    ${controlsHtml(story, spec.max_branches)}
    <div class="two"><div class="panel graphbox">${relationshipGraph(story)}
      <div class="legend"><span><i style="background:${relColour(0)}"></i>0 or below</span>
        <span><i style="background:${relColour(0.5)}"></i>0.5</span><span><i style="background:${relColour(1)}"></i>1 or above</span></div></div>
      <div class="panel"><h3>Strongest to weakest</h3><table><thead><tr><th>Pair</th><th>Strength</th></tr></thead><tbody>
        ${rels.map(([a, b, v]) => `<tr><td>${esc(a)} &amp; ${esc(b)}</td><td class="mono"><span class="sw" style="background:${relColour(v)}"></span>${v.toFixed(3)}</td></tr>`).join('')}
      </tbody></table></div></div>
    <h2>Who and what appears where</h2>
    <p class="small mute">Events whose text names each element (templates without a {location}, {character} or {item}
      slot do not mention one). <a href="${at()}">Play this story</a>.</p>
    <div class="three">${block('characters', 'Characters', 'b')}${block('locations', 'Places', 'c')}${block('items', 'Objects', 'a')}</div>`;
  wireControls(root, story, 'world', (seed, branches) => go(`#/world?seed=${seed}&branches=${branches}`));
});
