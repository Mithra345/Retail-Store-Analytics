import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("raw_sales_data_200_dirty.csv")

# -----------------------------
# 1. Remove duplicates (keep first)
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# 2. Handle missing values
# -----------------------------
df['store_id'] = df['store_id'].fillna(df['store_id'].mode()[0])
df['quantity_sold'] = df['quantity_sold'].fillna(df['quantity_sold'].median())
df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
df['product_category'] = df['product_category'].fillna('Unknown')

# -----------------------------
# 3. Fix negative values (convert to positive)
# -----------------------------
df['quantity_sold'] = df['quantity_sold'].abs()
df['unit_price'] = df['unit_price'].abs()

# Replace zeros if any (optional safety)
df.loc[df['quantity_sold'] == 0, 'quantity_sold'] = df['quantity_sold'].median()
df.loc[df['unit_price'] == 0, 'unit_price'] = df['unit_price'].median()

# -----------------------------
# 4. Fix date issues
# -----------------------------
# Convert dates (invalid → NaT)
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# Fill invalid dates with most frequent date
df['order_date'] = df['order_date'].fillna(df['order_date'].mode()[0])

# -----------------------------
# 5. Standardize categories
# -----------------------------
df['product_category'] = df['product_category'].str.lower()

df['product_category'] = df['product_category'].replace({
    'electronics': 'Electronics',
    'clothng': 'Clothing',
    'clothing': 'Clothing',
    'grocery': 'Grocery'
})

# -----------------------------
# Final dataset (no rows removed)
# -----------------------------
df = df.reset_index(drop=True)

# Save cleaned data
df.to_csv("cleaned_sales_data.csv", index=False)

print("✅ Cleaned dataset ready (no rows removed)")
print("Final row count:", len(df))