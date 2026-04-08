# loader.py

import pandas as pd
from database import get_engine

engine = get_engine()

# 🔹 FILE PATHS (update if needed)
RAW_FILE = r"C:\Users\pulla\Downloads\raw_sales_data_200_dirty.csv"
CLEAN_FILE = r"C:\Users\pulla\Downloads\cleaned_sales_data.csv"


# 🔹 LOAD RAW DATA
def load_raw():
    df = pd.read_csv(RAW_FILE)

    df.to_sql(
        name="raw_sales",
        con=engine,
        if_exists="append",
        index=False
    )

    print("✅ raw_sales loaded")


# 🔹 LOAD CLEANED DATA
def load_cleaned():
    df = pd.read_csv(CLEAN_FILE)

    # Optional safety (avoid duplicate key error)
    if 'order_id' in df.columns and 'product_id' in df.columns:
        df = df.drop_duplicates(subset=['order_id', 'product_id'])

    df.to_sql(
        name="cleaned_sales",
        con=engine,
        if_exists="append",
        index=False
    )

    print("✅ cleaned_sales loaded")


# 🔹 LOAD AGGREGATED DATA

# 🔹 MAIN RUNNER
if __name__ == "__main__":
    print("🚀 Starting data load...")

    load_raw()
    load_cleaned()


    print("🎯 All data loaded successfully!")