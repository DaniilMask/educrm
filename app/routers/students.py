from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.student import Student

from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate
)

router = APIRouter(
    prefix="/students",
    tags=["Children"]
)


@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    db_student = Student(**student.model_dump())

    db.add(db_student)

    db.commit()

    db.refresh(db_student)

    return db_student


@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.get("/stats/summary")
def get_students_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    group_name: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    total = db.query(func.count(Student.id)).scalar() or 0
    active = (
        db.query(func.count(Student.id))
        .filter(Student.status == "active")
        .scalar()
        or 0
    )
    inactive = total - active

    return {
        "total_children": total,
        "active_children": active,
        "inactive_children": inactive,
        "start_date": start_date,
        "end_date": end_date,
        "group_name": group_name
    }


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_values = updated_data.model_dump(exclude_unset=True)
    if not update_values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    for key, value in update_values.items():
        setattr(student, key, value)

    db.commit()

    db.refresh(student)

    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)

    db.commit()

    return {
        "message": "Student deleted"
    }