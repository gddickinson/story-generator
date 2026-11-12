import random
from dataclasses import dataclass
from typing import List, Dict, Set, Optional
import json
import numpy as np
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class StoryEvent:
    id: str
    text: str
    mood: str
    consequences: List[str]
    requirements: List[str]
    tension_level: float
    
class StoryWorld:
    def __init__(self):
        self.locations = set()
        self.characters = set()
        self.items = set()
        self.relationships = defaultdict(lambda: defaultdict(float))
        self.state = {}
        
    def add_location(self, location: str):
        self.locations.add(location)
        
    def add_character(self, character: str):
        self.characters.add(character)
        
    def add_item(self, item: str):
        self.items.add(item)
        
    def set_relationship(self, char1: str, char2: str, value: float):
        self.relationships[char1][char2] = value
        self.relationships[char2][char1] = value

class NarrativeGenerator:
    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
            np.random.seed(seed)
            
        self.story_world = StoryWorld()
        self.story_graph = nx.DiGraph()
        self.events = {}
        self.current_state = {}
        self.story_history = []
        
        # Initialize narrative elements
        self.themes = ["redemption", "discovery", "conflict", "transformation", "love", "loss"]
        self.emotions = ["joy", "sadness", "anger", "fear", "surprise", "anticipation"]
        self.plot_points = self._initialize_plot_points()
        
    def _initialize_plot_points(self) -> Dict[str, List[str]]:
        """Initialize basic plot structures"""
        return {
            "introduction": [
                "A mysterious stranger arrives in {location}",
                "An ancient artifact is discovered in {location}",
                "A long-held secret threatens to emerge in {location}",
                "Two unlikely allies meet in {location}"
            ],
            "development": [
                "{character} uncovers a hidden truth about {item}",
                "A conflict erupts between {character} and their allies",
                "An unexpected challenge tests {character}'s resolve",
                "A crucial decision must be made about {item}"
            ],
            "climax": [
                "All secrets are revealed in a dramatic confrontation",
                "The true nature of {item} becomes clear",
                "A final battle determines the fate of {location}",
                "{character} must face their greatest fear"
            ],
            "resolution": [
                "Peace returns to {location}, but at what cost?",
                "The truth about {item} changes everything",
                "{character} emerges transformed by their journey",
                "A new era begins for the people of {location}"
            ]
        }
    
    def initialize_world(self):
        """Initialize a rich story world"""
        # Add locations
        locations = ["Ancient Forest", "Crystal Cave", "Hidden Valley", "Mystic Temple", "Forgotten City"]
        for loc in locations:
            self.story_world.add_location(loc)
            
        # Add characters
        characters = ["The Seeker", "The Guardian", "The Sage", "The Trickster", "The Ally"]
        for char in characters:
            self.story_world.add_character(char)
            
        # Add items
        items = ["Crystal Key", "Ancient Scroll", "Magic Amulet", "Forgotten Sword", "Mystic Map"]
        for item in items:
            self.story_world.add_item(item)
            
        # Initialize relationships
        for char1 in characters:
            for char2 in characters:
                if char1 != char2:
                    relationship = np.random.normal(0.5, 0.2)
                    self.story_world.set_relationship(char1, char2, relationship)
    
    def generate_event(self, phase: str, tension: float) -> StoryEvent:
        """Generate a new story event based on current state"""
        # Select template based on phase
        template = random.choice(self.plot_points[phase])
        
        # Fill in template with world elements
        event_text = template.format(
            location=random.choice(list(self.story_world.locations)),
            character=random.choice(list(self.story_world.characters)),
            item=random.choice(list(self.story_world.items))
        )
        
        # Generate consequences based on tension
        num_consequences = max(1, int(tension * 3))
        consequences = []
        for _ in range(num_consequences):
            if random.random() < tension:
                consequences.append(f"tension_increase_{random.choice(self.themes)}")
            else:
                consequences.append(f"tension_decrease_{random.choice(self.themes)}")
        
        # Create event
        event_id = f"event_{len(self.events)}"
        event = StoryEvent(
            id=event_id,
            text=event_text,
            mood=random.choice(self.emotions),
            consequences=consequences,
            requirements=[],
            tension_level=tension
        )
        
        self.events[event_id] = event
        return event
    
    def generate_story_structure(self, num_branches: int = 3) -> None:
        """Generate a branching story structure"""
        # Initialize story graph with start node
        self.story_graph.add_node("start")
        
        # Generate introduction
        intro_event = self.generate_event("introduction", 0.3)
        self.story_graph.add_edge("start", intro_event.id)
        
        # Generate branching paths
        for _ in range(num_branches):
            current_node = intro_event.id
            tension = 0.3
            
            # Generate development events
            for phase in ["development", "climax", "resolution"]:
                tension += 0.2
                new_event = self.generate_event(phase, tension)
                self.story_graph.add_edge(current_node, new_event.id)
                current_node = new_event.id
    
    def visualize_story_graph(self, filename: str = "story_graph.png"):
        """Visualize the story graph structure"""
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.story_graph)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.story_graph, pos, node_size=2000, 
                             node_color='lightblue', alpha=0.6)
        
        # Draw edges
        nx.draw_networkx_edges(self.story_graph, pos, edge_color='gray', 
                             arrows=True, arrowsize=20)
        
        # Draw labels
        labels = {}
        for node in self.story_graph.nodes():
            if node == "start":
                labels[node] = "Story Start"
            else:
                event = self.events[node]
                labels[node] = f"{event.text[:30]}..."
        
        nx.draw_networkx_labels(self.story_graph, pos, labels, font_size=8,
                              font_weight='bold', font_family='sans-serif')
        
        plt.title("Interactive Story Structure")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def tell_story(self) -> Dict:
        """Generate and return the complete story structure"""
        story_data = {
            "title": f"The {random.choice(self.themes).title()} of the {random.choice(list(self.story_world.items))}",
            "world": {
                "locations": list(self.story_world.locations),
                "characters": list(self.story_world.characters),
                "items": list(self.story_world.items)
            },
            "events": {event_id: {
                "text": event.text,
                "mood": event.mood,
                "tension": event.tension_level
            } for event_id, event in self.events.items()},
            "structure": {
                "nodes": list(self.story_graph.nodes()),
                "edges": list(self.story_graph.edges())
            }
        }
        return story_data

def generate_and_save_story(seed: Optional[int] = None) -> None:
    """Generate a complete story and save all outputs"""
    # Create generator
    generator = NarrativeGenerator(seed)
    
    # Initialize and generate story
    generator.initialize_world()
    generator.generate_story_structure(num_branches=3)
    
    # Generate visualization
    generator.visualize_story_graph("story_structure.png")
    
    # Generate complete story
    story_data = generator.tell_story()
    
    # Save story data
    with open("story_data.json", "w") as f:
        json.dump(story_data, f, indent=2)
    
    # Print story overview
    print(f"\nGenerated Story: {story_data['title']}\n")
    print("Story World:")
    print(f"- Locations: {', '.join(story_data['world']['locations'])}")
    print(f"- Characters: {', '.join(story_data['world']['characters'])}")
    print(f"- Items: {', '.join(story_data['world']['items'])}\n")
    
    print("Story Events:")
    for event_id, event in story_data['events'].items():
        print(f"\n{event_id}:")
        print(f"- {event['text']}")
        print(f"- Mood: {event['mood']}")
        print(f"- Tension: {event['tension']:.2f}")

if __name__ == "__main__":
    generate_and_save_story(seed=42)  # Use seed for reproducibility
