from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middleware.metrics import MetricsMiddleware
from middleware.observability import ObservabilityMiddleware

from routes.stats import router as stats_router
from routes.verify import router as verify_router
from routes.config import router as config_router
from routes.analytics import router as analytics_router
from routes.health import router as health_router
from routes.logs import router as logs_router
from routes.metrics import router as metrics_router
from routes.work import router as work_router
from routes.orders import router as orders_router
from middleware.rate_limit import RateLimitMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dash-b9qyop.example.com",
        "https://exam.sanand.workers.dev", 
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(MetricsMiddleware)
app.add_middleware(RateLimitMiddleware)

app.include_router(stats_router)
app.include_router(verify_router)
app.include_router(config_router)
app.include_router(analytics_router)
app.include_router(orders_router)


obs_app = FastAPI()

obs_app.add_middleware(ObservabilityMiddleware)

obs_app.include_router(work_router)
obs_app.include_router(metrics_router)
obs_app.include_router(health_router)
obs_app.include_router(logs_router)

app.mount("/obs", obs_app)

@app.get("/")
def home():
    return {"message": "Hello World"}