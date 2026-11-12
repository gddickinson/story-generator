// About: what the generator is, how it works, how to run it, credits.
import { route, app } from './core.js';

route('about', () => {
  app().innerHTML = `<p class="kicker">About</p><h1 class="glow">Interactive Story Generator</h1>
    <p class="lead">A Python-based procedural narrative generation system that creates branching interactive stories
      with rich world-building and character relationships.</p>
    <h2>How a story is made</h2>
    <ol><li><b>World.</b> Five places, five characters and five objects; every pair of characters gets a relationship
      strength drawn from a normal distribution (mean 0.5, sd 0.2).</li>
      <li><b>Introduction.</b> One event from the introduction templates, at tension 0.3.</li>
      <li><b>Branches.</b> For each branch, a development, a climax and a resolution event, with tension rising by 0.2
        each step. Each template is filled with a random place, character and object; each event gets a mood and
        one to three consequences (tension rises or falls for a theme).</li>
      <li><b>Title.</b> "The <i>theme</i> of the <i>object</i>".</li></ol>
    <p>The templates live in <code>data/templates.json</code>; the structure is a NetworkX directed graph. Character
      relationships and consequences are generated but do not yet steer the plot.</p>
    <h2>This web interface</h2>
    <p>The pages run a JavaScript port of the generator (<code>story_engine.js</code>) that reproduces Python's random
      module and NumPy's <code>default_rng</code>, so a seed gives the same story here as in Python
      (see <a href="#/verify">Check</a>). The reader, story map, saving and share links are additions of the web
      interface; the stories themselves are exactly the generator's.</p>
    <h2>Run it</h2>
    <h3>Command line</h3><pre>pip install -r requirements.txt
python story_generator.py --seed 42 --branches 3 --output-dir output/</pre>
    <p>Writes <code>story_structure.png</code> (graph drawing) and <code>story_data.json</code>, and prints the story.</p>
    <h3>Web app (local)</h3><pre>pip install -r requirements-web.txt
python run_web.py        # http://127.0.0.1:8138</pre>
    <p>The local app adds a live check of any seed against the Python generator.</p>
    <h2>Credits</h2>
    <p>By George Dickinson. Built using NetworkX for graph visualisation and matplotlib for the images; inspired by
      narrative theory and procedural generation techniques. MIT licence.
      <a href="https://github.com/gddickinson/story-generator">Source on GitHub</a>.</p>`;
});
