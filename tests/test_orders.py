
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_orders_endpoint():

    response = client.get(
        "/orders?page=1&size=10"
    )

    assert response.status_code == 200


def test_orders_pagination():

    response = client.get(
        "/orders?page=2&size=50"
    )

    assert response.status_code == 200