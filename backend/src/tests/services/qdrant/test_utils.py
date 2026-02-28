import pytest
from uuid import uuid4, UUID

from qdrant_client.models import FieldCondition, Filter, Range, Record, ScoredPoint

from wines_rag.api.schemas.cart import Wine
from wines_rag.entities.qdrant import WineBase
from wines_rag.services.qdrant.utils import (
    make_qdrant_filters,
    qdrant_scored_points_to_wines,
    qdrant_points_to_wines
)


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


@pytest.mark.asyncio
class TestMakeQdrantFilters:
    """Тесты для функции make_qdrant_filters."""

    async def test_no_filters(self):
        """Оба параметра None — возвращается Filter с пустым must."""
        result = await make_qdrant_filters(price_min=None, price_max=None)

        assert isinstance(result, Filter)
        assert result.must == []

    async def test_price_min_only(self):
        """Только price_min — один FieldCondition с gte."""
        result = await make_qdrant_filters(price_min=100.0, price_max=None)

        assert isinstance(result, Filter)
        assert len(result.must) == 1
        assert isinstance(result.must[0], FieldCondition)
        assert result.must[0].key == "price"
        assert isinstance(result.must[0].range, Range)
        assert result.must[0].range.gte == 100.0
        assert result.must[0].range.lte is None

    async def test_price_max_only(self):
        """Только price_max — один FieldCondition с lte."""
        result = await make_qdrant_filters(price_min=None, price_max=500.0)

        assert isinstance(result, Filter)
        assert len(result.must) == 1
        assert result.must[0].key == "price"
        assert result.must[0].range.gte is None
        assert result.must[0].range.lte == 500.0

    async def test_both_price_filters(self):
        """Оба параметра — два FieldCondition."""
        result = await make_qdrant_filters(price_min=100.0, price_max=500.0)

        assert isinstance(result, Filter)
        assert len(result.must) == 2

        ranges = [cond.range for cond in result.must if cond.key == "price"]
        assert any(r.gte == 100.0 for r in ranges)
        assert any(r.lte == 500.0 for r in ranges)

    async def test_zero_price_min(self):
        """price_min=0 должен добавляться в фильтр."""
        result = await make_qdrant_filters(price_min=0.0, price_max=None)

        assert len(result.must) == 1
        assert result.must[0].range.gte == 0.0

    async def test_negative_price(self):
        """Отрицательные цены (валидация на уровне бизнес-логики)."""
        result = await make_qdrant_filters(price_min=-10.0, price_max=-1.0)

        assert len(result.must) == 2
        assert result.must[0].range.gte == -10.0
        assert result.must[1].range.lte == -1.0


