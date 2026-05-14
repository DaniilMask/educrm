from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, Text

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    method = Column(String, nullable=False)
    comment = Column(Text, nullable=True)
