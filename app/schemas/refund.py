
from pydantic import BaseModel


class RefundSchema(BaseModel):
    id: int
    order_id: int
    refund_amount: float

    class Config:
        from_attributes = True