"""
storygen/world.py
=================
StoryWorld -- manages locations, characters, items, and relationships.
"""

from collections import defaultdict
from typing import Iterable, Iterator, MutableSet


class OrderedSet(MutableSet):
    """A set that remembers insertion order.

    Plain sets iterate in an order that depends on string hashing, which Python
    randomises per process; a seeded story must not depend on that.
    """

    def __init__(self, items: Iterable[str] = ()) -> None:
        self._d: dict = dict.fromkeys(items)

    def __contains__(self, x: object) -> bool:
        return x in self._d

    def __iter__(self) -> Iterator[str]:
        return iter(self._d)

    def __len__(self) -> int:
        return len(self._d)

    def add(self, x: str) -> None:
        self._d[x] = None

    def discard(self, x: str) -> None:
        self._d.pop(x, None)

    def __repr__(self) -> str:
        return f"OrderedSet({list(self._d)!r})"


class StoryWorld:
    """Container for story world state: locations, characters, items, relationships."""

    def __init__(self) -> None:
        self.locations: OrderedSet = OrderedSet()
        self.characters: OrderedSet = OrderedSet()
        self.items: OrderedSet = OrderedSet()
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
