import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class MetricsMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        return response
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dash-b9qyop.example.com"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(MetricsMiddleware)


EMAIL = "24f2002771@ds.study.iitm.ac.in"


@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/stats")
def stats(values: str):
    nums = [int(x) for x in values.split(",")]

    count = len(nums)
    total = sum(nums)
    minimum = min(nums)
    maximum = max(nums)
    mean = total / count

    return {
        "email":EMAIL,
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": mean
    }