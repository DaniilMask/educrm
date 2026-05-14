"""
Файл app/models/attendance.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint

from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("lesson_id", "student_id", name="uq_attendance_lesson_student"),)

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    status = Column(String, nullable=False)
    comment = Column(Text, nullable=True)
