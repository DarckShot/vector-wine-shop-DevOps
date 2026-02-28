import pytest
from uuid import uuid4, UUID
from qdrant_client.models import ScoredPoint, Record


from tests.mocks.qdrant_service import create_qdrant_service_mock, create_mock_record
from tests.mocks.model_service import (
    create_model_service_mock,
    create_mock_embedding,
    create_mock_summary
)


@pytest.fixture
def qdrant_service_mock():
    """Переиспользуемая фикстура для мока QdrantService."""
    mock = create_qdrant_service_mock()
    return mock


@pytest.fixture
def mock_qdrant_record():
    """Фикстура для создания мок-записи Qdrant."""
    def _create_mock_record(payload: dict, point_id=None):
        return create_mock_record(payload=payload, point_id=point_id)
    return _create_mock_record


@pytest.fixture
def model_service_mock():
    """Переиспользуемая фикстура для мока ModelService."""
    mock = create_model_service_mock()
    return mock


@pytest.fixture
def mock_embedding():
    """Фикстура для создания мок-эмбеддинга."""
    def _create_embedding(dim: int = 384):
        return create_mock_embedding(dim=dim)
    return _create_embedding


@pytest.fixture
def mock_summary():
    """Фикстура для создания мок-саммаризации."""
    def _create_summary(text: str = "Mock summary"):
        return create_mock_summary(text=text)
    return _create_summary


@pytest.fixture
def wine_id():
    """Фикстура для генерации UUID вина."""
    return uuid4()


# В конце tests/conftest.py

# =============================================================================
# Фикстуры для тестов утилит Qdrant
# =============================================================================

@pytest.fixture
def valid_wine_payload():
    """Базовый валидный payload для модели Wine/WineBase."""
    return {
        "name": "Test Wine",
        "description": "Test description",
        "price": 99.99,
        "color": "red",
        "acidity": "medium",
        "country": "France"
    }


@pytest.fixture
def create_scored_point():
    """Фабрика для создания ScoredPoint."""
    def _create(
        point_id: UUID = None,
        payload: dict = None,
        score: float = 0.9,
        version: int = 1
    ):
        return ScoredPoint(
            id=point_id if point_id else uuid4(),
            payload=payload if payload else {},
            score=score,
            vector=None,
            version=version
        )
    return _create


@pytest.fixture
def create_record():
    """Фабрика для создания Record."""
    def _create(
        point_id: UUID = None,
        payload: dict = None
    ):
        return Record(
            id=point_id if point_id else uuid4(),
            payload=payload if payload else {},
            vector=None
        )
    return _create