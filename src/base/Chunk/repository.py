# src/chunk/repository.py
from typing import List, Dict, Optional
from src.base.Chunk.dao import ChunkDAO
from src.base.Chunk.model import DocumentChunk
from src.stage.repository import StageRepository

class ChunkRepository:
    def __init__(self):
        self.chunk_dao = ChunkDAO()
        self.stage_repo = StageRepository()

    def create_document_chunks(self, path: str, chunks: List[str], category: Optional[str] = None) -> bool:
        """Create chunks for a document"""
        try:
            # Get file info from stage
            file_info = self.stage_repo.get_file_info(path)
            if not file_info:
                return False

            # Get file URL
            file_url = self.stage_repo.get_file_url(path)
            scoped_url = self.stage_repo.get_file_url(path, expiration=1800)  # 30 min expiration

            # Create chunk objects
            doc_chunks = [
                DocumentChunk(
                    relative_path=path,
                    size=file_info.size,
                    file_url=file_url,
                    scoped_file_url=scoped_url,
                    chunk=chunk,
                    category=category
                ) for chunk in chunks
            ]

            return self.chunk_dao.create_chunks(doc_chunks)
            
        except Exception as e:
            self.logger.error(f"Failed to create document chunks: {str(e)}")
            return False

    def get_document_chunks(self, path: str) -> List[DocumentChunk]:
        """Get all chunks for a document"""
        return self.chunk_dao.get_chunks(path)

    def get_chunks_by_category(self, category: str) -> List[DocumentChunk]:
        """Get chunks by category"""
        return self.chunk_dao.find_by_category(category)

    def delete_document(self, path: str) -> bool:
        """Delete document chunks and optionally the file"""
        # First delete chunks
        chunks_deleted = self.chunk_dao.delete_document_chunks(path)
        
        # Optionally delete from stage
        # self.stage_repo.remove_files([path])
        
        return chunks_deleted

    def search_chunks(self, query: str, category: Optional[str] = None) -> List[DocumentChunk]:
        """Search through chunks"""
        try:
            base_query = """
            SELECT * FROM DOCS_CHUNKS_TABLE
            WHERE chunk LIKE %s
            """
            
            params = [f"%{query}%"]
            if category:
                base_query += " AND category = %s"
                params.append(category)

            result = self.chunk_dao.execute_query(base_query, tuple(params))
            return [DocumentChunk(**{k.lower(): v for k, v in row.asDict().items()})
                   for row in result]
                   
        except Exception as e:
            self.logger.error(f"Failed to search chunks: {str(e)}")
            return []

    def get_document_statistics(self, path: str) -> Dict:
        """Get statistics for a document's chunks"""
        chunks = self.get_document_chunks(path)
        if not chunks:
            return {
                'chunk_count': 0,
                'total_size': 0,
                'avg_chunk_length': 0
            }

        return {
            'chunk_count': len(chunks),
            'total_size': chunks[0].size,
            'avg_chunk_length': sum(len(chunk.chunk) for chunk in chunks) / len(chunks)
        }

# Example usage:
"""
# Initialize repository
chunk_repo = ChunkRepository()

# Create chunks for a document
chunks = ["chunk1 content", "chunk2 content", "chunk3 content"]
success = chunk_repo.create_document_chunks(
    path="docs/example.pdf",
    chunks=chunks,
    category="Technical"
)

# Get document chunks
doc_chunks = chunk_repo.get_document_chunks("docs/example.pdf")

# Search chunks
results = chunk_repo.search_chunks("specific content", category="Technical")

# Get statistics
stats = chunk_repo.get_document_statistics("docs/example.pdf")
"""