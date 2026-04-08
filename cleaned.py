import pandas as pd
from database import get_engine

engine = get_engine()

# 🔹 FILE PATHS (update if needed)
CLEAN_FILE = r"C:\Users\pulla\Downloads\cleaned_sales_data.csv"

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

    load_cleaned()


    print("🎯 All data loaded successfully!")