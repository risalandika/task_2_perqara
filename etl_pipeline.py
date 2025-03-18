import pandas as pd
from db_connection import create_connection
from load_data import load_data
from staging_etl import insert_into_staging
from transform_load import transform_and_insert_clean_data, create_data_mart

def etl_pipeline():
    connection = create_connection()
    if not connection:
        return
    
    file_paths = {
        "staging_customers": "customers_dataset.csv",
        "staging_geolocation": "geolocation_dataset.csv",
        "staging_order_items": "order_items_dataset.csv",
        "staging_order_payments": "order_payments_dataset.csv",
        "staging_order_reviews": "order_reviews_dataset.csv",
        "staging_orders": "orders_dataset.csv",
        "staging_products": "products_dataset.csv",
        "staging_sellers": "sellers_dataset.csv",
        "staging_product_category_translation": "product_category_name_translation.csv"
    }

    for table, file in file_paths.items():
        df = load_data(file)
        insert_into_staging(connection, table, df)

    transform_and_insert_clean_data(connection)
    create_data_mart(connection)

    connection.close()
    print("ETL process completed.")

if __name__ == "__main__":
    etl_pipeline()
