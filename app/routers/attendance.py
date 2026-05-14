from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceResponse, AttendanceUpsert

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=AttendanceResponse)
def upsert_attendance(payload: AttendanceUpsert, db: Session = Depends(get_db)):
    row = (
        db.query(Attendance)
        .filter(Attendance.lesson_id == payload.lesson_id, Attendance.student_id == payload.student_id)
        .first()
    )
    if row:
        row.status = payload.status
        row.comment = payload.comment
    else:
        row = Attendance(**payload.model_dump())
        db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/lesson/{lesson_id}", response_model=list[AttendanceResponse])
def list_attendance_for_lesson(lesson_id: int, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.lesson_id == lesson_id).all()
