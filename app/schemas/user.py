"""
Файл app/schemas/user.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    role: str
    phone: str
    password: str


class UserLogin(BaseModel):
    phone: str
    password: str