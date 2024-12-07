from typing import List
from src.base.dao import BaseDAO
from src.ChatMessage.model import ChatMessage

class ChatMessageDAO(BaseDAO):
    
    def create_table(self):
        """Create chat messages table if not exists"""
        query = """
        CREATE TABLE IF NOT EXISTS CHAT_MESSAGES (
            MESSAGE_ID VARCHAR(36) NOT NULL,
            SESSION_ID VARCHAR(36) NOT NULL,
            ROLE VARCHAR(50) NOT NULL,
            CONTENT TEXT NOT NULL,
            CREATED_AT TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
            PRIMARY KEY (MESSAGE_ID),
            FOREIGN KEY (SESSION_ID) REFERENCES CHAT_SESSIONS(SESSION_ID)
        )
        """
        self.execute_query(query)

    def add(self,record: ChatMessage) -> bool:
        """Create a new chat message"""
        try:
            query = """
            INSERT INTO CHAT_MESSAGES (message_id, session_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?)
            """
            result = self.execute_query(query, (record.message_id, record.session_id, record.role, record.content, record.created_at))
            return result[0].__getitem__('number of rows inserted') > 0
        except Exception as e:
            print(f"Error creating chat message: {e}")
            return None

    def getMessage(self, session_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get messages for a chat session"""
        query = """
        SELECT message_id, session_id, role, content, created_at FROM CHAT_MESSAGES
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """
        result = self.execute_query(query, (session_id, limit))
        return [ChatMessage(
            message_id=row['MESSAGE_ID'],
            session_id=row['SESSION_ID'],
            role=row['ROLE'],
            content=row['CONTENT'],
            created_at=row['CREATED_AT']
        ) for row in result]
