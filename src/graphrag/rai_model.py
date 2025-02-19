class RAIModelBuilder:
    def __init__(self, model_name: str, dry_run: bool = False):
        self.model = rai.Model(model_name, dry_run=dry_run)
        self.snowflake_model = Snowflake(self.model)
        
    def build_entity_type(self):
        """Define Entity type"""
        return self.model.Type("Entity", source="graph_rag.graph_rag.nodes")
    
    def build_relation_type(self, entity_type):
        """Define Relation type with src and dst properties"""
        relation = self.model.Type("Relation", source="graph_rag.graph_rag.edges")
        relation.define(
            src=(entity_type, "src_node_id", "id"),
            dst=(entity_type, "dst_node_id", "id")
        )
        return relation