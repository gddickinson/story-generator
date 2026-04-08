"""
storygen - Interactive Story Generator
======================================

A branching narrative generator using graph structures.

Submodules:
    models        - StoryEvent dataclass
    world         - StoryWorld (locations, characters, items, relationships)
    generator     - NarrativeGenerator (event/story creation, graph building)
    visualization - Story graph rendering to PNG
"""

from .models import StoryEvent
from .world import StoryWorld
from .generator import NarrativeGenerator

__all__ = ["StoryEvent", "StoryWorld", "NarrativeGenerator"]
