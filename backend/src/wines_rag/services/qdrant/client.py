from typing import Optional
from uuid import UUID

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    FieldCondition,
    Filter,
    Range,
    Record,
    ScoredPoint,
)
from wines_rag.config import Config
from wines_rag.entities.qdrant import QueryPointsSearch


class QdrantService:
    def __init__(self, config: Config):
        self.client = AsyncQdrantClient(
            url=config.qdrant.url, api_key=config.qdrant.api_key
        )
        self.collection_name = config.qdrant.collection_name

    async def close(self):
        await self.client.close()

    async def get_available_wines(self, limit: int = 1000) -> list[Record]:
        filter = Filter(must=[FieldCondition(key="count", range=Range(gt=0))])
        points, _ = await self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=filter,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )
        return points

    async def point_exists(self, point_id: UUID) -> Optional[Record]:
        points = await self.client.retrieve(
            collection_name=self.collection_name,
            ids=[point_id],
            with_payload=True,
            with_vectors=False,
        )
        return points[0] if len(points) > 0 else None

    async def update_point_count(self, point_id: UUID, new_count_value: int) -> bool:
        try:
            await self.client.set_payload(
                collection_name=self.collection_name,
                payload={"count": new_count_value},
                points=[point_id],
            )
            return True
        except Exception as e:
            print(f"Error updating payload for point {point_id}: {e}")
            return False

    async def query_search(
        self, query_points_search: QueryPointsSearch
    ) -> list[ScoredPoint]:
        nearest = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_points_search.embed_query,
            using="dense_vector",
            limit=query_points_search.top_k,
            score_threshold=query_points_search.score_threshold,
            query_filter=query_points_search.filters,
            with_payload=True,
        )
        return nearest.points
