# Interactive Story Generator -- Interface Map

## Package: `storygen/`
| File | Purpose | Key Classes/Functions |
|---|---|---|
| `__init__.py` | Package root; re-exports public API | `StoryEvent`, `StoryWorld`, `NarrativeGenerator` |
| `models.py` | Data models | `StoryEvent` (dataclass) |
| `world.py` | World state container | `StoryWorld` (locations, characters, items, relationships), `OrderedSet` |
| `generator.py` | Narrative generation & graph building (own `random.Random` + numpy `default_rng` per generator) | `NarrativeGenerator`, `_load_templates()` |
| `visualization.py` | Graph rendering to PNG | `visualize_story_graph()` |

## Web interface: `storygen/web/`
| File | Purpose |
|---|---|
| `app.py` | FastAPI app: `/api/info`, `/api/spec`, `/api/samples`, `/api/story/{seed}?branches=`; `STATIC_ENDPOINTS` |
| `story_api.py` | `spec()`, `story(seed, branches)`, `samples()`: story data from the real package |
| `static/index.html`, `main.js`, `core.js` | Shell, page registration, hash router (`core.js`, `style.css`: shared web kit, unchanged) |
| `static/story_engine.js` | JS port of the generator: `generateStory(spec, seed, branches)`, `tellStory`, `children`, `mentions`, `diffStories` |
| `static/py_random.js` | CPython `random.Random` (MT19937, `random`, `choice`) |
| `static/np_random.js`, `ziggurat_tables.js` | NumPy `default_rng` (SeedSequence, PCG64, ziggurat normal); from landscape-generator |
| `static/store.js` | Spec loading, localStorage save/restore, share links, seed/branch controls |
| `static/svg.js` | `relationshipGraph()`, `storyMap()`, `relColour()` |
| `static/play.js`, `world.js`, `story.js`, `verify.js`, `home.js`, `about.js` | Pages (`#/play`, `#/world`, `#/story`, `#/verify`, home, about) |
| `static/static_api.js` | Answers `api()` from exported JSON on GitHub Pages |
| `static/story_engine.test.mjs` | Node test: JS engine vs `tests/fixtures/stories.json` |

## Entry Points
| File | Purpose |
|---|---|
| `story_generator.py` | CLI entry point with argparse (`--seed`, `--branches`, `--output-dir`, `--theme`) |
| `run_web.py` | Local web app on 127.0.0.1:8138 |

## Scripts
| File | Purpose |
|---|---|
| `scripts/build_static.py` | Export the static site to `site/` (used by `.github/workflows/pages.yml`) |
| `scripts/screenshots.py` | Playwright smoke test of routes + README images (`docs/img/`) |
| `scripts/make_story_fixture.py` | Write `tests/fixtures/stories.json` (Python reference for the JS port) |

## Data
| File | Purpose |
|---|---|
| `data/templates.json` | Externalised plot-point templates (introduction/development/climax/resolution) |

## Tests
| File | Purpose |
|---|---|
| `tests/test_storygen.py` | Smoke tests for models, world, generator, serialization |
| `tests/test_regressions.py` | Fixed bugs: same seed same story across processes; no global random reseeding |
| `tests/test_web.py` | API, static build, fixture is current, node engine test |

## Legacy
| File | Purpose |
|---|---|
| `story-generator.py` | Original monolith (kept for reference; superseded by `storygen/` package; still has the set-order bug) |

## Module Dependencies
```
story_generator.py  -->  storygen.generator
                          |-> storygen.world
                          |-> storygen.models
                          |-> storygen.visualization
                          |-> data/templates.json (optional)
run_web.py --> storygen.web.app --> storygen.web.story_api --> storygen
static: main.js --> page modules --> store.js / svg.js --> story_engine.js --> py_random.js, np_random.js
```
