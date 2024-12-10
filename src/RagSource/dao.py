from typing import List, Optional, Dict
import uuid

import pandas as pd
from src.RagSource.model import RagSource
from src.base.dao import BaseDAO

class RagSourceDAO(BaseDAO):
    
    def create(self, session_id: str, document_path: str, relevance_score: float) -> Optional[RagSource]:
        """Create a new RAG source"""
        try:
            source_id = str(uuid.uuid4())
            query = """
            INSERT INTO RAG_SOURCES 
            (source_id, message_id, document_path, relevance_score)
            VALUES (?, ?, ?, ?)
            """
            result = self.execute_query(
                query,
                (source_id, session_id, document_path, relevance_score)
            )
            # Update sources count in session
            self.execute_query("""
                UPDATE CHAT_SESSIONS s
                SET sources_count = (
                    SELECT COUNT(DISTINCT rs.document_path)
                    FROM CHAT_APP.CHAT_MESSAGES cm
                    JOIN CHAT_APP.RAG_SOURCES rs ON cm.message_id = rs.message_id
                    WHERE cm.session_id = s.session_id
                )
                WHERE session_id = (
                    SELECT session_id 
                    FROM CHAT_MESSAGES 
                    WHERE message_id = ?
                )
            """, (message_id,))
            
            return RagSource(**result[0]) if result else None
        except Exception as e:
            print(f"Error creating RAG source: {e}")
            return None

    def get_by_session_id(self, session_id: str) -> List[RagSource]:
        """Get RAG sources for a message"""
        query = """
        SELECT * FROM RAG_SOURCES
        WHERE message_id = ?
        ORDER BY relevance_score DESC
        """
        result = self.execute_query(query, (session_id,))
        return [RagSource(**row) for row in result]

class SessionFileDAO(BaseDAO):
    def add(self, session_id: str, file_path: str) -> bool:
        """Link a file to a session"""
        try:
            query = """
            INSERT INTO SESSION_FILE (
                session_id, 
                file_name,
                created_at
            )
            VALUES (
                ?,
                ?,
                CURRENT_TIMESTAMP()
            )
            """
            self.execute_query(query, (session_id, file_path))
            return True
        except Exception as e:
            self.logger.error(f"Failed to add file to session: {str(e)}")
            return False

    def get_session_files(self, session_id: str) -> List[str]:
        """Get all files for a session"""
        try:
            query = """
            SELECT file_name 
            FROM SESSION_FILE
            WHERE session_id = ?
            """
            result = self.execute_query(query, (session_id,))
            return [row['FILE_NAME'] for row in result]
        except Exception as e:
            self.logger.error(f"Failed to get session files: {str(e)}")
            return []
    
    def remove_file(self, file_path: str) -> bool:
        """Unlink a session"""
        try:
            query = """
            DELETE FROM SESSION_FILES
            WHERE file_path = ?
            """
            self.execute_query(query, (file_path))
            return True
        except Exception as e:
            self.logger.error(f"Failed to remove file from session: {str(e)}")
            return False
        
    def get_files_details(self, session_id: str) -> pd.DataFrame:
        """Get detailed file information for a session"""
        try:
            query = """
            SELECT 
                sf.file_path as Name,
                sf.created_at as "Date Added",
                directory.size/1024 as Size,
                8 as Tokens,
                'PDFThumbnailReader' as Loader
            FROM SESSION_FILES sf
            JOIN DIRECTORY(@docs) directory
            ON sf.file_path = directory.name
            WHERE sf.session_id = ?
            ORDER BY sf.created_at DESC
            """
            result = self.execute_query(query, (session_id,))
            df = pd.DataFrame(result)
            
            if not df.empty:
                df['Size'] = df['Size'].apply(lambda x: f"{x:.0f}KB")
                df['Tokens'] = df['Tokens'].apply(lambda x: f"{x}K")
            
            return df
        except Exception as e:
            self.logger.error(f"Failed to get files details: {str(e)}")
            return pd.DataFrame()

