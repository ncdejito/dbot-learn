from typing import Optional

from fastapi import FastAPI

import uuid
import json

import os

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Instructions": "Order using endpoint formatted: /order/pickup={pickup_lon},{pickup_lat};dropoff={dropoff_lon},{dropoff_lat};"
    }


# http://127.0.0.1:8000/order/pickup=120.9635254,14.6348514;dropoff=121.0254764,14.565466
# http://127.0.0.1:8000/order/pickup=120.9907252,14.6697775;dropoff=121.0314065,14.6392059
@app.get(
    "/order/pickup={pickup_lon},{pickup_lat};dropoff={dropoff_lon},{dropoff_lat};"
)
def read_order(
    pickup_lon: float,
    pickup_lat: float,
    dropoff_lon: float,
    dropoff_lat: float,
    debug=False,
) -> dict:
    order = json.load(open("data/orders/template.json", "r"))
    order_id = uuid.uuid4()
    order["order_id"] = str(order_id)

    order["pickup"]["lon"] = pickup_lon
    order["pickup"]["lat"] = pickup_lat
    order["dropoff"]["lon"] = dropoff_lon
    order["dropoff"]["lat"] = dropoff_lat

    json.dump(order, open(f"data/orders/unassigned/{order_id}.json", "w"))

    if debug:
        return order

    return {
        "response": f"Your order has been received with reference no. {order_id}. Track it here: <streamlit webapp>/order={order_id}"
    }
