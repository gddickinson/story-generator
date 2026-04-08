# Interactive Story Generator -- Roadmap

## Current State
A single-file project (`story-generator.py`, ~250 lines) using NetworkX for graph
representation and matplotlib for visualization. Contains three classes:
`StoryEvent` (dataclass), `StoryWorld`, and `NarrativeGenerator`. Generates
branching narratives with locations, characters, items, relationships, and
tension curves. Outputs `story_structure.png` and `story_data.json`. Functional
but minimal -- stories are template-driven with random selection from hardcoded
lists. No tests, no package structure, no CLI options.

## Short-term Improvements
- [x] Split `story-generator.py` into a package: `storygen/world.py`,
      `storygen/generator.py`, `storygen/visualization.py`, `storygen/models.py`
- [x] Rename from `story-generator.py` to `story_generator.py` (hyphens break
      Python imports)
- [x] Add type hints to all methods, especially `generate_event()` and
      `tell_story()`
- [x] Add CLI with argparse: `--seed`, `--branches`, `--output-dir`, `--theme`
- [x] Add input validation in `NarrativeGenerator` (e.g., num_branches > 0)
- [x] Externalize story templates (locations, character names, plot points) into
      a `data/templates.json` so users can customize without editing code
- [x] Add unit tests for world initialization, event generation, and graph
      structure

## Feature Enhancements
- [ ] Add an interactive reader mode: present story in terminal with choices at
      branch points (using `rich` or `prompt_toolkit`)
- [ ] Implement character arc tracking: each character accumulates experiences
      that influence later events (currently characters are just names)
- [ ] Add genre presets (fantasy, sci-fi, mystery, romance) with genre-specific
      templates, vocabulary, and tension curves
- [ ] Improve narrative coherence: events should reference earlier events and
      maintain causal chains (currently each event is mostly independent)
- [ ] Add a web UI (Flask/Streamlit) for generating and exploring stories
- [ ] Generate longer stories with subplots and parallel character threads
- [ ] Add illustration generation: create scene descriptions suitable for
      image generation APIs (DALL-E, Stable Diffusion prompts)

## Long-term Vision
- [ ] LLM integration: use a local model to generate natural-language prose
      from the structural story graph, producing readable short stories
- [ ] Collaborative storytelling: multiple users contribute to the same story
      graph in real-time via a web interface
- [ ] Export to interactive fiction formats (Twine/Ink/Ren'Py) for playable
      stories
- [ ] Procedural world-building toolkit: generate entire fantasy/sci-fi worlds
      with consistent geography, history, and politics
- [ ] Analytics dashboard: visualize story statistics (tension curves, character
      screen time, relationship evolution)

## Technical Debt
- [x] All logic is in one file -- this is the most urgent refactoring need
- [x] `story_data.json` and `story_structure.png` are generated outputs that
      should not be version-controlled -- add to `.gitignore`
- [x] The `np.random.seed()` call is deprecated -- use `np.random.Generator`
- [x] No `requirements.txt` -- add one (numpy, networkx, matplotlib)
- [x] The `visualize_story_graph()` method uses hardcoded colors and layout
      -- make these configurable
- [ ] Relationship system in `StoryWorld` is defined but underutilized in
      story generation
