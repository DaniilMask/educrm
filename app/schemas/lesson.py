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
