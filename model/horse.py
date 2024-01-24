from database import Base
from sqlalchemy import Column, Double, ForeignKey, Integer, String


class Horse(Base):
    __tablename__ = 'horses'
    id: int = Column(Integer, primary_key=True)
    race_id: int = Column(ForeignKey('races.id'))
    jockey_id: int = Column(ForeignKey('jockeys.id'))
    frame_number: int = Column(Integer)
    arrival: int = Column(Integer)
    name: str = Column(String(64))
    odds: float = Column(Double)
    popularity: int = Column(Integer)
    handicap: int = Column(Integer)
    weight: int = Column(Integer)
    age: int = Column(Integer)
    sex_id: int = Column(Integer) # 1: 牡, 2: 牝, 3: セ
    
    def show(self)-> None:
        print(
            f"id:{self.id} race_id:{self.race_id} jockey_id:{self.jockey_id} frame_number:{self.frame_number} age:{self.age} sex_id:{self.sex_id}"
        )
