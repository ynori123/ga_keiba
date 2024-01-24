import sys
from database import Base, engine, SessionLocal
from model.horse import Horse
from model.jockey import Jockey
from model.race import Race
from model.state import State


def main(args):
    if len(args) >= 2 and "migrate" in args[1:] :
        if "-d" in args[1:]:
            print("Dropping all tables...")
            Base.metadata.drop_all(bind=engine)
        migrate()
        init_data()
    return

def migrate():
    print("Migrating database...")
    Base.metadata.create_all(bind=engine, tables=[Jockey.__table__])
    Base.metadata.create_all(bind=engine, tables=[State.__table__])
    Base.metadata.create_all(bind=engine, tables=[Race.__table__])
    Base.metadata.create_all(bind=engine, tables=[Horse.__table__])
    print("Database migrated successfully!")

def init_data():
    print("Initializing data...")
    with SessionLocal() as db:
        db.add(State(name="良"))
        db.add(State(name="稍重"))
        db.add(State(name="重"))
        db.add(State(name="不良"))
        db.commit()
    print("Data initialized successfully!")

if __name__ == "__main__":
    args = sys.argv
    main(args)
