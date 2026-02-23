from uuid import UUID

from fastapi import APIRouter, Response
from wines_rag.api.dependencies import CartDep
from wines_rag.api.schemas.cart import CartGetResponse, CartPutRequest, CartPutResponse

router = APIRouter(prefix="/cart")


@router.post("/wines/{wine_id}")
async def add_wine(wine_id: UUID, cart_service: CartDep) -> Response:
    await cart_service.add_wine(wine_id=wine_id)
    return Response(status_code=201)


@router.delete("/wines/{wine_id}")
async def delete_wine(wine_id: UUID, cart_service: CartDep) -> Response:
    await cart_service.delete_wine(wine_id=wine_id)
    return Response(status_code=204)


@router.put("/wines/{wine_id}", response_model=CartPutResponse)
async def put_wine(
    wine_id: UUID, put_request: CartPutRequest, cart_service: CartDep
) -> CartPutResponse:
    result = await cart_service.put_wine(wine_id=wine_id, wine_count=put_request.count)
    return result


@router.get("/wines", response_model=CartGetResponse)
async def get_wines(cart_service: CartDep) -> CartGetResponse:
    result = await cart_service.get_wines()
    return result
