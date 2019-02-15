import requests
import pandas as pd

from datetime import datetime,timezone,timedelta
import time
import os

def _get_js_datetime_now(milliseconds=1,microseconds=0,adjust=True):
    """
    JSベースの現在時刻を取得
    """
    JST = timezone(timedelta(hours=+9),'JST')
    base = datetime(1970,1,1,0,0,0,0,JST)
    now = datetime.now(JST)
    jst_delta = 60 * 60 * 9 *1000* (milliseconds) + 60 * 60*(microseconds)
    if adjust:
        jst_delta += 1000000   # ラグの部分の調整
    delta = int(((now - base)/timedelta(milliseconds=milliseconds,microseconds=microseconds)))
    delta = delta - jst_delta
    return delta

def scraping_chart_data():
    nations = [
    "eurjpy","usdjpy","eurusd","gdpjpy","cadjpy",
    "chfjpy","gdpusd","usdchf","sekjpy","nokjpy",
    "tryjpy","zarjpy","mxnjpy","audjpy","nzdjpy",
    "audusd","nzdusd","euraud","cnhjpy","hkdjpy"]
    
    DATA_DIR = "chart_data_gaitame"
    url = "https://navi.gaitame.com/v2/info/prices/chart"
    df_base = False
    now = datetime.now().strftime("%Y%m%d_%H%M")
    for nation in nations:
        token += token_increment
        payloads = {
            "pair": nation,
        "type": "1",
        "count": "500",
        "bid": "true",
        "ask": "true",
        "_": _get_js_datetime_now()
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
def sample_print():
    print("hello")