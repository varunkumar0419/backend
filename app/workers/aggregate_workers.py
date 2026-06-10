from app.db.database import SessionLocal
from app.db.models import Order, Refund
from sqlalchemy import func


def refresh_aggregates():

    db = SessionLocal()

    try:
        total_orders = db.query(func.count(Order.id)).scalar()
        total_revenue = db.query(func.sum(Order.amount)).scalar()
        total_refunds = db.query(func.sum(Refund.refund_amount)).scalar()

        print({
            "orders": total_orders,
            "revenue": float(total_revenue or 0),
            "refunds": float(total_refunds or 0)
        })

    finally:
        db.close()