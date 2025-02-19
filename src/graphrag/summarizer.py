from typing import Dict, List
import pandas as pd


class CommunitySummarizer:
    def __init__(self, snowflake_session):
        self.session = snowflake_session
        self.logger = logging.getLogger(__name__)

    def summarize_communities(self, communities_df: pd.DataFrame):
        """Generate summaries for communities"""
        # Convert DataFrame to community dictionary
        community_dict = self._prepare_community_data(communities_df)
        
        # Clear existing summaries
        self._truncate_summary_table()
        
        # Generate new summaries
        for community_id, corpus_ids in community_dict.items():
            self._summarize_community(community_id, corpus_ids)

    def _prepare_community_data(self, df: pd.DataFrame) -> Dict:
        communities_count_df = df.groupby(
            by=["community_id", "corpus_id"]
        ).count().rename(
            columns={"id": "entities_count"}
        ).sort_index()

        index = communities_count_df.index.to_flat_index()
        community_dict = {}
        for x, y in index:
            community_dict.setdefault(x, []).append(y)
        return community_dict

    def _truncate_summary_table(self):
        self.session.execute_statement(
            "TRUNCATE TABLE community_summary"
        )

    def _summarize_community(self, community_id: int, corpus_ids: List[str]):
        corpus_ids_str = ", ".join([str(i) for i in corpus_ids])
        self.logger.info(f"Summarizing IDs ({corpus_ids_str}) for community {community_id}")
        
        try:
            self._execute_summary_query(community_id, corpus_ids_str)
        except Exception as error:
            self.logger.error(
                f"Error summarizing IDs ({corpus_ids_str}) for community {community_id}: {str(error)}"
            )

    def _execute_summary_query(self, community_id: int, corpus_ids: str):
        query = """
        INSERT INTO community_summary(COMMUNITY_ID, CONTENT)
        WITH c AS (
            SELECT 
                LISTAGG(content, '\n\n') WITHIN GROUP(ORDER BY id) AS content
            FROM 
                CORPUS
            WHERE 
                id IN ({CORPUS_IDS})
        )
        SELECT 
            {COMMUNITY_ID} AS community_id,
            PARSE_JSON(LLM_EXTRACT_JSON(r.response)):answer AS response
        FROM 
            c
        JOIN TABLE(LLM_SUMMARIZE('llama3-70b', c.content)) AS r
        """
        
        self.session.execute_statement(
            query,
            parameters={
                "COMMUNITY_ID": str(community_id),
                "CORPUS_IDS": corpus_ids
            }
        )