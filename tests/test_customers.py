from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_customers_endpoint():

    response = client.get(
        "/customers?page=1&size=10"
    )

    assert response.status_code == 200


def test_customers_pagination():

    response = client.get(
        "/customers?page=1&size=100"
    )

    assert response.status_code == 200