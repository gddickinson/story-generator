"""
story_generator.py
==================
CLI entry point for the Interactive Story Generator.

Usage:
    python story_generator.py
    python story_generator.py --seed 42 --branches 5 --output-dir output/
    python story_generator.py --theme fantasy
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from storygen import NarrativeGenerator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate branching interactive stories.",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--branches", type=int, default=3,
        help="Number of branching paths (default: 3)",
    )
    parser.add_argument(
        "--output-dir", type=str, default=".",
        help="Directory for output files (default: current directory)",
    )
    parser.add_argument(
        "--theme", type=str, default=None,
        help="Story theme/genre (reserved for future presets)",
    )
    return parser.parse_args()


def generate_and_save_story(
    seed: Optional[int] = None,
    num_branches: int = 3,
    output_dir: str = ".",
) -> None:
    """Generate a complete story and save all outputs."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    generator = NarrativeGenerator(seed)
    generator.initialize_world()
    generator.generate_story_structure(num_branches=num_branches)

    generator.visualize_story_graph(str(out / "story_structure.png"))

    story_data = generator.tell_story()

    with open(out / "story_data.json", "w") as f:
        json.dump(story_data, f, indent=2)

    print(f"\nGenerated Story: {story_data['title']}\n")
    print("Story World:")
    print(f"- Locations: {', '.join(story_data['world']['locations'])}")
    print(f"- Characters: {', '.join(story_data['world']['characters'])}")
    print(f"- Items: {', '.join(story_data['world']['items'])}\n")

    print("Story Events:")
    for event_id, event in story_data["events"].items():
        print(f"\n{event_id}:")
        print(f"- {event['text']}")
        print(f"- Mood: {event['mood']}")
        print(f"- Tension: {event['tension']:.2f}")


if __name__ == "__main__":
    args = parse_args()
    generate_and_save_story(
        seed=args.seed,
        num_branches=args.branches,
        output_dir=args.output_dir,
    )
