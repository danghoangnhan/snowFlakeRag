from datetime import datetime
from typing import List, Optional, Tuple
import uuid
import streamlit as st

from src.ChatMessage.model import ChatMessage
from src.ChatSession.model import ChatSession
from src.ChatSession.repository import ChatRepository
from src.base.stage import StageManager
from src.base.rag import RAG_from_scratch

class ChatHistoryManager:
    def __init__(self,data:List[ChatMessage],slide_window:int):
        self.chat_history:List[ChatMessage]   = data
        self.slide_window:int = slide_window

    def push(self,data:ChatMessage):
        self.chat_history.append(data)
    
    def get(self) -> List[ChatMessage]:        
        start_index = max(0, len(self.chat_history) - self.slide_window)
        return self.chat_history[start_index:-1]

class ChatMessageView:
    def __init__(self, chat_session:ChatSession,slide_window: int = 7):
        self.chat_session:ChatSession   = chat_session
        self.rag_service                = RAG_from_scratch()
        self.stage_manager              = StageManager("docs")
        self.chat_repo                  = self.chat_repo = ChatRepository()
        self.chat_history               = ChatHistoryManager(
        data=self.chat_repo.getMessage(chat_session.session_id,limit=slide_window),slide_window=7)

    def answer_question(self, question: str) -> Tuple[str, Optional[List[str]]]:
        """Process question through RAG service"""
        return self.rag_service.query(
            query=question,
            history_chat=self.chat_history.get()
        )

    def display_related_documents(self, relative_paths: List[str]):
        """Display related documents in sidebar"""
        if relative_paths:
            with st.sidebar.expander("Related Documents"):
                for path in relative_paths:
                    cmd = f"select GET_PRESIGNED_URL(@docs, '{path}', 360) as URL_LINK from directory(@docs)"
                    self.connector.connect()
                    df_url_link = self.connector.session.sql(cmd).to_pandas()
                    url_link = df_url_link._get_value(0, 'URL_LINK')
                    st.sidebar.markdown(f"Doc: [{path}]({url_link})")



    def render(self):
        """Render chat interface"""
        st.title(f"💬 {self.chat_session.title}")
        
        for message in self.chat_history.chat_history:
            with st.chat_message(message.role):
                st.markdown(message.content)
        
        if question := st.chat_input("What would you like to know?"):            
            # Add user message
            userQuestion = ChatMessage(
                session_id=self.chat_session.session_id,
                message_id=str(uuid.uuid4()),
                role="user",
                content= question.replace("'", ""),
                created_at=datetime.now()
            )
            if self.chat_repo.add_message(userQuestion):
                self.chat_history.push(userQuestion)
            
                with st.chat_message("user"):
                    st.markdown(userQuestion.content)
            
                # Generate response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    
                    with st.spinner("Thinking..."):
                        response, relative_paths = self.answer_question(question)
                        
                        
                        modelRespone = ChatMessage(
                            session_id=self.chat_session.session_id,
                            message_id=str(uuid.uuid4()),
                            role="assistant",
                            content= response,
                            created_at=datetime.now()
                        )
                        if self.chat_repo.add_message(modelRespone):
                            self.chat_history.push(modelRespone)
                            message_placeholder.markdown(response)
                        

