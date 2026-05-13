from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    parent_name = Column(String, nullable=True)
    parent_phone = Column(String, nullable=True)

    status = Column(String, default="active")

    notes = Column(Text, nullable=True)