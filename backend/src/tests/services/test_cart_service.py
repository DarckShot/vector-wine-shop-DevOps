import pytest
from uuid import uuid4

from wines_rag.api.schemas.cart import CartGetResponse, CartPutResponse
from wines_rag.errors import WineNotFoundException
from wines_rag.services.cart import CartService


@pytest.fixture
def cart_service(qdrant_service_mock):
    """Создаёт экземпляр CartService с замоканной зависимостью."""
    return CartService(qdrant_service=qdrant_service_mock)


@pytest.mark.asyncio
class TestCartServiceAddWine:
    """Тесты для метода add_wine."""

    async def test_add_wine_success(self, cart_service, qdrant_service_mock, wine_id, mock_qdrant_record):
        """Успешное добавление вина в корзину."""
        mock_record = mock_qdrant_record(payload={"count": 0}, point_id=wine_id)
        qdrant_service_mock.point_exists.return_value = mock_record

        await cart_service.add_wine(wine_id)

        qdrant_service_mock.point_exists.assert_called_once_with(point_id=wine_id)
        qdrant_service_mock.update_point_count.assert_called_once_with(
            point_id=wine_id,
            new_count_value=1
        )

    async def test_add_wine_not_found(self, cart_service, qdrant_service_mock, wine_id):
        """Добавление несуществующего вина вызывает WineNotFoundException."""
        qdrant_service_mock.point_exists.return_value = None

        with pytest.raises(WineNotFoundException):
            await cart_service.add_wine(wine_id)

        qdrant_service_mock.update_point_count.assert_not_called()


@pytest.mark.asyncio
class TestCartServiceDeleteWine:
    """Тесты для метода delete_wine."""

    async def test_delete_wine_success(self, cart_service, qdrant_service_mock, wine_id, mock_qdrant_record):
        """Успешное удаление вина из корзины."""
        mock_record = mock_qdrant_record(payload={"count": 5}, point_id=wine_id)
        qdrant_service_mock.point_exists.return_value = mock_record

        await cart_service.delete_wine(wine_id)

        qdrant_service_mock.point_exists.assert_called_once_with(point_id=wine_id)
        qdrant_service_mock.update_point_count.assert_called_once_with(
            point_id=wine_id,
            new_count_value=0
        )

    async def test_delete_wine_not_found(self, cart_service, qdrant_service_mock, wine_id):
        """Удаление несуществующего вина вызывает WineNotFoundException."""
        qdrant_service_mock.point_exists.return_value = None

        with pytest.raises(WineNotFoundException):
            await cart_service.delete_wine(wine_id)

        qdrant_service_mock.update_point_count.assert_not_called()


@pytest.mark.asyncio
class TestCartServicePutWine:
    """Тесты для метода put_wine."""

    async def test_put_wine_success(self, cart_service, qdrant_service_mock, wine_id, mock_qdrant_record):
        """Успешное обновление количества вина."""
        new_count = 10
        initial_record = mock_qdrant_record(payload={"count": 1}, point_id=wine_id)
        updated_record = mock_qdrant_record(payload={"count": new_count}, point_id=wine_id)

        qdrant_service_mock.point_exists.side_effect = [initial_record, updated_record]
        qdrant_service_mock.update_point_count.return_value = True

        response = await cart_service.put_wine(wine_id, new_count)

        assert isinstance(response, CartPutResponse)
        assert response.updated_count == new_count
        assert qdrant_service_mock.point_exists.call_count == 2
        qdrant_service_mock.update_point_count.assert_called_once_with(
            point_id=wine_id,
            new_count_value=new_count
        )

    async def test_put_wine_update_failed(self, cart_service, qdrant_service_mock, wine_id, mock_qdrant_record):
        """Обновление количества вернуло False — метод возвращает None."""
        mock_record = mock_qdrant_record(payload={"count": 1}, point_id=wine_id)
        qdrant_service_mock.point_exists.return_value = mock_record
        qdrant_service_mock.update_point_count.return_value = False

        response = await cart_service.put_wine(wine_id, 10)

        assert response is None

    async def test_put_wine_not_found(self, cart_service, qdrant_service_mock, wine_id):
        """Обновление несуществующего вина вызывает WineNotFoundException."""
        qdrant_service_mock.point_exists.return_value = None

        with pytest.raises(WineNotFoundException):
            await cart_service.put_wine(wine_id, 10)

        qdrant_service_mock.update_point_count.assert_not_called()


@pytest.mark.asyncio
class TestCartServiceGetWines:
    """Тесты для метода get_wines."""

    async def test_get_wines_success(self, cart_service, qdrant_service_mock, mock_qdrant_record):
        """Успешное получение списка вин."""
        wine_id_1 = uuid4()
        wine_id_2 = uuid4()

        mock_points = [
            mock_qdrant_record(
                payload={
                    "count": 1,
                    "name": "Wine 1",
                    "description": "Description 1",
                    "price": 100.0,
                    "color": "red",
                    "acidity": "medium",
                    "country": "France"
                },
                point_id=wine_id_1
            ),
            mock_qdrant_record(
                payload={
                    "count": 5,
                    "name": "Wine 2",
                    "description": "Description 2",
                    "price": 200.0,
                    "color": "white",
                    "acidity": "high",
                    "country": "Italy"
                },
                point_id=wine_id_2
            )
        ]
        qdrant_service_mock.get_available_wines.return_value = mock_points

        response = await cart_service.get_wines()

        assert isinstance(response, CartGetResponse)
        assert len(response.wines) == 2
        qdrant_service_mock.get_available_wines.assert_called_once()

    async def test_get_wines_empty_list(self, cart_service, qdrant_service_mock):
        """Получение пустого списка вин."""
        qdrant_service_mock.get_available_wines.return_value = []

        response = await cart_service.get_wines()

        assert isinstance(response, CartGetResponse)
        assert response.wines == []