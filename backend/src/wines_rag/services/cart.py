
from uuid import UUID
from wines_rag.api.schemas.cart import CartGetResponse, CartPutResponse
from wines_rag.errors import WineNotFoundException
from wines_rag.services.qdrant.client import QdrantService
from wines_rag.services.qdrant.utils import qdrant_points_to_wines

class CartService:
    def __init__(self, qdrant_service: QdrantService):
        self.qdrant_service = qdrant_service
        
    async def add_wine(self,wine_id: UUID)->None:
        point_exists = await self.qdrant_service.point_exists(point_id=wine_id)
        if point_exists:
            await self.qdrant_service.update_point_count(point_id=wine_id,new_count_value=1)
        else:
            raise WineNotFoundException()
        
    async def delete_wine(self,wine_id: UUID)->None:
        point_exists = await self.qdrant_service.point_exists(point_id=wine_id)
        if point_exists:
            await self.qdrant_service.update_point_count(point_id=wine_id,new_count_value=0)
        else:
            raise WineNotFoundException()
    
    async def put_wine(self,wine_id: UUID, wine_count:int)->CartPutResponse:
        point_exists = await self.qdrant_service.point_exists(point_id=wine_id)
        if point_exists:
            is_payload_updated = await self.qdrant_service.update_point_count(point_id=wine_id,new_count_value=wine_count)
            if is_payload_updated:
                point_exists = await self.qdrant_service.point_exists(point_id=wine_id)
                updated_count = point_exists.payload.get("count",0)
                return CartPutResponse(updated_count=updated_count)
        else:
            raise WineNotFoundException()
        
    async def get_wines(self)->CartGetResponse:
        points = await self.qdrant_service.get_available_wines()
        wines = await qdrant_points_to_wines(points=points)
        return CartGetResponse(wines=wines)
        