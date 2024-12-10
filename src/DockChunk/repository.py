
import logging
import os
from typing import List, Optional
from src.DockChunk.dao import DocChunksDAO
from src.DockChunk.model import DocChunk
from src.stage.dao import SnowflakeStageDAO

class DocRepository:
    def __init__(self):
        self.stage_dao = SnowflakeStageDAO()
        self.chunks_dao = DocChunksDAO()
        self.logger = logging.getLogger(__name__)

    def process_document(self, file_path: str, category: Optional[str] = None) -> bool:
        """Process document: upload and create chunks"""
        try:
            # 1. Upload file to stage
            filename = os.path.basename(file_path)
            if not self.stage_dao.upload_file(file_path):
                return False

            # 2. Get file URLs
            file_url = self.stage_dao.get_file_url(filename)
            scoped_url = self.stage_dao.get_file_url(filename, expiration=1800)  # 30 min
            
            if not file_url or not scoped_url:
                return False

            # 3. Get file size
            file_size = os.path.getsize(file_path)

            # 4. Create chunks (implement your chunking logic here)
            # chunks = create_chunks_from_file(file_path)
            chunks = ["Sample chunk 1", "Sample chunk 2"]  # Replace with actual chunking

            # 5. Create DocChunk objects
            doc_chunks = [
                DocChunk(
                    relative_path=filename,
                    size=file_size,
                    file_url=file_url,
                    scoped_file_url=scoped_url,
                    chunk=chunk,
                    category=category
                ) for chunk in chunks
            ]

            # 6. Save chunks
            return self.chunks_dao.create_chunks(doc_chunks)

        except Exception as e:
            self.logger.error(f"Failed to process document: {str(e)}")
            return False

    def get(self, filename: str) -> List[DocChunk]:
        """Get all chunks for a document"""
        return self.chunks_dao.get_chunks(filename)

    def serch_chunks(self, query: str, category: Optional[str] = None) -> List[DocChunk]:
        """Search chunks by content and optional category"""
        try:
            base_query = """
            SELECT * FROM DOCS_CHUNKS_TABLE
            WHERE CONTAINS(chunk, %s)
            """
            
            if category:
                base_query += " AND category = %s"
                result = self.chunks_dao.execute_query(base_query, (query, category))
            else:
                result = self.chunks_dao.execute_query(base_query, (query,))

            return [DocChunk(**{k.lower(): v for k, v in row.asDict().items()})
                   for row in result]
        except Exception as e:
            self.logger.error(f"Failed to search chunks: {str(e)}")
            return []