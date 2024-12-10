from dataclasses import dataclass
from typing import List, Optional
from snowflake.cortex import Complete
from trulens.apps.custom import instrument
from snowflake.core import Root
from src.base.connector import SnowflakeConnector, get_resource_manager

@dataclass 
class SearchResult:
   context_text: List[str]
   relative_paths: set[str]


def generate_filter(column_name: str, array: list[str]):
    """
    Generate a filter with OR conditions for array of values
    """
    return {
        "@or": [
            {"@eq": {column_name: element}} 
            for element in array
        ]
    }
class CortexSearchRetriever:
    def __init__(self, connector: SnowflakeConnector, file_list:List[str],limit_to_retrieve: int = 4):
        self._session = connector.session
        self._limit_to_retrieve = limit_to_retrieve
        self.COLUMNS                = ["chunk","relative_path","category"]
        self.CORTEX_SEARCH_DATABASE = "cortex_search_db"
        self.CORTEX_SEARCH_SCHEMA   = "DATA"
        self.CORTEX_SEARCH_SERVICE  = "CC_SEARCH_SERVICE_CS"
        self.file_list = file_list


    def retrieve(self, query: str)-> SearchResult:
        service = (Root(self._session)
                 .databases[self.CORTEX_SEARCH_DATABASE]
                 .schemas[self.CORTEX_SEARCH_SCHEMA]
                 .cortex_search_services[self.CORTEX_SEARCH_SERVICE])
        

        if not self.file_list:
            return SearchResult([], set())
        
        filters = generate_filter("RELATIVE_PATH", self.file_list)
        resp = service.search(
           query=query,
           columns=self.COLUMNS,
           limit=self._limit_to_retrieve,
           filter=filters
       )
        if not resp.results:
           return SearchResult([], set())

        return SearchResult(
           context_text=[r["chunk"] for r in resp.results],
           relative_paths=set(r['relative_path'] for r in resp.results)
       )

class RAG_from_scratch:
    def __init__(self,model_name:str = "mistral-large2",file_list:List[str]=[]):
        self.connector    =   get_resource_manager()

        self.retriever = CortexSearchRetriever(
            connector=self.connector,
            limit_to_retrieve=4,
            file_list=file_list
        )
        self.model_name =   model_name
        
    @instrument
    def retrieve_context(self, query: str) -> SearchResult:
        """
        Retrieve relevant text from vector store.
        """
        return self.retriever.retrieve(query)


    @instrument
    def generate_completion(self, query: str, context: List[str]) -> str:
       prompt = f"""
       You are an expert assistant extracting information from context provided.
       Answer the question based on the context.
       Be concise and do not hallucinate.
       If you don´t have the information just say so.           
       Do not mention the CONTEXT used in your answer.
       Do not mention the CHAT HISTORY used in your answer.
       Only answer the question if you can extract it from the CONTEXT provided.
       
       Context: {context}
       Query: {query}
       Answer:"""

       return Complete(
           model=self.model_name,
           prompt=prompt,
           session=self.connector.session
       )
    
    @instrument
    def summarize(self, chat_history: List[str], query: str) -> str:
        prompt = f"""
        Based on the chat history below and the query, generate a query that extends the query with the chat history provided.
        The query should be in natural language. 
        Answer with only the query.
        Do not add any explanation.
        Chat history: {chat_history}
        Query: {query}"""

        return Complete(
            model=self.model_name,
            prompt=prompt,
            session=self.connector.session
        )

    @instrument
    def query(
        self, 
        query: str, 
        history_chat: Optional[List[str]] = None,
    ) -> tuple[str, set]:
        if history_chat:
            query = self.summarize(history_chat, query)
            
        result = self.retrieve_context(
            query=query
        )
        
        response = self.generate_completion(query, result.context_text)
        return response, result.relative_paths
# def create_prompt (question:str,use_chat_history:bool):

#     if use_chat_history:
#         chat_history = get_chat_history()

#         if chat_history != []:
#             question    =   summarize_question_with_history(
#                 model_name      = st.session_state.model_name,
#                 chat_history    = chat_history,
#                 question        =  question
#             )
#             question =    summary()
#             if st.session_state.debug:
#                 st.sidebar.text("Summary to be used to find similar chunks in the docs:")
#                 st.sidebar.caption(sumary)
#     ragService.generate_completion()
#     prompt_context = get_similar_chunks_search_service(
#         query = question,
#         category_value = st.session_state.category_value
#     )
#     chat_history = ""
  
#     prompt = f"""
#            You are an expert chat assistance that extracs information from the CONTEXT provided
#            between <context> and </context> tags.
#            You offer a chat experience considering the information included in the CHAT HISTORY
#            provided between <chat_history> and </chat_history> tags..
#            When ansering the question contained between <question> and </question> tags
#            be concise and do not hallucinate. 
#            If you don´t have the information just say so.
           
#            Do not mention the CONTEXT used in your answer.
#            Do not mention the CHAT HISTORY used in your asnwer.

#            Only anwer the question if you can extract it from the CONTEXT provideed.
           
#            <chat_history>
#            {chat_history}
#            </chat_history>
#            <context>          
#            {prompt_context}
#            </context>
#            <question>  
#            {question}
#            </question>
#            Answer: 
#            """
#     json_data = json.loads(prompt_context)

#     relative_paths = set(item['relative_path'] for item in json_data['results'])

#     return prompt, relative_paths
# Example usage:
if __name__ == "__main__":
    rag = RAG_from_scratch()