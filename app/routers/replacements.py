from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.lesson import Lesson
from app.models.replacement_request import ReplacementRequest
from app.schemas.replacement_request import (
    ReplacementRequestCreate,
    ReplacementRequestResponse,
    ReplacementRequestReview,
)

router = APIRouter(prefix="/replacement-requests", tags=["Replacements"])


@router.post("/", response_model=ReplacementRequestResponse)
def create_request(payload: ReplacementRequestCreate, db: Session = Depends(get_db)):
    row = ReplacementRequest(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/", response_model=list[ReplacementRequestResponse])
def list_requests(db: Session = Depends(get_db)):
    return db.query(ReplacementRequest).all()


@router.post("/{request_id}/review", response_model=ReplacementRequestResponse)
def review_request(request_id: int, payload: ReplacementRequestReview, db: Session = Depends(get_db)):
    row = db.get(ReplacementRequest, request_id)
    if not row:
        raise HTTPException(status_code=404, detail="Replacement request not found")

    row.status = "approved" if payload.approve else "rejected"
    if payload.approve:
        lesson = db.get(Lesson, row.lesson_id)
        if lesson:
            lesson.replacement_teacher_id = row.substitute_teacher_id

    db.commit()
    db.refresh(row)
    return row
