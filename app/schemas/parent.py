"""
Файл app/schemas/parent.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from pydantic import BaseModel


class ParentCreate(BaseModel):
    full_name: str
    phone: str
    student_ids: list[int] = []


class ParentResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    student_ids: list[int]


class ParentAttachChildren(BaseModel):
    student_ids: list[int]
