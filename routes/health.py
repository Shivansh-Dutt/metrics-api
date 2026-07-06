import time

from fastapi import APIRouter

router = APIRouter()

START_TIME = time.time()


@router.get("/healthz")
def health():

    return {
        "status": "ok",
        "uptime_s": time.time() - START_TIME
    }