from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from app.services.document_service import document_service
from app.core.config import settings

class RAGService:
    """
    Handles the inference pipeline:
    Query -> Retrieval Tool -> LLM -> Answer.
    """
    def __init__(self):
        # Initialize the LLM (model name comes from config or environment)
        self.llm = init_chat_model("google_genai:gemini-2.5-flash-lite")
        self.agent = None

    def _create_retrieval_tool(self):
        """Creates a tool that pulls context from the current vector store."""
        @tool(response_format="content_and_artifact")
        def retrieve_context(query: str):
            """Retrieve relevant context from the knowledge base to answer a query."""
            retrieved_docs = document_service.vector_store.similarity_search(query)
            serialized = "\n\n".join(
                (f"Source: {doc.metadata}\nContent: {doc.page_content}")
                for doc in retrieved_docs
            )
            return serialized, retrieved_docs
        return retrieve_context

    def build_agent(self):
        """Orchestrates tools and LLM into a conversational agent."""
        tools = [self._create_retrieval_tool()]
        
        system_prompt = (
            "You are a professional assistant. "
            "Use the provided retrieval tool to search for context from documentation URLs. "
            "If the retrieved context lacks sufficient information, honestly state that you don't know. "
            "Do not hallucinate or make up information. "
            "Give examples if asked. Also include code examples if needed."
            "Maintain a helpful, concise, and professional tone. Don't use markdown formatting."
            "If the user asks for code, provide the code in a code block."
            "Provide sources for the information you provide."
        )
        
        self.agent = create_react_agent(self.llm, tools, prompt=system_prompt)

    async def answer_query(self, query: str):
        """Executes the RAG pipeline for a given query."""
        if not self.agent:
            self.build_agent()
            
        try:
            response = self.agent.invoke(
                {"messages": [{"role": "user", "content": query}]}
            )
            return response["messages"][-1].content
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Singleton instance
rag_service = RAGService()
