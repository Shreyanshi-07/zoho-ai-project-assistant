from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        user_id = request.cookies.get("session_user")

        if request.url.path.startswith("/chat") and not user_id:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                {"detail": "Unauthorized"},
                status_code=401,
            )

        request.state.user_id = user_id
        return await call_next(request)
