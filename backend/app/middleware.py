from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class LoginRedirectMiddleware(BaseHTTPMiddleware):
    """Turn panel auth failures into a browser-friendly /login redirect."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        accept = request.headers.get("accept", "")
        if (
            response.status_code in {303, 401}
            and "text/html" in accept
            and request.url.path.startswith(("/admin", "/super-admin", "/teacher", "/student", "/parent"))
        ):
            return RedirectResponse(url="/login", status_code=302)
        return response
