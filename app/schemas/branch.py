"""
Файл app/schemas/branch.py:
Коротко: этот файл содержит код для части системы.
Ниже в коде добавлены комментарии и понятные имена, чтобы было легче читать.
"""

from typing import Optional

from pydantic import BaseModel


class BranchCreate(BaseModel):
    name: str
    kind: str
    sections_info: Optional[str] = None
    rent_model: str
    rent_details: Optional[str] = None
    free_time_schedule: Optional[str] = None


class BranchResponse(BranchCreate):
    id: int

    class Config:
        from_attributes = True
