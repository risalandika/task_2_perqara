from db_connection import create_connection

def transform_and_insert_clean_data(connection):
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO customers (customer_id, customer_unique_id, customer_city, customer_state)
        SELECT DISTINCT customer_id, customer_unique_id, customer_city, customer_state FROM staging_customers
    """)

    cursor.execute("""
        INSERT INTO orders (order_id, customer_id, order_status, order_purchase_timestamp, order_delivered_customer_date, order_estimated_delivery_date)
        SELECT order_id, customer_id, order_status, order_purchase_timestamp, order_delivered_customer_date, order_estimated_delivery_date FROM staging_orders
    """)

    cursor.execute("""
        INSERT INTO order_items (order_id, product_id, seller_id, price, freight_value)
        SELECT order_id, product_id, seller_id, price, freight_value FROM staging_order_items
    """)

    cursor.execute("""
        INSERT INTO products (product_id, product_category, product_weight_g, product_length_cm, product_height_cm, product_width_cm)
        SELECT product_id, product_category_name, product_weight_g, product_length_cm, product_height_cm, product_width_cm FROM staging_products
    """)

    cursor.execute("""
        INSERT INTO sellers (seller_id, seller_city, seller_state)
        SELECT DISTINCT seller_id, seller_city, seller_state FROM staging_sellers
    """)

    cursor.execute("""
        INSERT INTO payments (order_id, payment_type, payment_value)
        SELECT order_id, payment_type, payment_value FROM staging_order_payments
    """)

    cursor.execute("""
        INSERT INTO reviews (review_id, order_id, review_score, review_comment_message)
        SELECT review_id, order_id, review_score, review_comment_message FROM staging_order_reviews
    """)

    connection.commit()
    cursor.close()

def create_data_mart(connection):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO order_summary (order_id, customer_id, total_items, total_value, avg_review_score, order_status, order_purchase_timestamp)
        SELECT 
            o.order_id,
            o.customer_id,
            COUNT(oi.product_id) AS total_items,
            SUM(oi.price + oi.freight_value) AS total_value,
            AVG(r.review_score) AS avg_review_score,
            o.order_status,
            o.order_purchase_timestamp
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN reviews r ON o.order_id = r.order_id
        GROUP BY o.order_id, o.customer_id, o.order_status, o.order_purchase_timestamp
    """)

    connection.commit()
    cursor.close()
