from fastapi import FastAPI

from app.db.database import engine
from app.db.models import Base

from app.api.customers import router as customer_router
from app.api.orders import router as order_router
from app.api.refunds import router as refund_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title="Backend Assignment",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(customer_router)
app.include_router(order_router)
app.include_router(refund_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "Backend Assignment Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

