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
from src.stage.model import StageFile
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

    def add_files(self, session_id: str, file_infos: List[str]) -> Dict[str, bool]:
        """Add multiple files to a session"""
        results = {}
        for file_info in file_infos:
            if not os.path.exists(file_info):
                self.logger.warning(f"File not found: {file_info}")
                results[file_info['name']] = False
                continue
            if  not self.stage_dao.upload_file(file_info,session_id):
                results[file_info['name']] = False
                continue
            results['name'] = True
        return results
    
    def get_files(self,session_id: str) -> List[StageFile]:
        result =  self.stage_dao.get_stage_files(dir=session_id)
        
        return result
    def remove_file(self,session_id: str,file_name:str):
        return self.stage_dao.remove_file(dir_name=session_id,file_name=file_name)

    def remove_dir(self,session_id: str):
        return self.stage_dao.remove_dir(dir_name=session_id)
    
    