from fastapi import APIRouter, Response

router = APIRouter(prefix="")


@router.get("/health", include_in_schema=False)
async def health() -> Response:
    return Response(status_code=200)
