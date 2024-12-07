from dotenv import load_dotenv
import streamlit as st

from src.ChatSession.model import ChatSession
from src.ChatSession.view import ChatSessionView
from src.ChatMessage.view import ChatMessageView
from src.RagSource.view import  FileView

def render_sidebar(sessionChat:ChatSession):
    """Render chat sidebar"""
    # Project navigation
    st.sidebar.subheader("Project Navigation")
                
    if st.sidebar.button("💬 Chat Sessions", use_container_width=True):
        st.session_state.current_view = "chat"
        st.rerun()
                
    if st.sidebar.button("🔍 RAG Interface", use_container_width=True):
        st.session_state.current_view = "rag"
        st.rerun()
    
    if st.sidebar.button("← Back to Dashboard",use_container_width=True):
        st.session_state.current_chat = None
        st.rerun()
    st.sidebar.divider()


init_state={
    "current_chat": None,
    "current_view": None
}     

def main():
    load_dotenv('envs/dev.env')
    st.set_page_config(page_title="NotebookLM Clone", layout="wide")
    
    dashboard = ChatSessionView()

    for key,value in init_state.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state.current_chat is not None:
        render_sidebar(st.session_state.current_chat)
        if st.session_state.current_view == 'chat':
            chat = ChatMessageView(st.session_state.current_chat)
            chat.render()
        if st.session_state.current_view == 'rag':
            # chat = FileRagView(st.session_state.current_chat)
            # chat.render()
            file_view = FileView()
            file_view.render()
    else:
        dashboard.render()

if __name__ == "__main__":
    main()