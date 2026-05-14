from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    student_id: int
    amount: Decimal
    payment_date: date
    method: str
    comment: Optional[str] = None


class PaymentResponse(PaymentCreate):
    id: int

    class Config:
        from_attributes = True
