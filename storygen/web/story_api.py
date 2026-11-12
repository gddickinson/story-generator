"""Story data for the web interface, produced by the real storygen package.

spec()  -> the generator's built-in content (templates, themes, emotions, world lists) that the JS engine uses.
story() -> one generated story with everything the reader needs: events with phase and consequences, the branch
           structure and the character relationship strengths.
"""
from __future__ import annotations

from storygen import NarrativeGenerator

PHASES = ["development", "climax", "resolution"]
MAX_BRANCHES = 8
SAMPLE_SEEDS = [0, 1, 7, 42, 99, 2026, 31337]
SAMPLE_BRANCHES = [1, 3, 5, 8]


def spec() -> dict:
    """The content the generator draws from, read off a freshly initialised NarrativeGenerator."""
    g = NarrativeGenerator(seed=0)
    g.initialize_world()
    w = g.story_world
    return {
        "templates": g.plot_points,
        "themes": list(g.themes),
        "emotions": list(g.emotions),
        "locations": list(w.locations),
        "characters": list(w.characters),
        "items": list(w.items),
        "relationship": {"mean": 0.5, "sd": 0.2},
        "max_branches": MAX_BRANCHES,
    }


def story(seed: int, branches: int = 3) -> dict:
    """Generate a story exactly as story_generator.py does (initialise, structure, tell) and serialise it."""
    if seed < 0 or seed >= 2**53:
        raise ValueError("seed must be in 0 .. 2**53-1")
    if not 1 <= branches <= MAX_BRANCHES:
        raise ValueError(f"branches must be 1..{MAX_BRANCHES}")
    g = NarrativeGenerator(seed=seed)
    g.initialize_world()
    g.generate_story_structure(num_branches=branches)
    told = g.tell_story()
    chars = list(g.story_world.characters)
    rel = g.story_world.relationships
    phase = {"event_0": "introduction"}
    for b in range(branches):
        for k, p in enumerate(PHASES):
            phase[f"event_{1 + 3 * b + k}"] = p
    return {
        "seed": seed,
        "branches": branches,
        "title": told["title"],
        "world": told["world"],
        "relationships": [[a, b, rel[a][b]] for i, a in enumerate(chars) for b in chars[i + 1:]],
        "events": [
            {"id": eid, "phase": phase[eid], "text": ev.text, "mood": ev.mood,
             "tension": ev.tension_level, "consequences": list(ev.consequences)}
            for eid, ev in g.events.items()
        ],
        "edges": [list(e) for e in told["structure"]["edges"]],
    }


def samples() -> list[dict]:
    """Python stories for a fixed set of seeds, so the static site can check the JS engine against them."""
    return [story(s, b) for s in SAMPLE_SEEDS for b in SAMPLE_BRANCHES]
