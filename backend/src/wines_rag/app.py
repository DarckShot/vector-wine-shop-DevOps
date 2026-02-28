from typing import AsyncIterator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastembed import TextEmbedding
from openai import AsyncOpenAI
from wines_rag.config import Config, PathSettings
from wines_rag.errors import WineNotFoundException, WineServiceError
from wines_rag.services.model import ModelService
from wines_rag.services.qdrant.client import QdrantService
import uvicorn
from wines_rag.api.routes.api import router as health_router
from wines_rag.api.routes.chat import router as chat_router
from wines_rag.api.routes.cart import router as cart_router
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

APP_DIR = Path(__file__).parent
PROJECT_ROOT = APP_DIR.parent
path_settings: PathSettings = PathSettings(
    yaml_path=f"{PROJECT_ROOT}/config.yaml", env_path=f"{PROJECT_ROOT}/.env.local"
)


async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    config = Config.load(path_settings=path_settings)
    print(f"Qdrant_url: {config.qdrant.url}")
    qdrant_client = QdrantService(config=config)
    embedding_model = TextEmbedding(model_name=config.model.embedding.model)
    generative_model = AsyncOpenAI(
        api_key=config.model.generative.api_key, base_url=config.model.generative.url
    )

    app.state.qdrant_client = qdrant_client
    app.state.embedding_model = embedding_model
    app.state.generative_model = generative_model
    app.state.config = config
    yield
    await qdrant_client.close()
    await generative_model.close()
    print("QdrantService connection closed")


app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(cart_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(WineNotFoundException)
async def wine_not_found_handler(request: Request, exc: WineNotFoundException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.exception_handler(WineServiceError)
async def wine_service_error_handler(request: Request, exc: WineServiceError):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    loc = first_error.get("loc", ())

    if isinstance(loc, (list, tuple)):
        field_name = loc[-1] if loc else "unknown"
    else:
        field_name = str(loc)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errorCode": "VALIDATION_ERROR",
            "userMessage": f"{first_error['msg']} (поле: {field_name})",
        },
    )
