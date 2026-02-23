from fastembed import TextEmbedding
from qdrant_client import QdrantClient
import pandas as pd
import json
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    SparseVectorParams,
    SparseIndexParams,
    PayloadSchemaType,
)
from uuid import uuid4
import os

QDRANT_URL = os.getenv("QDRANT__URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT__API_KEY", "secret")
COLLECTION_NAME = os.getenv("QDRANT__COLLECTION_NAME", "wines")

# нулевая часть - сформировать вектора заранее
# embedding_model = TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
# # models = TextEmbedding.list_supported_models()


# input_file = 'prepared_wines_utf.csv'  # Укажите ваш путь
# output_file = 'wines.csv'
# df = pd.read_csv(input_file,sep=';',
#     quotechar='"',
#     quoting=0,
#    )


# def create_text_for_embedding(row):
#     return (
#         f"Name: {row['name']}. "
#         f"Description: {row['description']}. "
#         f"Country: {row['country']}. "
#         f"Acidity: {row['acidity']}. "
#         f"Color: {row['color']}."
#     )

# texts_to_embed = df.apply(create_text_for_embedding, axis=1).tolist()

# print(f"Генерация эмбеддингов для {len(texts_to_embed)} записей...")
# embeddings_iterator = embedding_model.embed(texts_to_embed)
# vectors = [embedding.tolist() for embedding in embeddings_iterator]
# df['dense_vector'] = [json.dumps(vec) for vec in vectors]
# df.to_csv(output_file, index=False, encoding='utf-8-sig')

# print(f"Готово! Файл сохранен как {output_file}")
# print(f"Размерность вектора: {len(vectors[0])}")

# первая часть - создание коллецкии, если ее нет
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "dense_vector": VectorParams(size=384, distance=Distance.COSINE)
        },
        sparse_vectors_config={"bm25": SparseVectorParams(index=SparseIndexParams())},
    )


# вторая часть - прогрузка вин
df = pd.read_csv("wines.csv", encoding="utf-8-sig")
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="price",
    field_schema=PayloadSchemaType.FLOAT,
)

points = []
for _, row in df.iterrows():
    dense_vector = json.loads(row["dense_vector"])
    price_str = str(row["price"]).replace(",", ".").replace(" ", "")

    payload = {
        "name": row["name"],
        "description": row["description"],
        "price": float(price_str),
        "acidity": row["acidity"],
        "color": row["color"],
        "country": row["country"],
        "count": 0,
    }

    bm25_text = f"{row['name']} {row['description']} {row['country']} {row["acidity"]} {row["color"]}"
    pid = uuid4()
    point = {
        "id": pid,
        "vector": {
            "dense_vector": dense_vector,
            "bm25": {"text": bm25_text, "model": "qdrant/bm25"},
        },
        "payload": payload,
    }
    points.append(point)


for i in range(0, len(points), 100):
    batch = points[i : i + 100]
    client.upsert(collection_name=COLLECTION_NAME, points=batch)
    print(f"Загружено {min(i+100, len(points))} из {len(points)}")
