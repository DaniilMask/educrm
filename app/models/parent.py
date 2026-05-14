"""
Файл app/models/parent.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


parent_students = Table(
    "parent_students",
    Base.metadata,
    Column("parent_id", ForeignKey("parents.id"), primary_key=True),
    Column("student_id", ForeignKey("students.id"), primary_key=True),
)


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    children = relationship("Student", secondary=parent_students, back_populates="parents")
