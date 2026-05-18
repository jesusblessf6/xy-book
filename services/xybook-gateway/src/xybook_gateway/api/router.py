from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
import httpx

from ..config import get_settings

router = APIRouter()

settings = get_settings()
client = httpx.AsyncClient(timeout=30.0)

ROUTES = {
    "/api/community": settings.community_url,
    "/api/agents": settings.agents_url,
    "/api/pipeline": settings.pipeline_url,
    "/api/experiments": settings.experiments_url,
    "/api/reports": settings.experiments_url,
}


def _match_upstream(path: str) -> str | None:
    for prefix, base_url in ROUTES.items():
        if path.startswith(prefix):
            return base_url
    return None


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request):
    full_path = f"/{path}"
    upstream = _match_upstream(full_path)
    if not upstream:
        return Response(status_code=404, content="No upstream matched")

    url = f"{upstream}{full_path}"
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    resp = await client.request(
        method=request.method,
        url=url,
        content=body,
        headers=headers,
        params=request.query_params,
    )
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
    )
