from src.order import read_order
import os


def test_read_order():
    response = read_order(
        pickup_lon=120.9635254,
        pickup_lat=14.6348514,
        dropoff_lon=121.0254764,
        dropoff_lat=14.565466,
        debug=True,
    )
    filepath = f"data/orders/unassigned/{response['order_id']}.json"
    file_created = os.path.exists(filepath)
    os.remove(filepath)

    assert file_created
