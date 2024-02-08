from io import StringIO
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from database import SessionLocal
from model.horse import Horse
from model.jockey import Jockey

urllib3.disable_warnings(InsecureRequestWarning)

states = ["良", "稍重", "重", "不良"]
sexes = ["牡", "牝", "セ"]
def fetch_test_data(db, url):
    req = requests.get(url=url, verify=False)
    req.encoding = "EUC-JP"
    data = pd.read_html(StringIO(req.text))
    # print(type(data[0]))
    soup = BeautifulSoup(req.text, "html.parser")
    race_name = soup.select('#main > div > div > div > diary_snap > div > div > dl > dd > h1')[0].contents[0]
    race_info = soup.select('#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span')[0].contents[0]
    state = race_info.split()[8] if race_info.split()[8] != ":" else race_info.split()[9]
    state_id = states.index(state) + 1
    course = soup.select('#main > div > div > div > diary_snap > div > div > p')[0].contents[0]
    is_right = race_info[1] == "右"
    course_name = course.split()[1][course.split()[1].index("回")+1:course.split()[1].index("日")-1]
    race_distance = re.search(r"\d+", race_info).group()
    # print(re.search(r"\d+", race_info).group())
    weather = re.search(r"天候\s*:\s*(\S+)", race_info).group(1)
    
    if race_info[0] == "ダ":
        is_dart = True
    elif race_info[0] == "芝":
        is_dart = False
    else: return None # 芝ダ以外は無視
    
    arr = []
    
    for id,record in data[0].iterrows():
        jockey_name = record.iloc[6]
        if db.query(Jockey).filter_by(name=jockey_name).first() == None:
            jockey = Jockey(name=jockey_name)
            db.add(jockey)
            db.commit()
        else:
            jockey = db.query(Jockey).filter_by(name=jockey_name).first()
        
        weight_str = str(record.iloc[11])
        # print(weight_str)
        weight_match = re.match(r"^\d+", weight_str)
        if weight_match:
            weight = int(weight_match.group())
        else:
            weight = None

        age_str = str(record.iloc[4])
        age_match = re.search(r"(?:牡|牝|セ)(\d+)", age_str)
        if age_match:
            age = int(age_match.group(1))
        else:
            age = None
        sex_id = sexes.index(record.iloc[4][0]) + 1

        horse = Horse(jockey_id=jockey.id, frame_number=record.iloc[2], arrival=record.iloc[0], name=record.iloc[3], odds=record.iloc[9], popularity=record.iloc[10], handicap=record.iloc[5], weight=weight, age=age, sex_id=sex_id)
        # print(horse.show())
        arr.append([horse.arrival, horse.jockey_id, horse.weight, horse.frame_number, horse.handicap, horse.odds, horse.popularity, horse.age, state_id])
        # print(record.iloc[:])
    columns = ['arrival', 'jockey_id', 'weight', 'frame_number', 'handicap', 'odds', 'popularity', 'age', 'state_id']
    # print(arr)
    res = pd.DataFrame(data=arr, columns=columns)
    return res

def get_test_data():
    with SessionLocal() as db:
        data = fetch_test_data(db=db, url="https://db.netkeiba.com/race/202206010608")
    print(data)
    # data = data.sample(frac=1).reset_index(drop=True)
    test_true = data['arrival']
    test_data = data.drop(['arrival', 'popularity'], axis=1)
    return test_data,test_true
    # https://db.netkeiba.com/race/202406010707
