FROM python:3.13-slim

# Переменные окружения для кэшей моделей и поведения Python
ENV HF_HOME=/app/.cache/huggingface
ENV FASTEMBED_CACHE_PATH=/app/.cache/fastembed
ENV SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence_transformers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
# Добавляем виртуальное окружение в PATH 
ENV PATH="/app/.venv/bin:$PATH"

# Рабочая директория внутри контейнера — весь проект будет работать из /app
WORKDIR /app

# Создаём непользовательского юзера 'appuser' для безопасности — не запускать процессы
# от root в контейнере.
RUN useradd --create-home --shell /bin/bash appuser

# Обновляем apt и устанавливаем минимальные системные утилиты,
# нужные для сборки пакетов или загрузки артефактов.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем служебные файлы и исходники внутрь контейнера.
# - README.md 
# - uv.lock и pyproject.toml содержат информацию о зависимостях проекта
# - src — директория с кодом приложения
COPY README.md ./
COPY uv.lock pyproject.toml ./
COPY src ./src

# Устанавливаем Python-зависимости. В проекте используется утилита `uv`.
# Команда `uv sync --frozen --no-dev` фиксирует установки согласно lock-файлу.
RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev

# Предзагружаем ML-модели в кэш, чтобы не делать это при первом старте сервера.
# Это выполняет небольшую Python-команду, которая импортирует классы из fastembed
# и инициализирует модели: плотную (sentence-transformers) и разрежённую (bm25).
# Примечание: это увеличит размер образа и время сборки, но ускорит старт контейнера.
RUN mkdir -p /app/.cache && \
    python -c "from fastembed import TextEmbedding, SparseTextEmbedding; \
    print('Downloading dense model...'); \
    TextEmbedding(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); \
    print('Downloading sparse model...'); \
    SparseTextEmbedding(model_name='qdrant/bm25'); \
    print('Models downloaded successfully!')"

# Устанавливаем права на директорию /app пользователю appuser
RUN chown -R appuser:appuser /app

# Переключаемся на непользовательского юзера для выполнения приложения
USER appuser

# Открываем порт, на котором будет слушать Uvicorn (FastAPI)
EXPOSE 8000

# Команда по умолчанию: запускает uvicorn с приложением `wines_rag.app:app`
CMD ["uvicorn", "wines_rag.app:app", "--host", "0.0.0.0", "--port", "8000"]