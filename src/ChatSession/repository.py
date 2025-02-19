from typing import Dict, List, Optional

from src.ChatMessage.dao import ChatMessageDAO
from src.ChatSession.dao import ChatSessionDAO
from src.ChatSession.model import ChatSession
from src.RagSource.dao import RagSourceDAO, SessionFileDAO
from src.ChatMessage.model import ChatMessage
from stage.dao import SnowflakeStageDAO

class ChatRepository:
    """Repository class to coordinate DAO operations"""
    def __init__(self):
        
        self.session_dao = ChatSessionDAO()
        self.message_dao = ChatMessageDAO()
        self.source_dao  = RagSourceDAO()
        self.session_file_dao = SessionFileDAO()
        self.stag_dao = SnowflakeStageDAO()
    

    def create_chat_session(self, record:ChatSession) -> bool:
        """Create a new chat session with just a title"""
        return self.session_dao.create(record)

    def get_all(self, active_only: bool = True) -> List[ChatSession]:
        return self.session_dao.get_all(active_only=active_only)

    def add_message(self, record:ChatMessage) -> bool:
        """Add message with associated RAG sources"""
        return self.message_dao.add(record)
        
    def get_session_statistics(self, session_id: str) -> Dict:
        return self.session_dao.get_session_statistics(session_id,)
    
    def getMessage(self, session_id: str, limit: int = 50)->List[ChatMessage]:
        return self.message_dao.getMessage(session_id,limit)

    def delete(self, session_id: str) -> bool:
        if(not self.stag_dao.remove_dir(dir_name=session_id)):
            return False
        if(not self.session_file_dao.delete_by_session_id(session_id=session_id)):
            return False
        if(not self.message_dao.delete_by_session(session_id=session_id)):
            return False        
        return self.session_dao.delete(session_id)