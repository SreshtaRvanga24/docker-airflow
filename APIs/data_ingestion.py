import requests
import pandas as pd
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import execute_values

load_dotenv()

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



database = os.getenv("DB_NAME")
port = 5432
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

conn = psycopg2.connect(
    dbname=database,
    user=user,
    password=password,
    host=host,
    port=port
)

def create_table_if_not_exists(table_name, df):
    columns = []
    for col, dtype in df.dtypes.items():
        if "int" in str(dtype):
            sql_type = "BIGINT"
        elif "float" in str(dtype):
            sql_type = "DOUBLE PRECISION"
        else:
            sql_type = "TEXT"
        columns.append(f"{col} {sql_type}")
    
    columns.append("load_date_time TIMESTAMP")
    
    create_query = f"""
        CREATE TABLE IF NOT EXISTS apis.{table_name} (
            {', '.join(columns)}
        );
    """
    curr = conn.cursor()
    curr.execute(create_query)
    conn.commit()

def ingest_data_to_db(table_name, df):
    cols = list(df.columns)
    values = [tuple(row) for row in df.to_numpy()]

    query = f"""
        INSERT INTO apis.{table_name} ({', '.join(cols)})
        VALUES %s
    """

    curr = conn.cursor()
    execute_values(curr, query, values)
    conn.commit()
    curr.close()

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
            create_table_if_not_exists(endpoint, df)
            df["load_date_time"] = datetime.now()
            ingest_data_to_db(endpoint, df)
            print(f'Data from {endpoint}:', df)
        else:
            print(f'No Data From {endpoint}')
main()
conn.close()
