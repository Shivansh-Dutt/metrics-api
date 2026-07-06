from typing import Optional

from fastapi import APIRouter

from utils.orders import ORDERS
from utils.cursor import encode_cursor, decode_cursor

from fastapi import Header, HTTPException, status
from utils.orders import IDEMPOTENCY_STORE
import utils.orders as orders_data

router = APIRouter()


@router.get("/orders")
def get_orders(
    limit: int = 10,
    cursor: Optional[str] = None,
):
    # First request starts from index 0
    start = 0 if cursor is None else decode_cursor(cursor)

    # Fetch current page
    items = ORDERS[start:start + limit]

    # Compute next cursor
    next_start = start + len(items)

    next_cursor = (
        encode_cursor(next_start)
        if next_start < len(ORDERS)
        else None
    )

    return {
        "items": items,
        "next_cursor": next_cursor
    }
    
@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(
    idempotency_key: str = Header(..., alias="Idempotency-Key")
):
    # Already created
    if idempotency_key in IDEMPOTENCY_STORE:
        return IDEMPOTENCY_STORE[idempotency_key]

    # Create a new order
    order = {
        "id": orders_data.NEXT_ORDER_ID
    }

    orders_data.NEXT_ORDER_ID += 1

    IDEMPOTENCY_STORE[idempotency_key] = order

    return order