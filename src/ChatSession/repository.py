from typing import Dict, List, Optional

from src.ChatMessage.dao import ChatMessageDAO
from src.ChatSession.dao import ChatSessionDAO
from src.ChatSession.model import ChatSession
from RagSource.dao import RagSourceDAO
from src.ChatMessage.model import ChatMessage
class ChatRepository:
    """Repository class to coordinate DAO operations"""
    def __init__(self):
        
        self.session_dao = ChatSessionDAO()
        self.message_dao = ChatMessageDAO()
        self.source_dao  = RagSourceDAO()

    def create_chat_session(self, record:ChatSession) -> bool:
        """Create a new chat session with just a title"""
        return self.session_dao.create(record)

    def get_all(self, active_only: bool = True) -> List[ChatSession]:
        return self.session_dao.get_all(active_only=active_only)

    def add_message(self, record:ChatMessage) -> bool:
        """Add message with associated RAG sources"""
        return self.message_dao.add(record)
        

    def get_session_statistics(self, session_id: str) -> Dict:
        """Get comprehensive session statistics"""
        query = """
        SELECT 
            COUNT(DISTINCT m.message_id) as message_count,
            COUNT(DISTINCT rs.document_path) as unique_sources,
            AVG(rs.relevance_score) as avg_relevance,
            MAX(m.created_at) as last_message
        FROM CHAT_APP.CHAT_SESSIONS s
        LEFT JOIN CHAT_APP.CHAT_MESSAGES m ON s.session_id = m.session_id
        LEFT JOIN CHAT_APP.RAG_SOURCES rs ON m.message_id = rs.message_id
        WHERE s.session_id = %s
        GROUP BY s.session_id
        """
        result = self.session_dao.execute_query(query, (session_id,))
        return result[0] if result else {}
    
    def getMessage(self, session_id: str, limit: int = 50)->List[ChatMessage]:
        return self.message_dao.getMessage(session_id,limit)

    def delete(self, session_id: str) -> bool:
        return self.session_dao.delete(session_id)