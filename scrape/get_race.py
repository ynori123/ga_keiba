import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
from calendar import isleap
import time
import re
from tqdm import tqdm


def get_raceid_list_from_date(today: datetime.date, cnt: int)-> {list[str], int}:
    date = f'{today.year:04}{today.month:02}{today.day:02}'
    url = 'https://db.netkeiba.com/race/list/' + date
    html = requests.get(url)
    html.encoding = "EUC-JP"
    soup = BeautifulSoup(html.text, "html.parser")
    race_list = soup.find('div', attrs={"class": 'race_list fc'})
    if race_list is None:
        cnt += 1
        return {"res": list(), "cnt": cnt}
    else:
        cnt = 0
    a_tag_list = race_list.find_all('a')
    href_list = [a_tag.get('href') for a_tag in a_tag_list]
    race_id_list = list()
    for href in href_list:
        for race_id in re.findall('[0-9]{12}', href):
            race_id_list.append(race_id)
    return {"res":list(set(race_id_list)), "cnt": cnt}

def scraping_race_id_list(year: int)-> list[str]:
    cnt: int = 0
    today = datetime.date.today()
    get_day = datetime.date(year, 1, 1)
    race_id_list = list()
    is_end = False
    for _ in tqdm(range(366 if isleap(year) else 365), desc="日"):
        if not is_end:
            res = get_raceid_list_from_date(get_day, cnt=cnt)
            race_id_list += res.get("res")
            cnt = res.get("cnt")
            get_day = get_day + relativedelta(days=1)
            if cnt >= 10:
                # 10日連続でレースがなかったら終了
                is_end = True
            if get_day > today:
                # 今日より先の日付になったら終了
                break
            time.sleep(1)
    return race_id_list
