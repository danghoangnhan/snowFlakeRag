from typing import List
from dotenv import load_dotenv
from docChunk import DocChunksRepository, DocChunk
from rag import RAG_from_scratch
from stage import StageManager
import streamlit as st # Import python packages
import pandas as pd
from connector import SnowflakeConnector

pd.set_option("max_colwidth",None)

load_dotenv('envs/dev.env')  # Load environment variables from .env file

connector = SnowflakeConnector()
connector.connect()
dockChunkRepository = DocChunksRepository(connector=connector)
stage_manager       = StageManager(connector, "docs")
ragService          = RAG_from_scratch(connector=connector)
   
### Functions
     
def config_options():
    categories:List[DocChunk] = dockChunkRepository.list_all()
    cat_list = ['ALL']
    for cat in categories:
        cat_list.append(cat)
    st.sidebar.selectbox('Select what products you are looking for', cat_list, key = "category_value")
    st.sidebar.checkbox('Do you want that I remember the chat history?', key="use_chat_history", value = True)
    st.sidebar.checkbox('Debug: Click to see summary generated of previous conversation', key="debug", value = True)
    st.sidebar.button("Start Over", key="clear_conversation", on_click=init_messages)
    st.sidebar.expander("Session State").write(st.session_state)
    docs_available = stage_manager.list_files()
    st.sidebar.dataframe(docs_available)

def init_messages():

    # Initialize chat history
    if st.session_state.clear_conversation or "messages" not in st.session_state:
        st.session_state.messages = []


def get_chat_history(slide_window:int = 7):    
    chat_history = []
    start_index = max(0, len(st.session_state.messages) - slide_window)
    for i in range (start_index , len(st.session_state.messages) -1):
         chat_history.append(st.session_state.messages[i])

    return chat_history

def answer_question(question):
    respone, relative_paths =ragService.query(
        query = question,
        history_chat =  get_chat_history()
    )
    return respone, relative_paths

def main():
    
    st.title(f":speech_balloon: Chat Document Assistant with Snowflake Cortex")
    st.write("This is the list of documents you already have and that will be used to answer your questions:")
    config_options()
    init_messages()

     
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if question := st.chat_input("What do you want to know about your products?"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
    
            question = question.replace("'","")
    
            with st.spinner(f"model  thinking..."):
                response, relative_paths = answer_question(question)       
                if relative_paths  is not None:
                    with st.sidebar.expander("Related Documents"):
                        for path in relative_paths:
                            cmd2 = f"select GET_PRESIGNED_URL(@docs, '{path}', 360) as URL_LINK from directory(@docs)"
                            connector.connect()
                            df_url_link = connector.session.sql(cmd2).to_pandas()
                            url_link = df_url_link._get_value(0,'URL_LINK')
                            display_url = f"Doc: [{path}]({url_link})"
                            st.sidebar.markdown(display_url)
                message_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()