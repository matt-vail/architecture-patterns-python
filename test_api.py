import pytest
import requests

def random_orderid():
    return random.randint(1, 1000)

def random_sku(name=""):
    return f"sku-{name}-{random.randint(1, 1000)}"

def random_batchref(num):
    return f"batch-{num}"

@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock):
    # Arrange
    sku, otherski = random_sku(), random_sku("other")
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock(
        [
            (laterbatch, sku, 100, "2011-01-02"),
            (earlybatch, sku, 100, "2011-01-01"),
            (otherbatch, otherski, 100, None),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = config.get_api_url()
    # Act
    r = requests.post(f"{url}/allocate", json=data)
    # Assert
    assert r.status_code == 201
    assert r.json()["batchref"] == earlybatch
