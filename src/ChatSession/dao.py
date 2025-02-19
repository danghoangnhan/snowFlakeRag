from typing import List, Optional, Dict
import uuid
from src.ChatSession.model import ChatSession
from src.base.dao import BaseDAO

class ChatSessionDAO(BaseDAO):
    def create(self, record:ChatSession) -> bool:
        """Create a new chat session"""
        try:
            
            query = """
            INSERT INTO CHAT_SESSIONS (session_id, title)
            VALUES (?, ?)
            """
            result = self.execute_query(query, [record.session_id, record.title])
            return result[0].__getitem__('number of rows inserted') > 0
        except Exception as e:
            print(f"Error creating chat session: {e}")
            return None

    def get_all(self, active_only: bool = True) -> List[ChatSession]:
        """Get all chat sessions"""
        query = """
        SELECT * FROM CHAT_SESSIONS
        WHERE (is_active = ?)
        ORDER BY updated_at DESC
        """
        result = self.execute_query(query, (active_only,))
        return [ChatSession(
                    session_id= row['SESSION_ID'],
                    title= row['TITLE'],
                    created_at= row['CREATED_AT'],
                    updated_at= row['UPDATED_AT'],
                    is_active= row['IS_ACTIVE']
                ) for row in result]


    def get_by_id(self, session_id: str) -> Optional[ChatSession]:
        """Get chat session by ID"""
        query = """
        SELECT * FROM CHAT_APP.CHAT_SESSIONS
        WHERE session_id = %s AND is_active = TRUE
        """
        result = self.execute_query(query, (session_id,))
        return ChatSession(**result[0]) if result else None

    def update(self, session_id: str, title: str = None, category: str = None) -> bool:
        """Update chat session"""
        updates = []
        params = []
        if title:
            updates.append("title = %s")
            params.append(title)
        if category:
            updates.append("category = %s")
            params.append(category)
        
        if not updates:
            return False

        query = f"""
        UPDATE CHAT_APP.CHAT_SESSIONS
        SET {", ".join(updates)}, updated_at = CURRENT_TIMESTAMP()
        WHERE session_id = %s
        """
        params.append(session_id)
        self.execute_query(query, tuple(params))
        return True

    def delete(self, session_id: str) -> bool:
        """Soft delete chat session"""
        query = """
        UPDATE CHAT_SESSIONS
        SET is_active = FALSE
        WHERE session_id = ?
        """
        self.execute_query(query, (session_id,))
        return True

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
        self.execute_query(query, (session_id,))
        return True