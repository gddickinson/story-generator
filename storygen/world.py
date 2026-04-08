"""
storygen/world.py
=================
StoryWorld -- manages locations, characters, items, and relationships.
"""

from collections import defaultdict


class StoryWorld:
    """Container for story world state: locations, characters, items, relationships."""

    def __init__(self) -> None:
        self.locations: set[str] = set()
        self.characters: set[str] = set()
        self.items: set[str] = set()
        self.relationships: dict[str, dict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        self.state: dict = {}

    def add_location(self, location: str) -> None:
        self.locations.add(location)

    def add_character(self, character: str) -> None:
        self.characters.add(character)

    def add_item(self, item: str) -> None:
        self.items.add(item)

    def set_relationship(self, char1: str, char2: str, value: float) -> None:
        self.relationships[char1][char2] = value
        self.relationships[char2][char1] = value
