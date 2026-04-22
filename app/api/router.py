from fastapi import APIRouter, HTTPException
from app.api.schemas import IndexRequest, IndexResponse, QueryRequest, QueryResponse
from app.services.document_service import document_service
from app.services.rag_service import rag_service

api_router = APIRouter()

@api_router.post("/index", response_model=IndexResponse)
async def index_documents(request: IndexRequest):
    """Refreshes the knowledge base with content from the provided URLs."""
    try:
        count = document_service.index_urls(request.urls)
        # Re-build the agent to use the new vector store if necessary
        rag_service.build_agent()
        return IndexResponse(
            message="Documents indexed successfully",
            status="ready",
            chunks_indexed=count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

@api_router.post("/query", response_model=QueryResponse)
async def query_assistant(request: QueryRequest):
    """Processes a natural language query using the RAG pipeline."""
    # Safety check: ensure indexing has happened
    if not document_service.vector_store:
        raise HTTPException(status_code=400, detail="Knowledge base is empty. Please index some URLs first.")
    
    try:
        answer = await rag_service.answer_query(request.query)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
