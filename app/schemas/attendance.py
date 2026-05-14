"""
Файл app/schemas/attendance.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from typing import Optional

from pydantic import BaseModel


class AttendanceUpsert(BaseModel):
    lesson_id: int
    student_id: int
    status: str
    comment: Optional[str] = None


class AttendanceResponse(AttendanceUpsert):
    id: int

    class Config:
        from_attributes = True
