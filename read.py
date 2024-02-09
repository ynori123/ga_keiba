
from model.horse import Horse
from model.race import Race


def fetch_data(session, course, distance, is_dart):
    """コース・距離・馬場別のデータ取得

    :返すデータ
    Horse.arrival,
    Horse.jockey_id, 
    Horse.weight, 
    Horse.frame_number,
    Horse.handicap, 
    Horse.odds, 
    Horse.popularity, 
    Horse.age,
    Race.state_id
    """
    query = session.query(
        Horse.arrival,
        Horse.race_id,
        Horse.jockey_id, 
        Horse.weight, 
        Horse.frame_number,
        Horse.handicap, 
        Horse.odds, 
        Horse.popularity, 
        Horse.age,
        Race.state_id
    ).join(Race, Horse.race_id == Race.id
    )#.filter_by(course=course, distance=distance, is_dart=is_dart)
    data = query.all()
    # print(len(data))  # クエリのレコード数を表示
    return data

def fetch_data_with_id(session, race_id):
    """コース・距離・馬場別のデータ取得

    :返すデータ
    Horse.arrival,
    Horse.jockey_id, 
    Horse.weight, 
    Horse.frame_number,
    Horse.handicap, 
    Horse.odds, 
    Horse.popularity, 
    Horse.age,
    Race.state_id
    """
    query = session.query(
        Horse.arrival,
        Horse.race_id,
        Horse.jockey_id, 
        Horse.weight, 
        Horse.frame_number,
        Horse.handicap, 
        Horse.odds, 
        Horse.popularity, 
        Horse.age,
        Race.state_id
    ).filter_by(race_id=race_id).join(Race, Horse.race_id == Race.id
    )
    data = query.all()
    # print(len(data))  # クエリのレコード数を表示
    return data
