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
