FROM python:3.13-slim

ENV HF_HOME=/app/.cache/huggingface
ENV FASTEMBED_CACHE_PATH=/app/.cache/fastembed
ENV SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence_transformers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app


RUN useradd --create-home --shell /bin/bash appuser


RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY README.md ./
COPY uv.lock pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev


RUN mkdir -p /app/.cache && \
    python -c "from fastembed import TextEmbedding, SparseTextEmbedding; \
    print('Downloading dense model...'); \
    TextEmbedding(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); \
    print('Downloading sparse model...'); \
    SparseTextEmbedding(model_name='qdrant/bm25'); \
    print('Models downloaded successfully!')"


RUN chown -R appuser:appuser /app


USER appuser

EXPOSE 8000


CMD ["uvicorn", "wines_rag.app:app", "--host", "0.0.0.0", "--port", "8000"]