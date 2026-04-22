from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from app.core.config import settings
from typing import List

class EmbeddingModel(Embeddings):
    """
    Production-grade wrapper for sentence-transformers.
    Implements LangChain's Embeddings interface.
    """
    def __init__(self, model_name: str = None):
        name = model_name or settings.EMBEDDING_MODEL_NAME
        self.model = SentenceTransformer(name)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Convert numpy arrays to list for LangChain compatibility
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        embedding = self.model.encode([text])[0]
        return embedding.tolist()

# Singleton instance for the app
embedding_service = EmbeddingModel()
