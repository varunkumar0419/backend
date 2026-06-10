
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.db.models import Order, Refund
from app.core.cache import get_cache, set_cache

router = APIRouter()


from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

@router.get("/analytics/summary")
def analytics_summary(db: Session = Depends(get_db)):
    cache_key = "analytics_summary"

    cached = get_cache(cache_key)
    if cached:
        return {"source": "cache", "data": cached}

    total_orders, total_revenue = db.query(
        func.count(Order.id),
        func.coalesce(func.sum(Order.amount), 0)
    ).first()

    total_refunds = db.query(
        func.coalesce(func.sum(Refund.refund_amount), 0)
    ).scalar()

    result = {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "total_refunds": float(total_refunds),
        "net_revenue": float(total_revenue - total_refunds),
        "average_order_value": float(total_revenue / total_orders if total_orders else 0)
    }

    set_cache(cache_key, result, ttl=60)  # reduce TTL for consistency

    return {"source": "db", "data": result}

@router.get("/analytics/top-customers")
def top_customers(db: Session = Depends(get_db)):

    cache_key = "top_customers"
    cached = get_cache(cache_key)
    if cached:
        return cached

    result = (
        db.query(
            Order.customer_id,
            func.sum(Order.amount).label("total_spend")
        )
        .group_by(Order.customer_id)
        .order_by(func.sum(Order.amount).desc())
        .limit(10)
        .all()
    )

    output = [
        {"customer_id": r.customer_id, "total_spend": float(r.total_spend)}
        for r in result
    ]

    set_cache(cache_key, output, ttl=300)

    return output


@router.get("/analytics/revenue-trends")
def revenue_trends(db: Session = Depends(get_db)):

    cache_key = "revenue_trends"
    cached = get_cache(cache_key)
    if cached:
        return {"source": "cache", "data": cached}

    result = (
        db.query(
            func.date_trunc("month", Order.order_date).label("month"),
            func.sum(Order.amount).label("revenue")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    output = [
        {"month": str(r.month), "revenue": float(r.revenue)}
        for r in result
    ]

    set_cache(cache_key, output, ttl=60)

    return {"source": "db", "data": output}


@router.get("/analytics/repeat-customer-revenue")
def repeat_customer_revenue(db: Session = Depends(get_db)):

    cache_key = "repeat_customer_revenue"
    cached = get_cache(cache_key)
    if cached:
        return cached

    subq = (
        db.query(
            Order.customer_id.label("customer_id")
        )
        .group_by(Order.customer_id)
        .having(func.count(Order.id) > 1)
        .subquery()
    )

    result = db.query(
        func.coalesce(func.sum(Order.amount), 0)
    ).filter(
        Order.customer_id.in_(subq)
    ).scalar()

    output = {
        "repeat_customer_revenue": float(result)
    }

    set_cache(cache_key, output, ttl=300)  # increase TTL (important)

    return output