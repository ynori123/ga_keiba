import numpy as np
import pandas as pd
from database import SessionLocal
from sqlalchemy import and_
from sklearn.preprocessing import StandardScaler, OneHotEncoder

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
    ).filter_by(course=course, distance=distance, is_dart=is_dart)
    data = query.all()
    # print(len(data))  # クエリのレコード数を表示
    return data

def preprocess_data(data):
    df = pd.DataFrame(data, columns=['arrival', 'race_id', 'jockey_id', 'weight', 'frame_number', 'handicap', 'odds', 'popularity', 'age', 'state_id'])
    # print(df.head())
    # エンコーダーとスケーラーの初期化
    encoder = OneHotEncoder()
    scaler = StandardScaler()

    # データの前処理
    categorical_data = encoder.fit_transform(df[['jockey_id', 'state_id']]).toarray()
    numerical_data = scaler.fit_transform(df[['weight', 'handicap', 'odds', 'popularity', 'age']])

    return np.hstack((numerical_data, categorical_data))



# print(raw_data[0][0])
# print(processed_features[:])

# env = HorseRacingEnv(features)

# print(env.reset())
