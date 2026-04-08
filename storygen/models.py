"""
storygen/models.py
==================
Data models for story elements.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class StoryEvent:
    """A single narrative event in the story graph."""
    id: str
    text: str
    mood: str
    consequences: List[str]
    requirements: List[str]
    tension_level: float
