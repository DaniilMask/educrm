from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.dependencies import get_db

from app.models.user import User

from app.schemas.user import UserCreate

from app.security import hash_password

router = APIRouter()


@router.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.execute(
        select(User).where(User.phone == user.phone)
    ).scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone already exists"
        )

    db_user = User(
        full_name=user.full_name,
        role=user.role,
        phone=user.phone,
        password_hash=hash_password(user.password)
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return {
        "id": db_user.id,
        "full_name": db_user.full_name
    }