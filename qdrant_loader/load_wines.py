from qdrant_client import QdrantClient
import pandas as pd
import json
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PayloadSchemaType,
)
from uuid import uuid4
import os

QDRANT_URL = os.getenv("QDRANT__URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT__API_KEY", "secret")
COLLECTION_NAME = os.getenv("QDRANT__COLLECTION_NAME", "wines")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
collection_exists = client.collection_exists(COLLECTION_NAME)

if not collection_exists:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "dense_vector": VectorParams(size=384, distance=Distance.COSINE)
        },
    )

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

        pid = uuid4()
        point = {
            "id": str(pid),
            "vector": {"dense_vector": dense_vector},
            "payload": payload,
        }
        points.append(point)

    for i in range(0, len(points), 100):
        batch = points[i : i + 100]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)
        print(f"Загружено {min(i+100, len(points))} из {len(points)}")
else:
    print(f"Коллекция {COLLECTION_NAME} уже существует, пропускаем загрузку.")
