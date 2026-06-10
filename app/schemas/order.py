from pydantic import BaseModel


class OrderSchema(BaseModel):
    id: int
    customer_id: int
    amount: float

    class Config:
        from_attributes = True