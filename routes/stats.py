from fastapi import APIRouter
from constants import EMAIL

router = APIRouter()


@router.get("/stats")
def stats(values: str):

    nums = [int(x) for x in values.split(",")]

    total = sum(nums)

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums),
    }