
from database import SessionLocal
from model.race import Race
from model.state import State
from sqlalchemy import or_


with SessionLocal() as db:
    # レコードを取得
    matches = db.query(Race).filter(
        or_(
            Race.course == "阪神1",
            Race.course == "中京1",
            Race.course == "京都1", 
            Race.course == "東京1"
        )
    ).all()

    # 各レコードの `course` から "1" を削除
    for match in matches:
        if match.course.endswith("1"):
            match.course = match.course[:-1]  # 末尾の "1" を削除

    # 変更をコミット
    db.commit()
