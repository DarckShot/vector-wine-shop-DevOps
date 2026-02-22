from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from wines_rag.entities.qdrant import WineBase

class ChatSearchWinesRequest(BaseModel):
    query: str
    price_min: Optional[float]=Field(default=None,ge=0,le=100000)
    price_max:  Optional[float]=Field(default=None,ge=1,le=100000)
    model_config = ConfigDict(alias_generator=to_camel,from_attributes=True,populate_by_name=True)
    
class ChatSearchWinesResponse(BaseModel):
    wines: list[WineBase]
    summary: str