class CommunityDetector:
    def __init__(self, model, graph):
        self.model = model
        self.graph = graph

    def compute_louvain(self, 
                       max_levels: int = 5, 
                       max_sweeps: int = 10,
                       level_tolerance: float = 1e-2,
                       sweep_tolerance: float = 1e-4):
        """Compute Louvain communities"""
        with self.model.rule():
            entity = self.model.Entity()
            community_id = self.graph.compute.louvain(
                node=entity,
                max_levels=max_levels,
                max_sweeps=max_sweeps,
                level_tolerance=level_tolerance,
                sweep_tolerance=sweep_tolerance
            )
            entity.set(community_id=community_id)