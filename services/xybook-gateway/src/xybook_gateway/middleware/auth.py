from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from ..config import get_settings

# Paths that never require auth
PUBLIC_PATHS = {"/health", "/docs", "/openapi.json", "/redoc"}

# Prefixes where GET is public but writes require auth
PUBLIC_READ_PREFIXES = ("/api/community",)


class AuthMiddleware(BaseHTTPMiddleware):
    """API Key authentication for admin-protected routes."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path

        # Public paths
        if path in PUBLIC_PATHS:
            return await call_next(request)

        # Public GET on community
        if request.method == "GET":
            for prefix in PUBLIC_READ_PREFIXES:
                if path.startswith(prefix):
                    return await call_next(request)

        # All other routes require X-API-Key
        api_key = request.headers.get("x-api-key")
        settings = get_settings()

        if not api_key or api_key != settings.admin_api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API key"},
            )

        return await call_next(request)
