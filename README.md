# Interactive Story Generator

A Python-based procedural narrative generation system that creates branching interactive stories with rich world-building and character relationships.

## Features

- **Procedural Story Generation**: Creates unique, branching narratives with multiple possible paths
- **Rich World Building**: Generates detailed story worlds with:
  - Dynamic locations
  - Complex characters
  - Meaningful items
  - Character relationships
- **Story Structure**: Implements proper narrative structure with:
  - Introduction
  - Development
  - Climax
  - Resolution
- **Visual Representation**: Generates visual graph representations of story structures
- **JSON Output**: Saves complete story data in structured JSON format
- **Customizable Parameters**: Adjust story complexity, themes, and branching factors

## Installation

1. Clone this repository:
```bash
git clone [your-repo-url]
cd interactive-story-generator
```

2. Install required dependencies:
```bash
pip install numpy networkx matplotlib
```

## Usage

### Basic Usage

Run the generator with default settings:

```python
python story_generator.py
```

This will:
1. Generate a new story
2. Create a visualization (saved as `story_structure.png`)
3. Save story data (as `story_data.json`)
4. Print a story overview to the console

### Custom Story Generation

You can also use the generator programmatically:

```python
from story_generator import generate_and_save_story

# Generate a story with a specific seed for reproducibility
generate_and_save_story(seed=42)

# Or generate a random story
generate_and_save_story()
```

### Customizing the Generator

The `NarrativeGenerator` class can be customized:

```python
from story_generator import NarrativeGenerator

# Create a generator with custom settings
generator = NarrativeGenerator(seed=42)

# Initialize world
generator.initialize_world()

# Generate story with more branches
generator.generate_story_structure(num_branches=5)

# Generate visualizations and data
generator.visualize_story_graph("custom_story.png")
story_data = generator.tell_story()
```

## Output Files

The generator creates two main output files:

1. `story_structure.png`: A visual representation of the story's branching structure
2. `story_data.json`: Complete story data including:
   - Story title
   - World details (locations, characters, items)
   - Event descriptions
   - Story structure
   - Character relationships

## Story Elements

### World Building
- **Locations**: Dynamic settings where story events take place
- **Characters**: Story actors with relationships and motivations
- **Items**: Important objects that influence the narrative
- **Relationships**: Dynamic connections between characters

### Narrative Elements
- **Themes**: Including redemption, discovery, conflict, transformation, love, loss
- **Emotions**: Joy, sadness, anger, fear, surprise, anticipation
- **Plot Points**: Structured story events with consequences
- **Tension Levels**: Dynamic story tension that evolves through the narrative

## Customization

### Modifying Story Elements

You can customize the story elements by modifying the initialization data:

```python
generator = NarrativeGenerator()

# Add custom locations
generator.story_world.add_location("Crystal Palace")

# Add custom characters
generator.story_world.add_character("The Mystic")

# Add custom items
generator.story_world.add_item("Ancient Tome")
```

### Adjusting Story Structure

Modify the branching factor and complexity:

```python
# Generate more complex stories
generator.generate_story_structure(num_branches=5)
```

## Contributing

Contributions are welcome! Some areas for potential enhancement:

- Additional plot structures
- More complex character relationships
- Enhanced world-building mechanics
- Improved narrative coherence
- New visualization options
- Custom theme support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using NetworkX for graph visualization
- Inspired by narrative theory and procedural generation techniques
- Uses matplotlib for visualization generation
