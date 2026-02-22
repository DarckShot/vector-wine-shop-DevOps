

from typing import Annotated

from fastapi import Depends, Request
from wines_rag.config import Config
from wines_rag.services.chat import ChatService
from wines_rag.services.model import ModelService
from wines_rag.services.qdrant.client import QdrantService


async def get_qdrat_client(request:Request):
    return request.app.state.qdrant_client

async def get_config(request:Request):
    return request.app.state.config

async def get_model(request:Request):
    return request.app.state.model

ConfigDep = Annotated[Config,Depends(get_config)]
QdrantDep = Annotated[QdrantService,Depends(get_qdrat_client)]
ModelDep = Annotated[ModelService,Depends(get_model)]

async def get_chat_service(
    qdrant_service: QdrantDep,
    model: ModelDep
)->ChatService:
    return ChatService(qdrant_service=qdrant_service,model=model)
ChatDep = Annotated[ChatService,Depends(get_chat_service)]