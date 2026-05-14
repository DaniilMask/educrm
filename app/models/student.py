"""
Файл app/models/student.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

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

    parents = relationship("Parent", secondary="parent_students", back_populates="children")
