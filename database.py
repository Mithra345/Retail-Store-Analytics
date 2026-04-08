import sqlite3
import os
import pandas as pd

def create_db_tables():
    # Make sure folder exists
    if not os.path.exists('data'):
        os.makedirs('data')
        
    # Connect to basic sqlite3 database
    conn = sqlite3.connect('data/retail.db')
    cursor = conn.cursor()
    
    # Table 1: Raw Data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            order_date TEXT,
            store_id TEXT,
            product_id TEXT,
            product_category TEXT,
            quantity_sold REAL,
            unit_price REAL
        )
    ''')
    
    # Table 2: Cleaned Data (no missing/bad data, but no new derived business fields)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cleaned_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            order_date TEXT,
            store_id TEXT,
            product_id TEXT,
            product_category TEXT,
            quantity_sold INTEGER,
            unit_price REAL
        )
    ''')

    # Table 3: Transformed Data (includes the new calculated columns)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transformed_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            order_date TEXT,
            store_id TEXT,
            product_id TEXT,
            product_category TEXT,
            quantity_sold INTEGER,
            unit_price REAL,
            total_amount REAL,
            order_month INTEGER,
            order_day INTEGER
        )
    ''')
    
    # Save and close
    conn.commit()
    conn.close()

def load_data_to_db(df, table_name):
    # Connect to our basic python database
    conn = sqlite3.connect('data/retail.db')
    
    # Save the pandas dataframe into the SQL table directly
    df.to_sql(table_name, conn, if_exists='append', index=False)
    
    conn.close()

def get_dashboard_data():
    conn = sqlite3.connect('data/retail.db')

    # Basic SQL queries to get totals from final transformed table
    df_store = pd.read_sql('SELECT store_id, SUM(total_amount) as total_sales FROM transformed_sales GROUP BY store_id', conn)
    df_category = pd.read_sql('SELECT product_category, SUM(total_amount) as total_sales FROM transformed_sales GROUP BY product_category', conn)
    
    # SQLite DATE() function to group per day
    df_date = pd.read_sql('SELECT DATE(order_date) as order_date_day, SUM(total_amount) as total_sales FROM transformed_sales GROUP BY DATE(order_date)', conn)
    
    conn.close()
    
    return df_store, df_category, df_date

if __name__ == "__main__":
    create_db_tables()
    print("Database tables created success!")
