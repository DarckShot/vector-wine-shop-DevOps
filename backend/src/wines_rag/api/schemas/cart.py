from pydantic import BaseModel
from uuid import UUID
from typing import Literal


class CartPutRequest(BaseModel):
    count: int


class CartPutResponse(BaseModel):
    updatedCount: int


class Wine(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    color: Literal["red", "white"]
    acidity: Literal["dry", "semi-dry", "semi-sweet", "sweet"]
    country: str
    count: int


class CartGetResponse(BaseModel):
    wines: list[Wine]
