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
