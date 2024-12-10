import logging
import os
from typing import List, Dict
from src.ChatSession.dao import ChatSessionDAO
from src.DockChunk.dao import DocChunksDAO
from src.DockChunk.model import ChunkCount
from src.RagSource.model import RagSource
from src.RagSource.dao import RagSourceDAO, SessionFileDAO
from src.ChatMessage.dao import ChatMessageDAO
from src.stage.dao import SnowflakeStageDAO
from src.stage.repository import StageRepository

class RagSourceRepository:
    """Repository layer for managing RAG sources"""
    
    def __init__(self):
        self.rag_source_dao = RagSourceDAO()
        self.chat_message_dao = ChatMessageDAO()

        self.session_dao = ChatSessionDAO()
        self.session_file_dao = SessionFileDAO()
        self.stage_dao =  SnowflakeStageDAO()
        self.chunk_repo = DocChunksDAO()
        self.logger = logging.getLogger(__name__)

    def get_sources(self, session_id: str) -> List[ChunkCount]:
        """
        Get all sources grouped by message for a chat session
        
        Args:
            session_id: ID of the chat session
            
        Returns:
            Dictionary mapping message IDs to lists of RagSource objects
        """
        try:
            
            return self.chunk_repo.get_file_statistic(session_id)
        except Exception as e:
            print(f"Error getting session sources: {e}")
            return {}

    def add_files(self, session_id: str, file_infos: List[Dict]) -> Dict[str, bool]:
        """Add multiple files to a session"""
        results = {}
        for file_info in file_infos:
            if not os.path.exists(file_info['path']):
                self.logger.warning(f"File not found: {file_info['path']}")
                results[file_info['name']] = False
                continue
            if  not self.stage_dao.upload_file(file_info['path']):
                results[file_info['name']] = False
                continue
            if  not self.session_file_dao.add(session_id, file_info['name']):
                results['name'] = False
                continue
            results['name'] = True
        return results

    def get_session_with_files(self, session_id: str) -> Dict:
        """Get session info with its files"""
        session = self.session_dao.get_by_id(session_id)
        if not session:
            return {}

        files_df = self.session_file_dao.get_files_details(session_id)
        
        return {
            'session': session,
            'files': files_df
        }
    def get_files(self,session_id: str) -> List[str]:
        return self.session_file_dao.get_session_files(session_id=session_id)