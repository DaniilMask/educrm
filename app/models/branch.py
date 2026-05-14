from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    kind = Column(String, nullable=False)  # school | studio
    sections_info = Column(Text, nullable=True)
    rent_model = Column(String, nullable=False)  # fixed | percent | custom
    rent_details = Column(Text, nullable=True)
    free_time_schedule = Column(Text, nullable=True)
