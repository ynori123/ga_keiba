from database import SessionLocal
from model.race import Race
from model.state import State
from sqlalchemy import and_


cs = ["阪神", "中京", "京都", "東京", "新潟", "小倉", "福島", "中山", "札幌", "函館"]
distances = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2500, 3200]

dictionaly = {}
with SessionLocal() as db:
    # レコードを取得
    for c in cs:
        for d in distances:
            cnt = db.query(Race).filter(and_(Race.course==c, Race.distance==d, Race.is_dart==True)).count()
            dictionaly.update({c+str(d)+"ダ": cnt})
            cnt = db.query(Race).filter(and_(Race.course==c, Race.distance==d, Race.is_dart==False)).count()
            dictionaly.update({c+str(d)+"芝": cnt})

l = sorted(dictionaly.items(), key=lambda x: x[1], reverse=True)
for i,[k,v] in enumerate(l):
    print(k, v)
    if i > 10:
        break
