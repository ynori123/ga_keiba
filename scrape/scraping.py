from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib3
from sqlalchemy.orm import Session
from urllib3.exceptions import InsecureRequestWarning
from model.horse import Horse
from model.jockey import Jockey
from model.race import Race
from model.state import State
from io import StringIO
import re


urllib3.disable_warnings(InsecureRequestWarning)

states = ["良", "稍重", "重", "不良"]
sexes = ["牡", "牝", "セ"]

def scrape(url: str, db: Session)-> None:
    req = requests.get(url=url, verify=False)
    req.encoding = "EUC-JP"
    data = pd.read_html(StringIO(req.text))
    # print(type(data[0]))
    soup = BeautifulSoup(req.text, "html.parser")
    race = get_race_info(soup, db, url)
    if race is None: return
    # print(race)
    # print(data[0].iterrows())
    get_horse_info(data=data, db=db, race=race)
    
    # print(race.show())
    # print(race_name)
    # print(state)
    return

def get_race_info(soup: BeautifulSoup, db: Session, url: str)-> Race:
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
    
    race = Race(id=url.split("/")[-1], name=race_name, state_id=state_id, course=course_name, is_dart=is_dart, is_right=is_right, distance=race_distance, weather=weather)
    db.add(race)
    db.commit()
    return race

def get_horse_info(data: list[pd.DataFrame], db: Session, race: Race)-> None:
    # print(len(data[0]))
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
        # print(record.iloc[:])
        horse = Horse(race_id=race.id, jockey_id=jockey.id, frame_number=record.iloc[2], arrival=record.iloc[0], name=record.iloc[3], odds=record.iloc[9], popularity=record.iloc[10], handicap=record.iloc[5], weight=weight, age=age, sex_id=sex_id)
        
        try:
            int(horse.arrival)
        except:
            print(f"found horse.arrival is not digit! {horse.arrival}")
            continue
        # horse.show()
        db.add(horse)
        db.commit()
    return

