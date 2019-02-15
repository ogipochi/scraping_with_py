from datetime import datetime,timezone,timedelta

def get_js_datetime_now(milliseconds=1,microseconds=0,adjust=True):
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