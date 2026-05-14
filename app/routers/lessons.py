"""
Файл app/routers/lessons.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonResponse

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.post("/", response_model=LessonResponse)
def create_lesson(payload: LessonCreate, db: Session = Depends(get_db)):
    lesson = Lesson(**payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.get("/", response_model=list[LessonResponse])
def list_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()
