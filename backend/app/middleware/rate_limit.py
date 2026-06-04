from collections import defaultdict, deque
from time import time

from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import get_settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        key = request.client.host if request.client else "anonymous"
        now = time()
        window = self.requests[key]
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= settings.rate_limit_per_minute:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        window.append(now)
        return await call_next(request)
