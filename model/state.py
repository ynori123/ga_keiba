from sqlalchemy import Column, Integer, String
from database import Base


class State(Base):
    __tablename__ = "states"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(64))
