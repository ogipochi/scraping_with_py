import requests
import pandas as pd

from datetime import datetime,timezone,timedelta
import time
import os

def scraping_buysell():
    """
    売買比率を確認
    """

    url = "https://navi.gaitame.com/v2/info/tools/buysell"
    DATA_DIR = "buysell_gaitame"
    now = datetime.now().strftime("%Y%m%d_%H%M")
    nations = [
    "eurjpy","usdjpy","eurusd","cadjpy",
    "chfjpy","usdchf","sekjpy","nokjpy",
    "tryjpy","zarjpy","mxnjpy","audjpy","nzdjpy",
    "audusd","nzdusd","euraud","cnhjpy","hkdjpy"]
    for nation in nations:
        payloads = {
            "order": "entryclose",
            "interval": "hour",
            "pairs": nation
        }
        response = requests.get(
            url,
            params = payloads
        )
        if response.status_code != 200:
            print(response,nation)
            continue
        if not os.path.isdir(os.path.join(DATA_DIR,nation)):
            os.makedirs(os.path.join(DATA_DIR,nation))
        response_data = response.json()["data"][0]["ratios"]
        response_data_normalized = []
        for d in response_data:
            response_data_normalized.append({
                "entry_buy":d["entry"]["buy"],
                "entry_sell":d["entry"]["sell"],
                "close_buy":d["close"]["buy"],
                "close_sell":d["close"]["sell"],
            })
        df = pd.DataFrame(response_data_normalized)
        df.to_csv(os.path.join(DATA_DIR,nation,"{}.csv".format(now)))
        time.sleep(3)
    print("ended buysell")

scraping_buysell()
