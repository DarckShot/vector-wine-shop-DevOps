from wines_rag.api.schemas.chat import ChatSearchWinesRequest, ChatSearchWinesResponse
from wines_rag.entities.qdrant import QueryPointsSearch
from wines_rag.services.model import ModelService
from wines_rag.services.qdrant.client import QdrantService
from wines_rag.services.qdrant.utils import (
    make_qdrant_filters,
    qdrant_scored_points_to_wines,
)


class ChatService:
    def __init__(self, qdrant_service: QdrantService, model: ModelService):
        self.qdrant_service = qdrant_service
        self.model = model

    async def search_wines(
        self, search_request: ChatSearchWinesRequest
    ) -> ChatSearchWinesResponse:
        cleaned_query = search_request.query.replace("вино", "")
        embed_query = await self.model.encode(text=cleaned_query)
        filters = await make_qdrant_filters(
            price_max=search_request.price_max, price_min=search_request.price_min
        )
        points = await self.qdrant_service.query_search(
            QueryPointsSearch(
                query=cleaned_query, filters=filters, embed_query=embed_query
            )
        )
        wines = await qdrant_scored_points_to_wines(points=points)
        summary = await self.model.summarize_wines(
            query=search_request.query, wines=wines
        )
        return ChatSearchWinesResponse(wines=wines, summary=summary)
