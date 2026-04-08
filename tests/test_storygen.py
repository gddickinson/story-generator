"""
tests/test_storygen.py
======================
Smoke tests for the storygen package.
"""

import json
import tempfile
from pathlib import Path

from storygen.models import StoryEvent
from storygen.world import StoryWorld
from storygen.generator import NarrativeGenerator


def test_story_event_creation():
    """StoryEvent dataclass can be instantiated."""
    event = StoryEvent(
        id="e1", text="Something happened", mood="joy",
        consequences=["c1"], requirements=[], tension_level=0.5,
    )
    assert event.id == "e1"
    assert event.tension_level == 0.5


def test_story_world_basics():
    """StoryWorld tracks locations, characters, items, relationships."""
    world = StoryWorld()
    world.add_location("Forest")
    world.add_character("Hero")
    world.add_item("Sword")
    assert "Forest" in world.locations
    assert "Hero" in world.characters
    assert "Sword" in world.items

    world.set_relationship("Hero", "Villain", -0.5)
    assert world.relationships["Hero"]["Villain"] == -0.5
    assert world.relationships["Villain"]["Hero"] == -0.5


def test_initialize_world():
    """NarrativeGenerator.initialize_world() populates the world."""
    gen = NarrativeGenerator(seed=42)
    gen.initialize_world()
    assert len(gen.story_world.locations) == 5
    assert len(gen.story_world.characters) == 5
    assert len(gen.story_world.items) == 5


def test_generate_event():
    """generate_event() creates a valid StoryEvent."""
    gen = NarrativeGenerator(seed=1)
    gen.initialize_world()
    event = gen.generate_event("introduction", 0.3)
    assert event.id == "event_0"
    assert isinstance(event.text, str) and len(event.text) > 0
    assert event.tension_level == 0.3


def test_generate_story_structure():
    """generate_story_structure() builds a graph with expected node count."""
    gen = NarrativeGenerator(seed=7)
    gen.initialize_world()
    gen.generate_story_structure(num_branches=2)
    # 1 start + 1 intro + 2 branches * 3 phases = 8 nodes
    assert len(gen.story_graph.nodes()) == 8
    assert len(gen.events) == 7  # intro + 2*3


def test_tell_story_serializable():
    """tell_story() output is JSON-serializable."""
    gen = NarrativeGenerator(seed=99)
    gen.initialize_world()
    gen.generate_story_structure(num_branches=2)
    data = gen.tell_story()
    serialized = json.dumps(data)
    assert isinstance(serialized, str)
    assert "title" in data
    assert "events" in data


def test_num_branches_validation():
    """num_branches < 1 raises ValueError."""
    gen = NarrativeGenerator(seed=0)
    gen.initialize_world()
    try:
        gen.generate_story_structure(num_branches=0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


if __name__ == "__main__":
    test_story_event_creation()
    test_story_world_basics()
    test_initialize_world()
    test_generate_event()
    test_generate_story_structure()
    test_tell_story_serializable()
    test_num_branches_validation()
    print("All story-generator tests passed!")
