from typing import Optional

from qdrant_client.models import FieldCondition, Filter, Range, ScoredPoint
from wines_rag.entities.qdrant import WineBase

async def make_qdrant_filters(
    price_min: Optional[float] = None,
    price_max: Optional[float] = None
) -> Optional[Filter]:

    conditions = []

    if price_min is not None:
        conditions.append(
            FieldCondition(
                key="price",  
                range=Range(gte=price_min)
            )
        )
    if price_max is not None:
        conditions.append(
            FieldCondition(
                key="price",
                range=Range(lte=price_max)
            )
        )  

    return Filter(must=conditions)

async def qdrant_points_to_wines_chunks(points:list[ScoredPoint])->list[WineBase]:
    chunks = []
    for point in points:
        payload = point.payload
        if not payload:
            continue
        filtered_payload = {k: v for k, v in payload.items() if k != 'count'}
        chunk = WineBase(**filtered_payload,id=point.id)
        chunks.append(chunk)
    return chunks