from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.parent import Parent
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


def cleanup_orphan_parents(db: Session):
    parents = db.query(Parent).all()
    for parent in parents:
        active_children = [child for child in parent.children if child.status == "active"]
        if len(active_children) == 0:
            db.delete(parent)


@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    payload = student.model_dump(exclude={"parent_id"})
    db_student = Student(**payload)

    db.add(db_student)
    db.flush()

    parent = None
    if student.parent_id:
        parent = db.get(Parent, student.parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")
    elif student.parent_name and student.parent_phone:
        parent = (
            db.query(Parent)
            .filter(Parent.full_name == student.parent_name, Parent.phone == student.parent_phone)
            .first()
        )
        if not parent:
            parent = Parent(full_name=student.parent_name, phone=student.parent_phone)
            db.add(parent)
            db.flush()

    if parent:
        parent.children.append(db_student)

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

    cleanup_orphan_parents(db)
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
    cleanup_orphan_parents(db)
    db.commit()

    return {
        "message": "Student deleted"
    }
