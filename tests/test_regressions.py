"""
tests/test_regressions.py
=========================
Regression tests for bugs fixed in the existing code (see SESSION_LOG.md).
"""

import json
import os

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
