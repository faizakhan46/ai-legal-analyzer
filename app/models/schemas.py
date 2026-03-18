from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., description="The query string to be processed.")
    top_k: int = Field(5, description="The number of top results to return.")       

class QueryResponse(BaseModel):
    results: list = Field(..., description="A list of results returned from the query.")    
class UploadResponse(BaseModel):
    message: str = Field(..., description="A message indicating the result of the upload operation.")   
    
class ComparisonRequest(BaseModel):
    query: str = Field(..., description="The query string to be compared.")
    top_k: int = Field(5, description="The number of top results to return for comparison.")