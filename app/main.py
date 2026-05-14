"""
Файл app/main.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

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

# Эти импорты моделей нужны, чтобы SQLAlchemy "увидел" таблицы при create_all.
# Проще говоря: без импорта класс может не загрузиться, и таблица не создастся.
from app.models.student import Student  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.parent import Parent  # noqa: F401
from app.models.branch import Branch  # noqa: F401
from app.models.section import Section  # noqa: F401


# Создаем приложение FastAPI.
# Это "сердце" нашего бэкенда: сюда подключаются маршруты (API-ручки).
app = FastAPI()

# Берем список разрешенных адресов фронтенда из переменной окружения.
# Если переменной нет — используем безопасное значение для локальной разработки.
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

# Добавляем CORS-настройки.
# CORS — это правило браузера: можно ли сайту с одного адреса обращаться к API на другом адресе.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Флаг: автоматически создавать таблицы или нет.
# Обычно в проде лучше миграции (alembic), а не auto create.
AUTO_CREATE_TABLES = os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true"
if AUTO_CREATE_TABLES:
    # Создаем таблицы по описанию моделей, если их еще нет.
    Base.metadata.create_all(bind=engine)


# Подключаем все модули API (роутеры).
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(parents.router)
app.include_router(branches.router)
app.include_router(sections.router)


@app.get("/")
def root():
    # Простой "проверочный" маршрут.
    # Нужен, чтобы быстро понять: сервер жив и отвечает.
    return {
        "status": "ok"
    }
