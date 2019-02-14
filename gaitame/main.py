import requests
import pandas as pd
import datetime
import time
import os

TOKEN_INITIAL = 1550098778572

def scraping_chart_data(token,token_increment = 2):
    nations = [
    "eurjpy","usdjpy","eurusd","gdpjpy","cadjpy",
    "chfjpy","gdpusd","usdchf","sekjpy","nokjpy",
    "tryjpy","zarjpy","mxnjpy","audjpy","nzdjpy",
    "audusd","nzdusd","euraud","cnhjpy","hkdjpy"]
    
    DATA_DIR = "chart_data_gaitame"
    url = "https://navi.gaitame.com/v2/info/prices/chart"
    df_base = False
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    for nation in nations:
        token += token_increment
        payloads = {
            "pair": "usdjpy",
        "type": "1",
        "count": "400",
        "bid": "true",
        "ask": "true",
        "_": token
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
    return token
def scraping_buysell():
    """
    売買比率を確認
    """

    url = "https://navi.gaitame.com/v2/info/tools/buysell"
    DATA_DIR = "buysell_gaitame"
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
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
token = TOKEN_INITIAL
while True:
    scraping_buysell()
    token = scraping_chart_data(token)
    time.sleep(60*60*6)
    token = scraping_buysell(token) 
    time.sleep(60*60*6)
