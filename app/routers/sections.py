"""
Файл app/routers/sections.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.section import Section
from app.schemas.section import ReplacementConfirm, ReplacementRequest, SectionCreate, SectionResponse

router = APIRouter(prefix="/sections", tags=["Sections"])

replacement_requests: dict[tuple[int, date], int] = {}


@router.post("/", response_model=SectionResponse)
def create_section(payload: SectionCreate, db: Session = Depends(get_db)):
    section = Section(**payload.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


@router.get("/", response_model=list[SectionResponse])
def list_sections(db: Session = Depends(get_db)):
    return db.query(Section).all()


@router.post("/{section_id}/replacement/request")
def request_replacement(section_id: int, payload: ReplacementRequest, db: Session = Depends(get_db)):
    section = db.get(Section, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    replacement_requests[(section_id, payload.lesson_date)] = payload.substitute_teacher_id
    return {"status": "pending_confirmation"}


@router.post("/{section_id}/replacement/confirm")
def confirm_replacement(
    section_id: int,
    lesson_date: date,
    payload: ReplacementConfirm,
    db: Session = Depends(get_db),
):
    section = db.get(Section, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    key = (section_id, lesson_date)
    substitute_id = replacement_requests.get(key)
    if substitute_id is None:
        raise HTTPException(status_code=404, detail="Replacement request not found")

    if payload.approve:
        section.substitute_teacher_id = substitute_id
        db.commit()
        db.refresh(section)
        replacement_requests.pop(key, None)
        return {"status": "confirmed", "substitute_teacher_id": substitute_id}

    replacement_requests.pop(key, None)
    return {"status": "rejected"}
