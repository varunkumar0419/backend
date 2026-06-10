
from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    total_orders: int
    total_revenue: float
    total_refunds: float
    net_revenue: float
    average_order_value: float