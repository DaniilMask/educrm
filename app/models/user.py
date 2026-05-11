from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    full_name = Column(String)

    role = Column(String)

    phone = Column(String)

    password_hash = Column(String)
