
from pydantic import BaseModel


class CustomerSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True