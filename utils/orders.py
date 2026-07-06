# utils/orders.py

TOTAL_ORDERS = 56

# Fixed catalog of orders
ORDERS = [
    {
        "id": i,
        "item": f"Item {i}"
    }
    for i in range(1, TOTAL_ORDERS + 1)
]

# Stores idempotency key -> created order
IDEMPOTENCY_STORE = {}

# Next order id for POST /orders
NEXT_ORDER_ID = TOTAL_ORDERS + 1