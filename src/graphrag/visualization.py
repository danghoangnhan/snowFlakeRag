from typing import Dict

class GraphVisualizer:
    def __init__(self, graph):
        self.graph = graph

    def get_random_color_map(self, communities_length: int) -> Dict:
        """Generate random colors for communities"""
        # Implementation of color map generation
        pass

    def create_visualization(self, three: bool = False, graph_height: int = 1000):
        """Create graph visualization"""
        community_color_map = self.get_random_color_map(200)
        
        return self.graph.visualize(
            three=three,
            graph_height=graph_height,
            show_node_label=True,
            show_edge_label=True,
            style=self._get_visualization_style(community_color_map)
        )

    def _get_visualization_style(self, color_map: Dict) -> Dict:
        return {
            "node": {
                "label": lambda n: f"{n.get('id')} ({n.get('type')})",
                "color": lambda n: color_map.get(n["community_id"], "black"),
                "size": 30,
                "hover": lambda n: f"{n.get('id')} (type: {n.get('type')}, community: {n.get('community_id')})"
            },
            "edge": {
                "label": lambda e: e.get("type"),
                "color": "grey",
                "hover": lambda e: e.get("type")
            }
        }