import requests
import pandas as pd
from config import get_headers

def get_data(url, key):
    try:
        response = requests.get(url, headers=get_headers())
        
        if response.status_code != 200:
            print(f"Xatolik yuz berdi. Status code: {response.status_code}")
            return pd.DataFrame()

        records = response.json()

        if not records or key not in records:
            return pd.DataFrame()

        return pd.json_normalize(records[key])

    except Exception as e:
        print(f"So'rov yuborishda xatolik: {e}")
        return pd.DataFrame()





