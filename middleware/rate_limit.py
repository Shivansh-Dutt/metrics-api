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

        # Only rate limit the orders endpoint
        # if request.url.path != "/orders":
        #     return await call_next(request)
        client_id = request.headers.get("X-Client-Id")

        # No client id → skip limiting
        if not client_id:
            return await call_next(request)

        now = time.time()

        timestamps = CLIENT_REQUESTS[client_id]

        # Remove timestamps older than 10 seconds
        while timestamps and now - timestamps[0] >= WINDOW:
            timestamps.popleft()

        print(
            request.method,
            request.url.path,
            request.headers.get("X-Client-Id"),
            len(timestamps),
        )
        # Limit exceeded
        if len(timestamps) >= RATE_LIMIT:
            retry_after = max(1, int(WINDOW - (now - timestamps[0])))

            return JSONResponse(
                status_code=429,
                headers={"Retry-After": str(retry_after)},
                content={"detail": "Too Many Requests"},
            )
            
        timestamps.append(now)

        return await call_next(request)
