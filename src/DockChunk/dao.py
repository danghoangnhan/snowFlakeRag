
# src/doc_chunks/dao.py
from typing import List
from src.DockChunk.model import ChunkCount, DocChunk
from src.base.dao import BaseDAO

class DocChunksDAO(BaseDAO):
    def create(self, chunks: List[DocChunk]) -> bool:
        """Batch insert document chunks"""
        try:
            if not chunks:
                return True

            query = """
            INSERT INTO DOCS_CHUNKS_TABLE (
                relative_path, size, file_url, 
                scoped_file_url, chunk, category
            ) VALUES (?, ?, ?, ?, ?, ?)
            """
            
            for chunk in chunks:
                self.execute_query(query, (
                    chunk.relative_path,
                    chunk.size,
                    chunk.file_url,
                    chunk.scoped_file_url,
                    chunk.chunk,
                    chunk.category
                ))
            return True
        except Exception as e:
            self.logger.error(f"Failed to create chunks: {str(e)}")
            return False

    def get(self, relative_path: str) -> List[DocChunk]:
        """Get all chunks for a document"""
        try:
            query = """
            SELECT * FROM DOCS_CHUNKS_TABLE
            WHERE relative_path = ?
            """
            result = self.execute_query(query, (relative_path,))
            return [DocChunk(**{k.lower(): v for k, v in row.asDict().items()})
                   for row in result]
        except Exception as e:
            self.logger.error(f"Failed to get chunks: {str(e)}")
            return []

    def get_file_statistic(self, session_id: str) -> List[ChunkCount]:
        """Get chunk counts for files in a specific session"""
        try:
            query = """
            SELECT 
                dc.RELATIVE_PATH,
                SUM (DC.SIZE) as CHUNK_COUNT
            FROM DOCS_CHUNKS_TABLE dc
            JOIN SESSION_FILE sf 
                ON dc.RELATIVE_PATH = sf.file_name
            WHERE sf.session_id = ?
            GROUP BY dc.RELATIVE_PATH
            """
            result = self.execute_query(query, (session_id,))
            return [
                ChunkCount(
                    relative_path=row['RELATIVE_PATH'],
                    chunk_count=row['CHUNK_COUNT']
                )
                for row in result
            ]
        except Exception as e:
            self.logger.error(f"Failed to get chunk counts: {str(e)}")
            return []

    def delete_by_file(self, relative_path: str) -> bool:
        """Delete all chunks for a specific file path"""
        try:
            query = """
            DELETE FROM DOCS_CHUNKS_TABLE
            WHERE RELATIVE_PATH = ?
            """
            self.execute_query(query, (relative_path,))
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete chunks for file {relative_path}: {str(e)}")
            return False

    def delete_by_session(self, session_id: str) -> bool:
        """Delete all chunks for files in a session"""
        try:
            query = """
            DELETE FROM DOCS_CHUNKS_TABLE
            WHERE RELATIVE_PATH IN (
                SELECT file_name 
                FROM SESSION_FILE_MAPPING 
                WHERE session_id = ?
            )
            """
            self.execute_query(query, (session_id,))
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete chunks for session {session_id}: {str(e)}")
            return False