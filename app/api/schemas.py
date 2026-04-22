from pydantic import BaseModel
from typing import List

class IndexRequest(BaseModel):
    urls: List[str]

class IndexResponse(BaseModel):
    message: str
    status: str
    chunks_indexed: int

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
