import uuid
import streamlit as st
from datetime import datetime

from src.ChatSession.model import ChatSession
from src.ChatSession.repository import ChatRepository

init_state = {
    'creating_new' : False,
    'editing_block': None,
    'delete_confirmation' : None,
}

class ChatSessionView:
    def __init__(self):
        self.chat_repo = ChatRepository()
        st.session_state.chat_history = self.chat_repo.get_all()
        
        for key,value in init_state.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def show_create_form(self):
        """Display create new block form"""
        st.markdown("""
            <div style="
                background: rgba(60,60,60,0.9);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0;
            ">
                <h3>Create New Notebook</h3>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form(key="create_block_form"):
            title = st.text_input("Notebook Name", "New Notebook")
            # icon = st.selectbox("Select Icon", list(self.icons.values()))
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button("Create")
            with col2:
                cancel = st.form_submit_button("Cancel")
        if submit:  
            if not title.strip():
                st.error("Chat title cannot be empty")
                return 
            current_time = datetime.now()
            # Create ChatSession object
            newChat = ChatSession(
                session_id=str(uuid.uuid4()),
                title=title,
                created_at=current_time,
                updated_at=current_time,
                is_active=True
            )
            if self.chat_repo.create_chat_session(record=newChat):
                st.session_state.chat_history.append(newChat)
                st.success(f"Chat '{title}' created successfully!")
            else:
                st.error("Failed to create chat. Please try again.")

                st.session_state.creating_new = False
                st.rerun()
        
        if cancel:
            st.session_state.creating_new = False
            st.rerun()

    def render(self):
        st.title("Welcome to NotebookLM")
        st.subheader("My Notebooks")
        
        # Add Create New button and sort options
        col1, col2, col3 = st.columns([2, 8, 2])
        with col1:
            if st.button("➕ Create new"):
                st.session_state.creating_new = True
                st.rerun()

        with col3:
            st.selectbox("Sort by", ["Most recent", "Oldest", "Title"], key="sort_option")
        
        # Show create form if creating_new is True
        if st.session_state.creating_new:
            self.show_create_form()
            return

        # Display chat cards in a grid
        if st.session_state.chat_history:
            cols = st.columns(3)
            for idx, chat in enumerate(st.session_state.chat_history):
                with cols[idx % 3]:
                    self.create_chat_card(chat)
        else:
            st.markdown("""
                <div style="text-align: center; padding: 50px;">
                    <h3>No notebooks found</h3>
                    <p>Create a new notebook to get started!</p>
                </div>
            """, unsafe_allow_html=True)

    def create_chat_card(self, chat: ChatSession):
        with st.container():
            # Show delete confirmation if this is the chat being deleted
            if st.session_state.delete_confirmation == chat.session_id:
                self.show_delete_confirmation(chat)
                return

            # Card header with menu
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(45deg, rgba(60,60,60,0.9), rgba(40,40,40,0.9));
                        padding: 20px;
                        border-radius: 15px;
                        margin: 10px 0;
                        cursor: pointer;
                    ">
                        # <div style="font-size: 24px; margin-bottom: 5px;">
                         {chat.title}
                        # </div>
                        <div style="color: #888; font-size: 14px;">
                            {chat.created_at.strftime('%b %d, %Y')} - last updated:{chat.updated_at.strftime('%b %d, %Y')} 
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                option = st.selectbox(
                    "",
                    ["Edit", "Delete"],
                    key=f"menu_{chat.session_id}",
                    label_visibility="collapsed"
                )
                
                if option == "Delete":
                    st.session_state.delete_confirmation = chat.session_id
                    st.rerun()

            # Make the card clickable
            if st.button("Open Chat", key=f"btn_{chat.session_id}", use_container_width=True):
                st.session_state.current_chat = chat
                st.rerun()

    def show_delete_confirmation(self, chat: ChatSession):
        """Show delete confirmation dialog"""
        st.markdown(
            f"""
            <div style="
                background: rgba(255, 0, 0, 0.1);
                padding: 20px;
                border-radius: 10px;
                border: 1px solid red;
                margin: 10px 0;
            ">
                <h3>Delete Confirmation</h3>
                <p>Are you sure you want to delete "{chat.title}"?</p>
                <p>This action cannot be undone.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("❌ Cancel", key=f"cancel_delete_{chat.session_id}"):
                st.session_state.delete_confirmation = None
                st.rerun()
        with col2:
            if st.button("🗑️ Delete", key=f"confirm_delete_{chat.session_id}", type="primary"):
                self.chat_repo.delete(chat.session_id)
                st.session_state.chat_history.remove(chat)
                st.session_state.delete_confirmation = None
                st.rerun()

def main():
    st.set_page_config(page_title="NotebookLM Clone", layout="wide")
    
    # Apply custom CSS
    st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        .stButton button {
            background-color: #3D3D3D;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
        }
        .stButton button[data-baseweb="button"] {
            background-color: #FF4B4B;
        }
        .stSelectbox {
            background-color: #3D3D3D;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    dashboard = ChatSessionView()
    dashboard.render()

if __name__ == "__main__":
    main()