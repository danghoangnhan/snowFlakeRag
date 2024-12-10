# src/chunk/dao.py
from typing import List
import logging
from src.base.Chunk.model import DocumentChunk
from src.base.dao import BaseDAO

class ChunkDAO(BaseDAO):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def create_chunks(self, chunks: List[DocumentChunk]) -> bool:
        """Batch insert document chunks"""
        try:
            if not chunks:
                return True

            query = """
            INSERT INTO DOCS_CHUNKS_TABLE (
                relative_path, size, file_url, 
                scoped_file_url, chunk, category
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            values = [(
                chunk.relative_path,
                chunk.size,
                chunk.file_url,
                chunk.scoped_file_url,
                chunk.chunk,
                chunk.category
            ) for chunk in chunks]
            
            for value in values:
                self.execute_query(query, value)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create chunks: {str(e)}")
            return False

    def get_chunks(self, relative_path: str) -> List[DocumentChunk]:
        """Get all chunks for a document"""
        try:
            query = """
            SELECT * FROM DOCS_CHUNKS_TABLE
            WHERE relative_path = %s
            """
            result = self.execute_query(query, (relative_path,))
            return [DocumentChunk(**{k.lower(): v for k, v in row.asDict().items()})
                   for row in result]
        except Exception as e:
            self.logger.error(f"Failed to get chunks: {str(e)}")
            return []

    def find_by_category(self, category: str) -> List[DocumentChunk]:
        """Find chunks by category"""
        try:
            query = """
            SELECT * FROM DOCS_CHUNKS_TABLE
            WHERE category = %s
            """
            result = self.execute_query(query, (category,))
            return [DocumentChunk(**{k.lower(): v for k, v in row.asDict().items()})
                   for row in result]
        except Exception as e:
            self.logger.error(f"Failed to find chunks by category: {str(e)}")
            return []

    def delete_document_chunks(self, relative_path: str) -> bool:
        """Delete all chunks for a document"""
        try:
            query = """
            DELETE FROM DOCS_CHUNKS_TABLE
            WHERE relative_path = %s
            """
            self.execute_query(query, (relative_path,))
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete chunks: {str(e)}")
            return False