"""Write tests/fixtures/stories.json: Python reference values for the JS port (story_engine.test.mjs).

Contains the generator content (spec), raw random streams (Python random and numpy default_rng) for a few seeds, and
complete stories for the sample seeds plus extra seeds/branch counts. tests/test_web.py checks the file is current.

Run: python scripts/make_story_fixture.py
"""
import json
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from storygen import NarrativeGenerator  # noqa: E402
from storygen.web import story_api  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "stories.json"
RNG_SEEDS = [0, 1, 42, 2**32 + 5, 123456789012]
EXTRA = [(s, 1 + s % 8) for s in range(0, 400, 7)] + [(2**40 + 3, 4), (9007199254740991, 2)]


def rng_streams() -> list:
    out = []
    for s in RNG_SEEDS:
        r = random.Random(s)
        g = np.random.default_rng(s)
        out.append({
            "seed": s,
            "random": [r.random() for _ in range(5)],
            "choice7": [r.choice(range(7)) for _ in range(10)],
            "normal": [float(g.normal(0.5, 0.2)) for _ in range(25)],
        })
    return out


def story_data(seed: int, branches: int) -> dict:
    """story_data.json exactly as story_generator.py writes it."""
    g = NarrativeGenerator(seed=seed)
    g.initialize_world()
    g.generate_story_structure(num_branches=branches)
    return {"seed": seed, "branches": branches, "json": json.dumps(g.tell_story(), indent=2)}


def build() -> dict:
    return {
        "numpy": np.__version__,
        "python": sys.version.split()[0],
        "spec": story_api.spec(),
        "rng": rng_streams(),
        "story_data": story_data(42, 3),
        "stories": story_api.samples() + [story_api.story(s, b) for s, b in EXTRA],
    }


if __name__ == "__main__":
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    data = build()
    FIXTURE.write_text(json.dumps(data, separators=(",", ":")))
    print(f"wrote {FIXTURE} ({len(data['stories'])} stories, {FIXTURE.stat().st_size / 1e3:.0f} kB)")
