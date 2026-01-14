import psycopg2
import pandas as pd
import io
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")


conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

def read_data_from_csv(file_path):
    return pd.read_csv(file_path)

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
    
    columns.append("load_date TIMESTAMP")
    
    create_query = f"""
        CREATE TABLE IF NOT EXISTS public.{table_name} (
            {', '.join(columns)}
        );
    """
    curr = conn.cursor()
    curr.execute(create_query)
    conn.commit()
    curr.close()

def ingest_csv_to_db(table_name, df):
    load_date = datetime.datetime.now()
    df['load_date'] = load_date
    
    buffer = io.StringIO()
    # Convert DataFrame → CSV (in memory)
    df.to_csv(buffer, index=False, header=False)  # Changed header=False
    buffer.seek(0)
    
    curr = conn.cursor()
    
    # Get column names in the correct order
    columns = list(df.columns)
    
    copy_query = f"""
        COPY public.{table_name} ({', '.join(columns)})
        FROM STDIN
        WITH CSV
    """
    curr.copy_expert(copy_query, buffer)
    conn.commit()
    curr.close()

def main():
    tables = [
        "products",
        "customers",
        "stores",
        "suppliers",
        "inventory",
        "transactions",
        "returns",
        "promotions"
    ]
    
    for table in tables:
        file_path = f"./data/{table}.csv"
        df = read_data_from_csv(file_path)
        create_table_if_not_exists(table, df)
        ingest_csv_to_db(table, df)
        print(f"Ingested data into {table} table.")

# main()

query = "SELECT count(product_id) FROM public.products"
curr = conn.cursor()
curr.execute(query)
print(curr.fetchall())

conn.close()