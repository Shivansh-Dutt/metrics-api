from fastapi import APIRouter

from utils.logger import logs

router = APIRouter()


@router.get("/logs/tail")
def tail(limit: int = 10):

    return list(logs)[-limit:]