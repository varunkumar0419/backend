
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_refunds_endpoint():

    response = client.get(
        "/refunds?page=1&size=10"
    )

    assert response.status_code == 200


def test_refunds_pagination():

    response = client.get(
        "/refunds?page=3&size=25"
    )

    assert response.status_code == 200