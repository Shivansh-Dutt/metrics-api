from fastapi import APIRouter
from constants import EMAIL

router = APIRouter()


@router.get("/work")
def work(n: int):

    # simulate K units of work
    for _ in range(n):
        pass

    return {
        "email": EMAIL,
        "done": n
    }