"""
Файл app/routers/students.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

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
    # Ищем родителей без "активных" детей и удаляем их.
    # "Активный" значит status == "active".
    # Это маленькая уборка базы, чтобы не хранить "пустые" записи.
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
    # Получаем данные ученика из входного объекта.
    # parent_id исключаем, потому что это связь, а не поле самой таблицы students.
    payload = student.model_dump(exclude={"parent_id"})
    db_student = Student(**payload)

    # Добавляем ученика в текущую транзакцию.
    db.add(db_student)
    # flush отправляет изменения в БД без финального commit.
    # Это помогает получить id и строить связи дальше.
    db.flush()

    parent = None
    if student.parent_id:
        # Вариант 1: передали id родителя -> ищем его.
        parent = db.get(Parent, student.parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent not found")
    elif student.parent_name and student.parent_phone:
        # Вариант 2: передали имя и телефон родителя.
        # Сначала проверяем, нет ли уже такого родителя.
        parent = (
            db.query(Parent)
            .filter(Parent.full_name == student.parent_name, Parent.phone == student.parent_phone)
            .first()
        )
        if not parent:
            # Если нет — создаем нового.
            parent = Parent(full_name=student.parent_name, phone=student.parent_phone)
            db.add(parent)
            db.flush()

    if parent:
        # Связываем найденного/созданного родителя с учеником.
        parent.children.append(db_student)

    # Подтверждаем все изменения.
    db.commit()

    # Обновляем объект из БД (чтобы вернуть актуальные поля).
    db.refresh(db_student)

    return db_student


@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    # Возвращаем всех учеников.
    return db.query(Student).all()


@router.get("/stats/summary")
def get_students_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    group_name: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    # Пока что это простая статистика:
    # общее число, активные, неактивные.
    # Параметры start_date/end_date/group_name возвращаются как echo (для будущей фильтрации).
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
    # Ищем одного ученика по id.
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
    # Ищем ученика, которого нужно изменить.
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
        # Если клиент не прислал ни одного поля — это ошибка запроса.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    # Применяем все переданные изменения.
    for key, value in update_values.items():
        setattr(student, key, value)

    # После изменений делаем уборку "осиротевших" родителей.
    cleanup_orphan_parents(db)
    db.commit()

    db.refresh(student)

    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    # Ищем ученика перед удалением.
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

    # Удаляем ученика.
    db.delete(student)
    # После удаления снова чистим родителей без активных детей.
    cleanup_orphan_parents(db)
    db.commit()

    return {
        "message": "Student deleted"
    }
