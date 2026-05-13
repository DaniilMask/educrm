from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    role: str
    phone: str
    password: str


class UserLogin(BaseModel):
    phone: str
    password: str