from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    payment = Payment(**payload.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@router.get("/", response_model=list[PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


@router.get("/students/{student_id}/balance")
def student_balance(student_id: int, db: Session = Depends(get_db)):
    paid = db.query(func.coalesce(func.sum(Payment.amount), Decimal("0"))).filter(Payment.student_id == student_id).scalar()
    return {"student_id": student_id, "paid": str(paid)}
