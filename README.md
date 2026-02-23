# vector-wine-shop-DevOps

## сборка образа бэкенда
docker build -t wines_rag_backend .

## Запуск всего приложения в докере
создать предварительно файлк .env рядом с docker-compose.yml \
обязательно задать: \ 
QDRANT__API_KEY=ваш_ключ \
QDRANT__SERVICE__API_KEY=ваш_ключ \
QDRANT__URL="http://qdrant:6333" \
MODEL__GENERATIVE__API_KEY=ваш_ключ \
выполнить: docker compose up -d \
просмотр логов: docker compose logs -f \
