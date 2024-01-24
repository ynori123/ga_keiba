from database import SessionLocal
from scraping import scrape
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning
import urllib3
from settings import BEGIN_YEAR
from datetime import date
from get_race import scraping_race_id_list

urllib3.disable_warnings(InsecureRequestWarning)

states = ["良", "稍重", "重", "不良"]
sexes = ["牡", "牝", "セ"]

def get_all_race_id_list()-> list[str]:
    # レース情報を取得
    start_year = BEGIN_YEAR
    end_year = date.today().year
    race_id_list = []
    for year in tqdm(range(start_year, end_year + 1), desc="年"):
        race_id_list += scraping_race_id_list(year)
    return race_id_list

def main():
    race_id_list = get_all_race_id_list()
    print(race_id_list)
    with SessionLocal() as db:
        for netkeiba_race_id in tqdm(race_id_list, desc="レース"):
            # 中山競馬場
            print(netkeiba_race_id)
            scrape(url=f"https://db.netkeiba.com/race/{netkeiba_race_id}",db=db)

main()
