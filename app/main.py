import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base
from app.database import engine

from app.routers import users
from app.routers import auth
from app.routers import students
from app.routers import parents
from app.routers import branches
from app.routers import sections

from app.models.student import Student
from app.models.user import User
from app.models.parent import Parent
from app.models.branch import Branch
from app.models.section import Section


app = FastAPI()

CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTO_CREATE_TABLES = os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true"
if AUTO_CREATE_TABLES:
    Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(parents.router)
app.include_router(branches.router)
app.include_router(sections.router)


@app.get("/")
def root():
    return {
        "status": "ok"
    }