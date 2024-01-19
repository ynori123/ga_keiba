from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class Race(Base):
    __tablename__ = "races"
    id: int = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    state_id: int = Column(ForeignKey("states.id"))
    course: str = Column(String(64))
    is_dart: bool = Column(Boolean)
    is_right: bool = Column(Boolean)
    distance: int = Column(Integer)
    weather: str = Column(String(64))

    def show(self):
        print(
            f"id: {self.id}, state_id: {self.state_id}, course: {self.course}, is_dart: {self.is_dart}, is_right: {self.is_right}, distance: {self.distance}, weather: {self.weather}"
        )
