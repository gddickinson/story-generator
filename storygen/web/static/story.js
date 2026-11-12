// Script: the whole story at once, as story_generator.py prints it, plus a download of story_data.json in the same
// format NarrativeGenerator.tell_story() writes (title, world, events, structure).
import { route, app, esc, go, download } from './core.js';
import { pickStory, controlsHtml, wireControls } from './store.js';
import { storyMap } from './svg.js';
import { tellStory } from './story_engine.js';

route('story', async (args, query) => {
  const { spec, story } = await pickStory(query);
  const root = app();
  const intro = story.events[0];
  const paths = Array.from({ length: story.branches }, (_, b) => story.events.slice(1 + 3 * b, 4 + 3 * b));
  const row = e => `<li><span class="tag">${esc(e.phase)}</span> ${esc(e.text)}
    <span class="small mute">· ${esc(e.mood)} · tension ${e.tension.toFixed(2)}</span></li>`;
  root.innerHTML = `<p class="kicker">Full script · seed ${story.seed}</p><h1 class="glow">${esc(story.title)}</h1>
    <p class="lead">Every event the generator made, branch by branch: what <code>python story_generator.py --seed
      ${story.seed} --branches ${story.branches}</code> prints. Spoilers for every ending.</p>
    ${controlsHtml(story, spec.max_branches)}
    <div class="side"><div class="panel">${storyMap(story, { visited: new Set(['start', ...story.events.map(e => e.id)]) })}
      <button id="dl" class="alt">Download story_data.json</button></div>
      <div><div class="panel"><h3>Introduction</h3><ol class="script">${row(intro)}</ol></div>
        ${paths.map((p, b) => `<div class="panel"><h3>Path ${b + 1}</h3><ol class="script">${p.map(row).join('')}</ol></div>`).join('')}
      </div></div>`;
  wireControls(root, story, 'story', (seed, branches) => go(`#/story?seed=${seed}&branches=${branches}`));
  root.querySelector('#dl').addEventListener('click', () =>
    download('story_data.json', JSON.stringify(tellStory(story), null, 2), 'application/json'));
});
