from typing import AsyncIterator

from fastapi import FastAPI
from wines_rag.config import Config, PathSettings
from wines_rag.services.model import ModelService
from wines_rag.services.qdrant.client import QdrantService
import uvicorn
from wines_rag.api.routes.api import router as health_router
from wines_rag.api.routes.chat import router as chat_router
from pathlib import Path
 
APP_DIR = Path(__file__).parent
PROJECT_ROOT = APP_DIR.parent
path_settings: PathSettings = PathSettings(yaml_path=f"{PROJECT_ROOT}/config.yaml",env_path=f"{PROJECT_ROOT}/.env.local")

async def lifespan(app:FastAPI)->AsyncIterator[None]:
    config = Config.load(path_settings=path_settings)
    qdrant_client = QdrantService(config=config)
    model = ModelService(config=config)
    app.state.qdrant_client = qdrant_client
    app.state.model = model
    app.state.config = config
    yield
    await qdrant_client.close()
    print("QdrantService connection closed")
    
app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(
        "wines_rag.app:app",  
        host="localhost",
        reload=True  
    )