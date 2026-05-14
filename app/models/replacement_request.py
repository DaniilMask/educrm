"""
Файл app/models/replacement_request.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.database import Base


class ReplacementRequest(Base):
    __tablename__ = "replacement_requests"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    requested_by_teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    substitute_teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")
    comment = Column(Text, nullable=True)
    created_at = Column(Date, nullable=False)
