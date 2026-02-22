from fastapi import APIRouter
from wines_rag.api.dependencies import ChatDep
from wines_rag.api.schemas.chat import ChatSearchWinesResponse,ChatSearchWinesRequest
router = APIRouter(prefix="")

@router.post("/search/wines", response_model=ChatSearchWinesResponse, status_code=200)
async def search_wines(search_request: ChatSearchWinesRequest, chat_service: ChatDep)-> ChatSearchWinesResponse:
    print(search_request)
    response = await chat_service.search_wines(search_request)
    return response