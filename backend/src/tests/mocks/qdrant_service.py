from unittest.mock import AsyncMock
from typing import Optional
from uuid import UUID

from qdrant_client.models import Record


def create_qdrant_service_mock() -> AsyncMock:
    """
    Создаёт переиспользуемый мок для QdrantService.
    """
    mock = AsyncMock()
    mock.__class__.__name__ = "QdrantService"

    mock.point_exists = AsyncMock()
    mock.update_point_count = AsyncMock()
    mock.get_available_wines = AsyncMock()
    mock.query_search = AsyncMock()
    mock.close = AsyncMock()

    return mock


def create_mock_record(payload: dict, point_id: Optional[UUID] = None) -> Record:
    """
    Создаёт реальный объект Record для имитации ответа от Qdrant.
    """
    return Record(
        id=point_id if point_id else UUID(int=0),
        payload=payload,
        vector=None
    )