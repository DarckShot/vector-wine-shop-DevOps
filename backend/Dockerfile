FROM python:3.13-slim AS build

ENV HF_HOME=/app/.cache/huggingface \
    FASTEMBED_CACHE_PATH=/app/.cache/fastembed \
    SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence_transformers \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY README.md pyproject.toml uv.lock ./
COPY src ./src

RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev

# Предзагружаем модели в build-слое, чтобы ускорить первый старт контейнера.
RUN mkdir -p /app/.cache && \
    python -c "from fastembed import TextEmbedding, SparseTextEmbedding; \
    print('Downloading dense model...'); \
    TextEmbedding(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); \
    print('Downloading sparse model...'); \
    SparseTextEmbedding(model_name='qdrant/bm25'); \
    print('Models downloaded successfully!')"


FROM python:3.13-slim AS runtime

ENV HF_HOME=/app/.cache/huggingface \
    FASTEMBED_CACHE_PATH=/app/.cache/fastembed \
    SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence_transformers \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser

COPY --from=build /app/.venv /app/.venv
COPY --from=build /app/.cache /app/.cache
COPY --from=build /app/src /app/src

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "wines_rag.app:app", "--host", "0.0.0.0", "--port", "8000"]