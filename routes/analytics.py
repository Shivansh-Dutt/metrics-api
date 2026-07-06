from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

API_KEY = "ak_ht41wht6omfpeywieybi5f8t"
EMAIL = "24f2002771@ds.study.iitm.ac.in"   # <-- Replace with your IITM email


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@router.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str = Header(None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = request.events

    total_events = len(events)

    unique_users = len({e.user for e in events})

    revenue = sum(e.amount for e in events if e.amount > 0)

    user_totals = {}

    for e in events:
        if e.amount > 0:
            user_totals[e.user] = user_totals.get(e.user, 0) + e.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }