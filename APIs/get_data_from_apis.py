import requests
import pandas as pd
import json
from typing import Optional, Dict, List, Any
from datetime import datetime

url = 'http://localhost:8000'
endpoints = [
"products",
"customers",
"stores",
"suppliers",
"inventory",
"transactions",
"returns",
"promotions"]


def get_data_from_api(endpoint, params):
    response = requests.get(f'{url}/{endpoint}')
    if response.status_code == 200:
        return pd.DataFrame(response.json()['data'])
    else:
        print(f"Failed to fetch data from {endpoint}. Status code: {response.status_code}")
        return pd.DataFrame()
    
def main():
    for endpoint in endpoints:
        df = get_data_from_api(endpoint, params = {"limit":10, "offset":0})
        if not df.empty:
            
            print(f'Data from {endpoint}:', df)
        else:
            print(f'No Data From {endpoint}')
main()