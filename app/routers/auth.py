from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.dependencies import get_current_user, get_db

from app.models.user import User

from app.schemas.user import UserLogin

from app.security import verify_password

from app.auth import create_access_token

router = APIRouter()


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.execute(
        select(User).where(
            User.phone == user.phone
        )
    ).scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "phone": current_user.phone
    }