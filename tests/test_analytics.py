
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analytics_summary():

    response = client.get(
        "/analytics/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_orders" in data
    assert "total_revenue" in data
    assert "total_refunds" in data
    assert "net_revenue" in data
    assert "average_order_value" in data