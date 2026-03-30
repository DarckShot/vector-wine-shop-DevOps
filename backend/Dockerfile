FROM python:3.13-slim AS build

ENV HF_HOME=/app/.cache/huggingface \
    FASTEMBED_CACHE_PATH=/app/.cache/fastembed \
    SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence_transformers \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.8.6 /uv /uvx /bin/

COPY README.md pyproject.toml uv.lock ./

# Install third-party dependencies first to maximize cache reuse when app code changes.
RUN uv sync --frozen --no-dev --no-install-project

# Предзагружаем модели в build-слое, чтобы ускорить первый старт контейнера.
RUN mkdir -p /app/.cache && \
    python -c "from fastembed import TextEmbedding, SparseTextEmbedding; \
    print('Downloading dense model...'); \
    TextEmbedding(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); \
    print('Downloading sparse model...'); \
    SparseTextEmbedding(model_name='qdrant/bm25'); \
    print('Models downloaded successfully!')"

COPY src ./src

# Install the local project after source copy; dependency layer above remains cacheable.
RUN uv sync --frozen --no-dev


FROM python:3.13-slim AS runtime

ENV HF_HOME=/app/.cache/huggingface \
    FASTEMBED_CACHE_PATH=/app/.cache/fastembed \
    SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence_transformers \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser

COPY --from=build --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=build --chown=appuser:appuser /app/.cache /app/.cache
COPY --from=build --chown=appuser:appuser /app/src /app/src

USER appuser

EXPOSE 8000

CMD ["uvicorn", "wines_rag.app:app", "--host", "0.0.0.0", "--port", "8000"]