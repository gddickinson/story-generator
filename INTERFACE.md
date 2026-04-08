# Interactive Story Generator -- Interface Map

## Package: `storygen/`
| File | Purpose | Key Classes/Functions |
|---|---|---|
| `__init__.py` | Package root; re-exports public API | `StoryEvent`, `StoryWorld`, `NarrativeGenerator` |
| `models.py` | Data models | `StoryEvent` (dataclass) |
| `world.py` | World state container | `StoryWorld` (locations, characters, items, relationships) |
| `generator.py` | Narrative generation & graph building | `NarrativeGenerator`, `_load_templates()` |
| `visualization.py` | Graph rendering to PNG | `visualize_story_graph()` |

## Entry Point
| File | Purpose |
|---|---|
| `story_generator.py` | CLI entry point with argparse (`--seed`, `--branches`, `--output-dir`, `--theme`) |

## Data
| File | Purpose |
|---|---|
| `data/templates.json` | Externalised plot-point templates (introduction/development/climax/resolution) |

## Tests
| File | Purpose |
|---|---|
| `tests/test_storygen.py` | Smoke tests for models, world, generator, serialization |

## Legacy
| File | Purpose |
|---|---|
| `story-generator.py` | Original monolith (kept for reference; superseded by `storygen/` package) |

## Module Dependencies
```
story_generator.py  -->  storygen.generator
                          |-> storygen.world
                          |-> storygen.models
                          |-> storygen.visualization
                          |-> data/templates.json (optional)
```
