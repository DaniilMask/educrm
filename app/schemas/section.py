"""
Файл app/schemas/section.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class SectionCreate(BaseModel):
    name: str
    branch_id: int
    teacher_id: Optional[int] = None
    start_date: Optional[date] = None
    weekday: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None


class ReplacementRequest(BaseModel):
    lesson_date: date
    substitute_teacher_id: int


class ReplacementConfirm(BaseModel):
    approve: bool


class SectionResponse(SectionCreate):
    id: int
    substitute_teacher_id: Optional[int] = None

    class Config:
        from_attributes = True
