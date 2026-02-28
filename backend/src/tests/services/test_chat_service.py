import pytest
from uuid import uuid4, UUID

from qdrant_client.models import ScoredPoint

from wines_rag.api.schemas.chat import ChatSearchWinesRequest, ChatSearchWinesResponse
from wines_rag.services.chat import ChatService


@pytest.fixture
def chat_service(qdrant_service_mock, model_service_mock):
    """Создаёт экземпляр ChatService с замоканными зависимостями."""
    return ChatService(
        qdrant_service=qdrant_service_mock,
        model=model_service_mock
    )


@pytest.fixture
def search_request():
    """Фикстура для создания запроса поиска."""

    def _create_request(query: str = "красное сухое вино", price_min: float = None, price_max: float = None):
        return ChatSearchWinesRequest(
            query=query,
            price_min=price_min,
            price_max=price_max
        )

    return _create_request


@pytest.fixture
def mock_scored_point():
    """Фикстура для создания ScoredPoint (оригинальный класс qdrant_client)."""
    def _create_scored_point(
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
    return _create_scored_point


@pytest.mark.asyncio
class TestChatServiceSearchWines:
    """Тесты для метода search_wines."""

    async def test_search_wines_success(
            self,
            chat_service,
            qdrant_service_mock,
            model_service_mock,
            search_request,
            mock_embedding,
            mock_summary,
            mock_scored_point
    ):
        """Успешный поиск вин."""
        request = search_request(query="хочу красное вино", price_min=500, price_max=2000)
        embedding = mock_embedding()

        wine_id_1 = uuid4()
        wine_id_2 = uuid4()
        mock_points = [
            mock_scored_point(
                point_id=wine_id_1,
                payload={
                    "name": "Wine 1",
                    "description": "Desc 1",
                    "price": 1000,
                    "color": "red",
                    "acidity": "medium",
                    "country": "France"
                },
                score=0.95
            ),
            mock_scored_point(
                point_id=wine_id_2,
                payload={
                    "name": "Wine 2",
                    "description": "Desc 2",
                    "price": 1500,
                    "color": "red",
                    "acidity": "high",
                    "country": "Italy"
                },
                score=0.87
            )
        ]
        summary_text = mock_summary("Рекомендую Wine 1 и Wine 2")

        model_service_mock.encode.return_value = embedding
        qdrant_service_mock.query_search.return_value = mock_points
        model_service_mock.summarize_wines.return_value = summary_text

        response = await chat_service.search_wines(request)

        assert isinstance(response, ChatSearchWinesResponse)
        assert len(response.wines) == 2
        assert response.summary == summary_text

        model_service_mock.encode.assert_called_once()
        qdrant_service_mock.query_search.assert_called_once()
        model_service_mock.summarize_wines.assert_called_once()

    async def test_search_wines_empty_results(
            self,
            chat_service,
            qdrant_service_mock,
            model_service_mock,
            search_request,
            mock_embedding
    ):
        """Поиск не вернул результатов."""
        request = search_request(query="редкое вино")
        model_service_mock.encode.return_value = mock_embedding()
        qdrant_service_mock.query_search.return_value = []
        model_service_mock.summarize_wines.return_value = "Ничего не найдено"

        response = await chat_service.search_wines(request)

        assert isinstance(response, ChatSearchWinesResponse)
        assert response.wines == []
        assert response.summary == "Ничего не найдено"

    async def test_search_wines_encode_error(
            self,
            chat_service,
            qdrant_service_mock,
            model_service_mock,
            search_request
    ):
        """Ошибка при кодировании запроса."""
        request = search_request(query="тест")
        model_service_mock.encode.side_effect = RuntimeError("Embedding failed")

        with pytest.raises(RuntimeError, match="Embedding failed"):
            await chat_service.search_wines(request)

        qdrant_service_mock.query_search.assert_not_called()

    async def test_search_wines_qdrant_error(
            self,
            chat_service,
            qdrant_service_mock,
            model_service_mock,
            search_request,
            mock_embedding
    ):
        """Ошибка при поиске в Qdrant."""
        request = search_request(query="тест")
        model_service_mock.encode.return_value = mock_embedding()
        qdrant_service_mock.query_search.side_effect = ConnectionError("Qdrant unavailable")

        with pytest.raises(ConnectionError, match="Qdrant unavailable"):
            await chat_service.search_wines(request)

        model_service_mock.summarize_wines.assert_not_called()

    async def test_search_wines_summarize_error(
            self,
            chat_service,
            qdrant_service_mock,
            model_service_mock,
            search_request,
            mock_embedding,
            mock_scored_point
    ):
        """Ошибка при генерации саммаризации."""
        request = search_request(query="тест")

        mock_points = [
            mock_scored_point(
                payload={
                    "name": "Wine",
                    "description": "D",
                    "price": 100,
                    "color": "red",
                    "acidity": "medium",
                    "country": "FR"
                }
            )
        ]

        model_service_mock.encode.return_value = mock_embedding()
        qdrant_service_mock.query_search.return_value = mock_points
        model_service_mock.summarize_wines.side_effect = RuntimeError("API error")

        with pytest.raises(RuntimeError, match="API error"):
            await chat_service.search_wines(request)