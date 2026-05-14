from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time

from app.database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    substitute_teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    start_date = Column(Date, nullable=True)
    weekday = Column(String, nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
