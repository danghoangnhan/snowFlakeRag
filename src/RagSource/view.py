import os
import tempfile
import uuid
import pandas as pd
import streamlit as st

from src.ChatSession.model import ChatSession
from src.RagSource.repository import RagSourceRepository
class RAGFileView:
    def __init__(self, chat_session:ChatSession):
        self.session_file_repo = RagSourceRepository()
        self.chat_session:ChatSession   = chat_session
        

    def render_upload_section(self):
        """Render file upload section"""
        tab1, tab2 = st.tabs(["Upload Files", "Use Web Links"])
        
        with tab1:
            with st.form("upload Form", clear_on_submit=True):
                uploaded_files = st.file_uploader(
                    "Choose PDF files",
                    type=['pdf'],
                    accept_multiple_files=True,
                    key="file_uploader"
                )
                submit = st.form_submit_button("Upload Selected Files", use_container_width=True)
                if submit:
                    meta_data = []
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        temp_dir = os.path.dirname(tmp_file.name)
                        for uploaded_file in uploaded_files:
                                temp_path = os.path.join(temp_dir, uploaded_file.name)
                                
                                # Write file content
                                with open(temp_path, 'wb') as f:
                                    f.write(uploaded_file.getbuffer())
                                meta_data.append(temp_path)
                    print(meta_data)
                    results =  self.session_file_repo.add_files(session_id=self.chat_session.session_id,file_infos=meta_data)
                    # Show results
                    # success_count = sum(1 for r in results if r['success'])
                    # if success_count == len(results):
                    #     st.success(f"Successfully uploaded all {len(results)} files!")
                    # else:
                    #     st.warning(f"Uploaded {success_count} of {len(results)} files successfully.")
                    
                    # Clear the uploader
                    st.rerun()
        
            if uploaded_files:
                if st.button("Upload and Index", use_container_width=True):
                    for file in uploaded_files:
                        # Handle file upload logic here
                        
                        pass

        with tab2:
            st.text_area(
                "Input web URLs",
                help="(separated by new line)",
                height=200
            )

            st.button("Upload and Index", type="primary")

    def render_file_list(self):
        """Render file listing with details"""
        # Filter input
        st.text_area(
            "Filter by name:",
            help="(1) Case-insensitive. (2) Search with empty string to show all files.",
            key="file_filter"
        )
        chunk_counts = self.session_file_repo.get_files(self.chat_session.session_id)
        chunk_counts_df = pd.DataFrame([chunk.to_dict() for chunk in chunk_counts])
        if not chunk_counts_df.empty:
            st.dataframe(
                chunk_counts_df,
                column_config={
                    "relative path": st.column_config.TextColumn("relative_path", width="large"),
                    "chunk_count": st.column_config.NumberColumn(
                        "chunk_count",
                        format="%dKB",
                        width="small"
                    )
                },
                hide_index=True,
                use_container_width=True
            )

            # File actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Download all files", use_container_width=True):
                    # Handle download logic
                    pass
            with col2:
                if st.button("Delete all files", 
                           use_container_width=True,
                           type="secondary",
                           help="This will delete all files in the current session"):
                    if self.session_file_repo.remove(self.chat_session.session_id):
                        st.success("All files deleted successfully")
                        st.rerun()
                    else:
                        st.error("Failed to delete files")
        else:
            st.info("No files found. Upload some files to get started.")


    def render(self):
        """Main render method"""
        # Tab selection
        tab1, tab2 = st.tabs(["Files", "Groups"])
        
        with tab1:
            self.render_upload_section()
            st.divider()
            self.render_file_list()

        with tab2:
            st.info("Groups functionality coming soon...")