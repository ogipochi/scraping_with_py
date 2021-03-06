import requests
import pandas as pd

from datetime import datetime,timezone,timedelta
from general import get_js_datetime_now
import time
import os



def scraping_chart_data():
    nations = [
    "eurjpy","usdjpy","eurusd","cadjpy",
    "chfjpy","usdchf","sekjpy","nokjpy",
    "tryjpy","zarjpy","mxnjpy","audjpy","nzdjpy",
    "audusd","nzdusd","euraud","cnhjpy","hkdjpy"]
    
    DATA_DIR = "chart_data_gaitame"
    url = "https://navi.gaitame.com/v2/info/prices/chart"
    df_base = False
    JST = timezone(timedelta(hours=+9),'JST')
    now = datetime.now(JST).strftime("%Y%m%d_%H%M")
    for nation in nations:
        payloads = {
            "pair": nation,
        "type": "1",
        "count": "400",
        "bid": "true",
        "ask": "true",
        "_": get_js_datetime_now()
        }
        response = requests.get(
            url,
            params = payloads
        )
        if response.status_code != 200:
            print(response)
        if not os.path.isdir(os.path.join(DATA_DIR,nation)):
            os.makedirs(os.path.join(DATA_DIR,nation))
        df = pd.DataFrame(response.json()["data"])
        df.to_csv(os.path.join(DATA_DIR,nation,"{}.csv".format(now)))
        
        time.sleep(3)
    print("ended chart data")

scraping_chart_data()
