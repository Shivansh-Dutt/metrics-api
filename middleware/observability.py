import time
import uuid

from prometheus_client import Counter

from starlette.middleware.base import BaseHTTPMiddleware
from utils.logger import logs

HTTP_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)


class ObservabilityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        HTTP_COUNTER.inc()

        request_id = str(uuid.uuid4())
        
        response = await call_next(request)

        logs.append({
            "level": "INFO",
            "ts": time.time(),
            "path": request.url.path,
            "request_id": request_id,
        })

        response.headers["X-Request-ID"] = request_id

        return response