from app.db.models import Order, Refund, Customer
from sqlalchemy import Index

order_indexes = [
    Index("idx_orders_customer", Order.customer_id),
    Index("idx_orders_date", Order.order_date),
]

refund_indexes = [
    Index("idx_refunds_order", Refund.order_id),
]