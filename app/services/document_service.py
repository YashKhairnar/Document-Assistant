import bs4
from typing import List, Tuple
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from app.services.embedding_service import embedding_service

class DocumentService:
    """
    Handles the document ingestion pipeline: 
    Fetching -> Splitting -> Indexing.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
        )
        # Initialize an empty vector store bound to our embedding service
        self.vector_store = InMemoryVectorStore(embedding_service)

    def fetch_documents(self, urls: List[str]) -> List:
        """Fetches and parses documents from the provided list of URLs."""
        if not urls:
            return []
        
        # Only keep primary content tags to reduce noise
        loader = WebBaseLoader(
            web_paths=tuple(urls)
        )
        return loader.load()

    def index_urls(self, urls: List[str]) -> int:
        """
        Full ingestion pipeline:
        1. Reset store
        2. Fetch docs
        3. Split into chunks
        4. Add to vector store
        """
        # Clear existing data for a fresh index (as per current design)
        self.vector_store = InMemoryVectorStore(embedding_service)
        
        docs = self.fetch_documents(urls)
        if not docs:
            return 0
            
        all_splits = self.text_splitter.split_documents(docs)
        self.vector_store.add_documents(documents=all_splits)
        return len(all_splits)

# Singleton instance
document_service = DocumentService()
