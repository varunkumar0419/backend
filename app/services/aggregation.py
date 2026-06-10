
from sqlalchemy import func

from app.db.models import (
    Order,
    Refund
)


def build_aggregates(db):

    revenue = db.query(
        func.sum(Order.amount)
    ).scalar() or 0

    refunds = db.query(
        func.sum(Refund.refund_amount)
    ).scalar() or 0

    return {
        "revenue": revenue,
        "refunds": refunds,
        "net_revenue":
            revenue - refunds
    }