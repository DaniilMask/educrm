from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.database import SessionLocal

from app.models.user import User

from app.schemas import UserCreate

from app.security import hash_password

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/users")
def create_user(user: UserCreate):

    db: Session = SessionLocal()

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
