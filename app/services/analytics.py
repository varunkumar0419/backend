
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

from app.db.database import get_db
from app.db.models import Order, Refund
from app.core.cache import get_cache, set_cache

router = APIRouter(tags=["Analytics"])

logger = logging.getLogger(__name__)


@router.get("/analytics/summary")
def analytics_summary(db: Session = Depends(get_db)):
    try:
        cache_key = "analytics_summary"

        cached = get_cache(cache_key)
        if cached:
            return {
                "source": "cache",
                "data": cached
            }

        total_orders = (
            db.query(func.count(Order.id))
            .scalar()
            or 0
        )

        total_revenue = (
            db.query(func.sum(Order.amount))
            .scalar()
            or 0
        )

        total_refunds = (
            db.query(func.sum(Refund.refund_amount))
            .scalar()
            or 0
        )

        average_order_value = (
            total_revenue / total_orders
            if total_orders > 0
            else 0
        )

        result = {
            "total_orders": int(total_orders),
            "total_revenue": float(total_revenue),
            "total_refunds": float(total_refunds),
            "net_revenue": float(
                total_revenue - total_refunds
            ),
            "average_order_value": float(
                average_order_value
            )
        }

        set_cache(
            cache_key,
            result,
            ttl=3600
        )

        return {
            "source": "db",
            "data": result
        }

    except Exception as e:
        logger.exception(
            "Analytics summary failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/analytics/top-customers")
def top_customers(db: Session = Depends(get_db)):
    try:
        cache_key = "top_customers"

        cached = get_cache(cache_key)
        if cached:
            return cached

        result = (
            db.query(
                Order.customer_id,
                func.sum(Order.amount).label(
                    "total_spend"
                )
            )
            .group_by(Order.customer_id)
            .order_by(
                func.sum(Order.amount).desc()
            )
            .limit(10)
            .all()
        )

        output = [
            {
                "customer_id": row.customer_id,
                "total_spend": float(
                    row.total_spend
                )
            }
            for row in result
        ]

        set_cache(
            cache_key,
            output,
            ttl=3600
        )

        return output

    except Exception as e:
        logger.exception(
            "Top customers failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/analytics/revenue-trends")
def revenue_trends(db: Session = Depends(get_db)):
    try:
        cache_key = "revenue_trends"

        cached = get_cache(cache_key)
        if cached:
            return {
                "source": "cache",
                "data": cached
            }

        result = (
            db.query(
                func.date_trunc("month", Order.order_date).label("month"),
                func.sum(Order.amount).label("revenue")
            )
            .group_by(func.date_trunc("month", Order.order_date))
            .order_by(func.date_trunc("month", Order.order_date))
            .all()
        )

        output = [
            {
                "month": str(row.month),
                "revenue": float(row.revenue)
            }
            for row in result
        ]

        set_cache(cache_key, output, ttl=3600)

        return {
            "source": "db",
            "data": output
        }

    except Exception as e:
        logger.exception("Revenue trends failed")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/repeat-customer-revenue")
def repeat_customer_revenue(db: Session = Depends(get_db)):
    try:
        cache_key = "repeat_customer_revenue"

        cached = get_cache(cache_key)
        if cached:
            return cached

        result = (
            db.query(
                func.sum(Order.amount)
            )
            .filter(
                Order.customer_id.in_(
                    db.query(Order.customer_id)
                    .group_by(Order.customer_id)
                    .having(func.count(Order.id) > 1)
                )
            )
            .scalar()
        )

        output = {
            "repeat_customer_revenue": float(result or 0)
        }

        set_cache(cache_key, output, ttl=10800)

        return output

    except Exception as e:
        logger.exception("Repeat customer revenue failed")
        raise HTTPException(status_code=500, detail=str(e))