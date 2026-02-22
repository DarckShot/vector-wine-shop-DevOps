

from typing import Annotated

from fastapi import Depends, Request
from fastembed import TextEmbedding
from openai import AsyncOpenAI
from wines_rag.config import Config
from wines_rag.services.cart import CartService
from wines_rag.services.chat import ChatService
from wines_rag.services.model import ModelService
from wines_rag.services.qdrant.client import QdrantService


async def get_qdrat_client(request:Request):
    return request.app.state.qdrant_client

async def get_config(request:Request):
    return request.app.state.config

async def get_embedding_model(request: Request) -> TextEmbedding:
    return request.app.state.embedding_model

async def get_generative_model(request: Request) -> AsyncOpenAI:
    return request.app.state.generative_model


ConfigDep = Annotated[Config,Depends(get_config)]
QdrantDep = Annotated[QdrantService,Depends(get_qdrat_client)]


async def get_model_service(
    config: ConfigDep,
    embedding_model: TextEmbedding = Depends(get_embedding_model),
    generative_model: AsyncOpenAI = Depends(get_generative_model)
) -> ModelService:
    return ModelService(
        config=config,
        embedding_model=embedding_model,
        generative_model=generative_model
    )
ModelDep = Annotated[ModelService,Depends(get_model_service)]

async def get_chat_service(
    qdrant_service: QdrantDep,
    model: ModelDep
)->ChatService:
    return ChatService(qdrant_service=qdrant_service,model=model)
ChatDep = Annotated[ChatService,Depends(get_chat_service)]

async def get_cart_service(
    qdrant_service: QdrantDep,
)->CartService:
    return CartService(qdrant_service=qdrant_service)
CartDep = Annotated[CartService,Depends(get_cart_service)]