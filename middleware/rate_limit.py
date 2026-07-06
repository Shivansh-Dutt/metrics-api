import time
from collections import defaultdict, deque

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

RATE_LIMIT = 18
WINDOW = 10  # seconds

# client_id -> deque[timestamps]
CLIENT_REQUESTS = defaultdict(deque)


class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        client_id = request.headers.get("X-Client-Id")

        # No client id → skip limiting
        if not client_id:
            return await call_next(request)

        now = time.time()

        timestamps = CLIENT_REQUESTS[client_id]

        # Remove timestamps older than 10 seconds
        while timestamps and now - timestamps[0] >= WINDOW:
            timestamps.popleft()

        # Limit exceeded
        if len(timestamps) >= RATE_LIMIT:

            retry_after = WINDOW - (now - timestamps[0])

            return JSONResponse(
                status_code=429,
                headers={
                    "Retry-After": str(int(retry_after) + 1)
                },
                content={
                    "detail": "Rate limit exceeded"
                }
            )

        timestamps.append(now)

        return await call_next(request)