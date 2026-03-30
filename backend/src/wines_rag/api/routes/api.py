from fastapi import APIRouter, Response
from wines_rag.metrics import metrics_registry

router = APIRouter(prefix="")


@router.get("/health", include_in_schema=False)
async def health() -> Response:
    return Response(status_code=200)


@router.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(
        content=metrics_registry.render_prometheus(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
