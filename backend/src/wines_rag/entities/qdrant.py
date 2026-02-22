from pydantic import BaseModel
from typing import Optional,Literal
from uuid import UUID
from qdrant_client.models import Filter

class QueryPointsSearch(BaseModel):
    query: str
    top_k: Optional[int] = 5
    score_threshold: Optional[float]=0.5
    filters: Filter
    embed_query: list[float]
    

class WineBase(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    color: str
    acidity: str
    # color: Literal["red", "white"]
    # acidity: Literal["dry", "semi-dry", "semi-sweet", "sweet"]
    country: str
    
