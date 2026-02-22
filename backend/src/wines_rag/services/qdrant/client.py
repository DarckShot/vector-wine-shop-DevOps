

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Document, Fusion, FusionQuery, Prefetch, ScoredPoint
from wines_rag.config import Config
from wines_rag.entities.qdrant import QueryPointsSearch



class QdrantService:
    def __init__(self, config: Config):
        self.client = AsyncQdrantClient(
            url = config.qdrant.url,
            api_key=config.qdrant.api_key
        )
        self.collection_name = config.qdrant.collection_name
        
    async def close(self):
        await self.client.close()
        
        
    async def query_search(self,query_points_search:QueryPointsSearch)->list[ScoredPoint]:
        nearest = await self.client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                Prefetch(
                    query=query_points_search.embed_query,
                    using="dense_vector",
                    limit=query_points_search.top_k*2,
                    score_threshold=query_points_search.score_threshold,
                    filter=query_points_search.filters
                ),
                Prefetch(
                    query=Document(text=query_points_search.query,model="qdrant/bm25"),
                    using="bm25",
                    limit=query_points_search.top_k*2,
                    score_threshold=query_points_search.score_threshold,
                    filter=query_points_search.filters
                ),
                      ],
            query = FusionQuery(fusion=Fusion.DBSF),
            score_threshold=query_points_search.score_threshold,
            limit=query_points_search.top_k
            
            )
        points = nearest.points
        return points
        
          