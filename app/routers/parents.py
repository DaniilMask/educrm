from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.parent import Parent
from app.models.student import Student
from app.schemas.parent import ParentAttachChildren, ParentCreate, ParentResponse

router = APIRouter(prefix="/parents", tags=["Parents"])


@router.post("/", response_model=ParentResponse)
def create_parent(payload: ParentCreate, db: Session = Depends(get_db)):
    children = []
    if payload.student_ids:
        children = db.query(Student).filter(Student.id.in_(payload.student_ids)).all()
    parent = Parent(full_name=payload.full_name, phone=payload.phone, children=children)
    db.add(parent)
    db.commit()
    db.refresh(parent)
    return ParentResponse(
        id=parent.id,
        full_name=parent.full_name,
        phone=parent.phone,
        student_ids=[s.id for s in parent.children],
    )


@router.get("/", response_model=list[ParentResponse])
def list_parents(db: Session = Depends(get_db)):
    parents = db.query(Parent).all()
    return [
        ParentResponse(
            id=p.id,
            full_name=p.full_name,
            phone=p.phone,
            student_ids=[s.id for s in p.children],
        )
        for p in parents
    ]


@router.put("/{parent_id}/children", response_model=ParentResponse)
def set_parent_children(parent_id: int, payload: ParentAttachChildren, db: Session = Depends(get_db)):
    parent = db.get(Parent, parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    children = db.query(Student).filter(Student.id.in_(payload.student_ids)).all()
    parent.children = children
    db.commit()
    db.refresh(parent)
    return ParentResponse(
        id=parent.id,
        full_name=parent.full_name,
        phone=parent.phone,
        student_ids=[s.id for s in parent.children],
    )
