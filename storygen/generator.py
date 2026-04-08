"""
storygen/generator.py
=====================
NarrativeGenerator -- builds branching story structures.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List, Optional

import networkx as nx
import numpy as np

from .models import StoryEvent
from .visualization import visualize_story_graph
from .world import StoryWorld

# Default data directory for templates
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_templates(path: Optional[Path] = None) -> Dict[str, List[str]]:
    """Load plot-point templates from a JSON file, falling back to defaults."""
    if path is None:
        path = _DATA_DIR / "templates.json"
    if path.is_file():
        with open(path, "r") as f:
            return json.load(f)
    # Hardcoded fallback
    return {
        "introduction": [
            "A mysterious stranger arrives in {location}",
            "An ancient artifact is discovered in {location}",
            "A long-held secret threatens to emerge in {location}",
            "Two unlikely allies meet in {location}",
        ],
        "development": [
            "{character} uncovers a hidden truth about {item}",
            "A conflict erupts between {character} and their allies",
            "An unexpected challenge tests {character}'s resolve",
            "A crucial decision must be made about {item}",
        ],
        "climax": [
            "All secrets are revealed in a dramatic confrontation",
            "The true nature of {item} becomes clear",
            "A final battle determines the fate of {location}",
            "{character} must face their greatest fear",
        ],
        "resolution": [
            "Peace returns to {location}, but at what cost?",
            "The truth about {item} changes everything",
            "{character} emerges transformed by their journey",
            "A new era begins for the people of {location}",
        ],
    }


class NarrativeGenerator:
    """Generates branching narrative structures backed by a directed graph."""

    def __init__(
        self,
        seed: Optional[int] = None,
        templates_path: Optional[Path] = None,
    ) -> None:
        if seed is not None:
            random.seed(seed)
            self._rng = np.random.default_rng(seed)
        else:
            self._rng = np.random.default_rng()

        self.story_world = StoryWorld()
        self.story_graph: nx.DiGraph = nx.DiGraph()
        self.events: Dict[str, StoryEvent] = {}
        self.current_state: Dict = {}
        self.story_history: List = []

        self.themes = [
            "redemption", "discovery", "conflict",
            "transformation", "love", "loss",
        ]
        self.emotions = [
            "joy", "sadness", "anger",
            "fear", "surprise", "anticipation",
        ]
        self.plot_points = _load_templates(templates_path)

    # -- world setup -------------------------------------------------------

    def initialize_world(self) -> None:
        """Populate the story world with default locations, characters, items."""
        for loc in [
            "Ancient Forest", "Crystal Cave", "Hidden Valley",
            "Mystic Temple", "Forgotten City",
        ]:
            self.story_world.add_location(loc)

        characters = [
            "The Seeker", "The Guardian", "The Sage",
            "The Trickster", "The Ally",
        ]
        for char in characters:
            self.story_world.add_character(char)

        for item in [
            "Crystal Key", "Ancient Scroll", "Magic Amulet",
            "Forgotten Sword", "Mystic Map",
        ]:
            self.story_world.add_item(item)

        for c1 in characters:
            for c2 in characters:
                if c1 != c2:
                    rel = float(self._rng.normal(0.5, 0.2))
                    self.story_world.set_relationship(c1, c2, rel)

    # -- event generation --------------------------------------------------

    def generate_event(self, phase: str, tension: float) -> StoryEvent:
        """Create a single story event for the given narrative phase."""
        if phase not in self.plot_points:
            raise ValueError(f"Unknown story phase: {phase}")

        template = random.choice(self.plot_points[phase])
        event_text = template.format(
            location=random.choice(list(self.story_world.locations)),
            character=random.choice(list(self.story_world.characters)),
            item=random.choice(list(self.story_world.items)),
        )

        num_consequences = max(1, int(tension * 3))
        consequences = []
        for _ in range(num_consequences):
            direction = "increase" if random.random() < tension else "decrease"
            consequences.append(f"tension_{direction}_{random.choice(self.themes)}")

        event_id = f"event_{len(self.events)}"
        event = StoryEvent(
            id=event_id,
            text=event_text,
            mood=random.choice(self.emotions),
            consequences=consequences,
            requirements=[],
            tension_level=tension,
        )
        self.events[event_id] = event
        return event

    # -- story structure ---------------------------------------------------

    def generate_story_structure(self, num_branches: int = 3) -> None:
        """Build a branching story graph with *num_branches* paths."""
        if num_branches < 1:
            raise ValueError("num_branches must be >= 1")

        self.story_graph.add_node("start")
        intro_event = self.generate_event("introduction", 0.3)
        self.story_graph.add_edge("start", intro_event.id)

        for _ in range(num_branches):
            current_node = intro_event.id
            tension = 0.3
            for phase in ["development", "climax", "resolution"]:
                tension += 0.2
                new_event = self.generate_event(phase, tension)
                self.story_graph.add_edge(current_node, new_event.id)
                current_node = new_event.id

    def visualize_story_graph(self, filename: str = "story_graph.png", **kwargs) -> None:
        """Render the story graph to an image file."""
        visualize_story_graph(self.story_graph, self.events, filename, **kwargs)

    def tell_story(self) -> Dict:
        """Return a JSON-serialisable dict describing the full story."""
        return {
            "title": (
                f"The {random.choice(self.themes).title()} "
                f"of the {random.choice(list(self.story_world.items))}"
            ),
            "world": {
                "locations": list(self.story_world.locations),
                "characters": list(self.story_world.characters),
                "items": list(self.story_world.items),
            },
            "events": {
                eid: {
                    "text": ev.text,
                    "mood": ev.mood,
                    "tension": ev.tension_level,
                }
                for eid, ev in self.events.items()
            },
            "structure": {
                "nodes": list(self.story_graph.nodes()),
                "edges": list(self.story_graph.edges()),
            },
        }
