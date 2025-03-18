import pandas as pd
from db_connection import create_connection

def insert_into_staging(connection, table_name, df):
    cursor = connection.cursor()
    for _, row in df.iterrows():
        columns = ", ".join(df.columns)
        values = ", ".join(["%s"] * len(row))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(sql, tuple(row))
    connection.commit()
    cursor.close()
