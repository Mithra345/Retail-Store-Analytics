import pandas as pd
import numpy as np

def read_and_rename_columns(file_path):
    # Use simple pandas read_csv
    df = pd.read_csv(file_path)
    
    # Rename columns so they are strictly standardized to match code format
    df = df.rename(columns={
        'Order ID': 'order_id',
        'Order Date': 'order_date',
        'Store ID': 'store_id',
        'Product ID': 'product_id',
        'Product Category': 'product_category',
        'Quantity Sold': 'quantity_sold',
        'Unit Price': 'unit_price'
    })
    
    return df

def clean_data(df):
    # -----------------------------
    # 1. Remove duplicates
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
    # 3. Fix negative values
    # -----------------------------
    df['quantity_sold'] = df['quantity_sold'].abs()
    df['unit_price'] = df['unit_price'].abs()

    # Replace zeros (optional safety)
    df.loc[df['quantity_sold'] == 0, 'quantity_sold'] = df['quantity_sold'].median()
    df.loc[df['unit_price'] == 0, 'unit_price'] = df['unit_price'].median()
    
    # -----------------------------
    # 4. Fix date format (IMPORTANT)
    # -----------------------------
    # Convert object to datetime
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    # Fill invalid dates
    df['order_date'] = df['order_date'].fillna(df['order_date'].mode()[0])
    
    # -----------------------------
    # 5. Standardize categories
    # -----------------------------
    df['product_category'] = df['product_category'].astype(str).str.lower()
    df['product_category'] = df['product_category'].replace({
        'electronics': 'Electronics',
        'clothng': 'Clothing',
        'clothing': 'Clothing',
        'grocery': 'Grocery'
    })
    
    # -----------------------------
    # Final cleaned dataset
    # -----------------------------
    df = df.reset_index(drop=True)

    return df
