"""
tests/test_regressions.py
=========================
Regression tests for bugs fixed in the existing code (see SESSION_LOG.md).
"""

import json
import os
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_SCRIPT = (
    "import json, sys\n"
    "from storygen import NarrativeGenerator\n"
    "g = NarrativeGenerator(seed=42)\n"
    "g.initialize_world()\n"
    "g.generate_story_structure(num_branches=3)\n"
    "print(json.dumps(g.tell_story()))\n"
)


def _story_with_hashseed(hashseed: str) -> dict:
    env = dict(os.environ, PYTHONHASHSEED=hashseed)
    out = subprocess.run(
        [sys.executable, "-c", _SCRIPT], cwd=ROOT, env=env,
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


def test_same_seed_same_story_across_processes():
    """A seed gives the same story in every Python process.

    Bug: StoryWorld kept locations/characters/items in sets, whose order depends on
    string hashing (randomised per process), so random.choice() over them picked
    different places and items for the same seed.
    """
    stories = [_story_with_hashseed(h) for h in ("1", "2", "3", "4")]
    assert all(s == stories[0] for s in stories[1:])


def test_world_keeps_insertion_order():
    """World elements come back in the order they were added."""
    from storygen import StoryWorld
    w = StoryWorld()
    names = ["Zeta", "Alpha", "Mid", "Beta", "Omega"]
    for n in names:
        w.add_location(n)
    w.add_location("Alpha")  # duplicates are still ignored
    assert list(w.locations) == names
    assert len(w.locations) == 5 and "Mid" in w.locations


def test_generator_leaves_global_random_alone():
    """Creating a seeded generator must not reseed Python's global random module.

    Bug: NarrativeGenerator(seed) called random.seed(seed), resetting the global
    random state of the whole program (and making concurrent generators, e.g. in
    a web server, interfere with each other).
    """
    from storygen import NarrativeGenerator
    random.seed(12345)
    expected = random.random()
    random.seed(12345)
    NarrativeGenerator(seed=7).initialize_world()
    assert random.random() == expected


def test_interleaved_generators_are_independent():
    """Two seeded generators used alternately give the same stories as used alone."""
    from storygen import NarrativeGenerator

    def alone(seed):
        g = NarrativeGenerator(seed=seed)
        g.initialize_world()
        g.generate_story_structure(num_branches=2)
        return g.tell_story()

    a, b = NarrativeGenerator(seed=1), NarrativeGenerator(seed=2)
    a.initialize_world(); b.initialize_world()
    for phase, t in (("introduction", 0.3), ("development", 0.5)):
        a.generate_event(phase, t); b.generate_event(phase, t)
    a2, b2 = NarrativeGenerator(seed=1), NarrativeGenerator(seed=2)
    a2.initialize_world(); a2.generate_event("introduction", 0.3); a2.generate_event("development", 0.5)
    b2.initialize_world(); b2.generate_event("introduction", 0.3); b2.generate_event("development", 0.5)
    assert [e.text for e in a.events.values()] == [e.text for e in a2.events.values()]
    assert [e.text for e in b.events.values()] == [e.text for e in b2.events.values()]
    assert alone(3) == alone(3)
