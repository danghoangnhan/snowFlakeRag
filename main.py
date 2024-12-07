from dotenv import load_dotenv
import streamlit as st

from src.ChatSession.view import ChatSessionView
from src.ChatMessage.view import ChatMessageView

def render_sidebar():
    """Render chat sidebar"""
    st.sidebar.checkbox(
        'Remember chat history',
        key="use_chat_history",
        value=True
    )
    st.sidebar.checkbox(
        'Debug mode',
        key="debug",
        value=False
    )
    if st.sidebar.button("← Back to Dashboard"):
        st.session_state.current_chat = None
        st.rerun()

init_state={
    "current_chat": None
}     

def main():
    load_dotenv('envs/dev.env')
    st.set_page_config(page_title="NotebookLM Clone", layout="wide")
    
    dashboard = ChatSessionView()

    for key,value in init_state.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state.current_chat is not None:
        chat = ChatMessageView(st.session_state.current_chat)
        chat.render()
    else:
        dashboard.render()

if __name__ == "__main__":
    main()