from unittest.mock import AsyncMock
from typing import List


def create_model_service_mock() -> AsyncMock:
    """
    Создаёт переиспользуемый мок для ModelService.
    """
    mock = AsyncMock()
    mock.__class__.__name__ = "ModelService"

    mock.encode = AsyncMock()
    mock.summarize_wines = AsyncMock()

    return mock


def create_mock_embedding(dim: int = 384) -> List[float]:
    """Создаёт мок-вектор эмбеддинга."""
    return [0.1] * dim


def create_mock_summary(text: str = "Mock summary response") -> str:
    """Создаёт мок-ответ саммаризации."""
    return text