"""
Файл app/schemas/lesson.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class LessonCreate(BaseModel):
    section_id: int
    teacher_id: Optional[int] = None
    date: date
    start_time: time
    end_time: time
    status: str = "scheduled"


class LessonResponse(LessonCreate):
    id: int
    replacement_teacher_id: Optional[int] = None

    class Config:
        from_attributes = True
