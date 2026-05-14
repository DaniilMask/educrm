from datetime import date
from typing import Optional

from pydantic import BaseModel


class ReplacementRequestCreate(BaseModel):
    lesson_id: int
    requested_by_teacher_id: int
    substitute_teacher_id: int
    comment: Optional[str] = None
    created_at: date


class ReplacementRequestReview(BaseModel):
    approve: bool


class ReplacementRequestResponse(ReplacementRequestCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
