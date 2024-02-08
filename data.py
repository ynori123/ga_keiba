import pandas as pd
from database import SessionLocal
from read import fetch_data, fetch_data_with_id
from itertools import groupby
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from deap import base, creator, tools, algorithms

def fix_model_data(course, distance, is_dart):
    
    # データの取得と前処理
    with SessionLocal() as db:
        data = fetch_data(db, course, distance, is_dart)
    df = pd.DataFrame(data, columns=['arrival', 'race_id', 'jockey_id', 'weight', 'frame_number', 'handicap', 'odds', 'popularity', 'age', 'state_id'])
    print(df.head())
    # data = group_tuples_by_second_element(data)
    return df

def fix_predict_model_data():
    # データの取得と前処理
    with SessionLocal() as db:
        data = fetch_data_with_id(db, 202306030710)
    df = pd.DataFrame(data, columns=['arrival', 'race_id', 'jockey_id', 'weight', 'frame_number', 'handicap', 'odds', 'popularity', 'age', 'state_id'])
    print(df.head())
    # data = group_tuples_by_second_element(data)
    return df

def group_tuples_by_second_element(tuples):
    # グループ化するために、二つ目の要素でソート
    tuples_sorted = sorted(tuples, key=lambda x: x[1])

    # 二つ目の要素でグループ化
    grouped = [list(group) for _, group in groupby(tuples_sorted, lambda x: x[1])]
    
    return grouped

