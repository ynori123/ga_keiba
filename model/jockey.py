from database import Base
from sqlalchemy import Column, Integer, String


class Jockey(Base):
    __tablename__ = "jockeys"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(64))
