from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middleware.metrics import MetricsMiddleware

from routes.stats import router as stats_router
from routes.verify import router as verify_router
from routes.config import router as config_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dash-b9qyop.example.com"
        "https://exam.sanand.workers.dev/tds-2026-05-ga2",    
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(MetricsMiddleware)

app.include_router(stats_router)
app.include_router(verify_router)
app.include_router(config_router)


@app.get("/")
def home():
    return {"message": "Hello World"}