@pytest.mark.asyncio
class TestQdrantScoredPointsToWines:
    """Тесты для функции qdrant_scored_points_to_wines."""

    async def test_empty_list(self):
        """Пустой список — возвращается пустой список."""
        result = await qdrant_scored_points_to_wines(points=[])

        assert result == []

    async def test_valid_points(self, create_scored_point, valid_wine_payload):
        """Валидные точки конвертируются в WineBase."""
        wine_id = uuid4()
        points = [
            create_scored_point(point_id=wine_id, payload=valid_wine_payload, score=0.95)
        ]

        result = await qdrant_scored_points_to_wines(points=points)

        assert len(result) == 1
        assert isinstance(result[0], WineBase)
        assert result[0].id == wine_id
        assert result[0].name == "Test Wine"
        assert result[0].price == 99.99

    async def test_empty_payload_skipped(self, create_scored_point, valid_wine_payload):
        """Точки с пустым payload пропускаются."""
        points = [
            create_scored_point(payload={}),
            create_scored_point(
                payload=valid_wine_payload,
                point_id=uuid4()
            ),
            create_scored_point(payload=None)
        ]

        result = await qdrant_scored_points_to_wines(points=points)

        assert len(result) == 1
        assert result[0].name == "Test Wine"

    async def test_count_field_filtered_out(self, create_scored_point, valid_wine_payload):
        """Поле 'count' удаляется из payload при конвертации."""
        payload_with_count = {**valid_wine_payload, "count": 5}
        points = [create_scored_point(payload=payload_with_count)]

        result = await qdrant_scored_points_to_wines(points=points)

        assert len(result) == 1
        assert not hasattr(result[0], 'count')
        assert result[0].price == valid_wine_payload["price"]

    async def test_multiple_points(self, create_scored_point):
        """Конвертация нескольких точек."""
        points = [
            create_scored_point(
                payload={"name": f"Wine {i}", "description": "D", "price": i * 100,
                         "color": "red", "acidity": "medium", "country": "FR"},
                score=0.9 - i * 0.1
            )
            for i in range(3)
        ]

        result = await qdrant_scored_points_to_wines(points=points)

        assert len(result) == 3
        assert [w.name for w in result] == ["Wine 0", "Wine 1", "Wine 2"]
        assert [w.price for w in result] == [0, 100, 200]

    async def test_missing_required_field_raises(self, create_scored_point):
        """Отсутствие обязательного поля WineBase вызывает ValidationError."""
        incomplete_payload = {"name": "Incomplete"}  # нет description, price, etc.
        points = [create_scored_point(payload=incomplete_payload)]

        with pytest.raises(Exception):
            await qdrant_scored_points_to_wines(points=points)


@pytest.mark.asyncio
class TestQdrantPointsToWines:
    """Тесты для функции qdrant_points_to_wines."""

    async def test_empty_list(self):
        """Пустой список — возвращается пустой список."""
        result = await qdrant_points_to_wines(points=[])

        assert result == []

    async def test_valid_records(self, create_record, valid_wine_payload):
        """Валидные Record конвертируются в Wine."""
        wine_id = uuid4()
        payload_with_count = {**valid_wine_payload, "count": 3}
        records = [create_record(point_id=wine_id, payload=payload_with_count)]

        result = await qdrant_points_to_wines(points=records)

        assert len(result) == 1
        assert isinstance(result[0], Wine)
        assert result[0].id == wine_id
        assert result[0].name == "Test Wine"
        assert result[0].count == 3

    async def test_empty_payload_skipped(self, create_record, valid_wine_payload):
        """Записи с пустым payload пропускаются."""
        payload_with_count = {**valid_wine_payload, "count": 1}

        records = [
            create_record(payload={}),
            create_record(
                payload=payload_with_count,
                point_id=uuid4()
            ),
            create_record(payload=None)
        ]

        result = await qdrant_points_to_wines(points=records)

        assert len(result) == 1
        assert result[0].name == "Test Wine"
        assert result[0].count == 1

    async def test_count_field_preserved(self, create_record, valid_wine_payload):
        """Поле 'count' сохраняется при конвертации в Wine."""
        payload_with_count = {**valid_wine_payload, "count": 10}
        records = [create_record(payload=payload_with_count)]

        result = await qdrant_points_to_wines(points=records)

        assert len(result) == 1
        assert result[0].count == 10

    async def test_multiple_records(self, create_record):
        """Конвертация нескольких записей."""
        records = [
            create_record(
                payload={"name": f"Wine {i}", "description": "D", "price": i * 100,
                         "color": "red", "acidity": "medium", "country": "FR", "count": i + 1}
            )
            for i in range(3)
        ]

        result = await qdrant_points_to_wines(points=records)

        assert len(result) == 3
        assert [w.name for w in result] == ["Wine 0", "Wine 1", "Wine 2"]
        assert [w.count for w in result] == [1, 2, 3]

    async def test_missing_required_field_raises(self, create_record):
        """Отсутствие обязательного поля Wine вызывает ValidationError."""
        incomplete_payload = {"name": "Incomplete", "count": 1}
        records = [create_record(payload=incomplete_payload)]

        with pytest.raises(Exception):
            await qdrant_points_to_wines(points=records)