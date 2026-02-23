from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from wines_rag.entities.qdrant import WineBase


class CartPutRequest(BaseModel):
    count: int = Field(ge=1, le=1000)


class CartPutResponse(BaseModel):
    updated_count: int
    model_config = ConfigDict(
        alias_generator=to_camel, from_attributes=True, populate_by_name=True
    )


class Wine(WineBase):
    count: int


class CartGetResponse(BaseModel):
    wines: list[Wine]
