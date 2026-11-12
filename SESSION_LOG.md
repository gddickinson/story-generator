# Session Log

## 2026-11-11: web interface and static GitHub Pages site (branch `web-interface`)
- Bugs fixed in existing code (separate commits, regression tests in `tests/test_regressions.py`):
  1. Same `--seed` gave different stories in different runs: `StoryWorld` used sets, whose order depends on
     per-process string hashing. Now an insertion-ordered `OrderedSet` (same set API).
  2. `NarrativeGenerator(seed)` reseeded Python's global `random` module (side effect; concurrent generators interfered).
     Each generator now owns a `random.Random(seed)`; output for a seed is unchanged (checked on 30 seeds).
  3. README claimed relationships are in `story_data.json`, adjustable themes and "dynamic" relationships: corrected.
- Added `storygen/web/` (FastAPI + ES modules): Play (gamebook reader, story map, localStorage save, share links),
  World (relationship graph SVG), Script (all branches, story_data.json download), Check (JS vs Python).
- JS port `story_engine.js` + `py_random.js` + `np_random.js` (NumPy default_rng port reused from landscape-generator).
  Node test: 88 stories match Python; texts/choices/structure identical, story_data.json byte-identical; relationship
  strengths within 1 ULP (NumPy arm64 uses fused multiply-add for `loc + scale*z`).
- Verified: pytest (all tests), screenshots.py on static site and on run_web.py (port 8138), phone width 390 px.
- Not done / for George: `requirements.txt` pins numpy<2.0 while the web/CI pins 2.5.4; generated `story_data.json`
  and `story_structure.png` are still tracked; legacy `story-generator.py` still has the set-order bug.
- No LLM/API use. Mac mini not used.
