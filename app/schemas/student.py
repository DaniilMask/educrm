from pydantic import BaseModel
from typing import Optional


class StudentCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    notes: Optional[str] = None


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    full_name: str
    phone: Optional[str]
    parent_name: Optional[str]
    parent_phone: Optional[str]
    status: str
    notes: Optional[str]

    class Config:
        from_attributes = True