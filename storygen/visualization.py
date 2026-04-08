"""
storygen/visualization.py
=========================
Story graph visualization using matplotlib and networkx.
"""

from typing import Dict

import matplotlib.pyplot as plt
import networkx as nx

from .models import StoryEvent


def visualize_story_graph(
    graph: nx.DiGraph,
    events: Dict[str, StoryEvent],
    filename: str = "story_graph.png",
    node_color: str = "lightblue",
    edge_color: str = "gray",
) -> None:
    """Render the story graph to a PNG file.

    Args:
        graph:      The directed story graph.
        events:     Mapping of event_id -> StoryEvent.
        filename:   Output file path.
        node_color: Fill colour for nodes.
        edge_color: Colour for edges.
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)

    nx.draw_networkx_nodes(
        graph, pos, node_size=2000, node_color=node_color, alpha=0.6
    )
    nx.draw_networkx_edges(
        graph, pos, edge_color=edge_color, arrows=True, arrowsize=20
    )

    labels = {}
    for node in graph.nodes():
        if node == "start":
            labels[node] = "Story Start"
        else:
            event = events[node]
            labels[node] = f"{event.text[:30]}..."

    nx.draw_networkx_labels(
        graph, pos, labels, font_size=8,
        font_weight="bold", font_family="sans-serif",
    )

    plt.title("Interactive Story Structure")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
