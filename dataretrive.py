import pandas as pd

def clean_data(raw_df):
    """
    Clean raw data: remove duplicates, handle missing values, fix negative values,
    fix date formats, and standardize categories.
    """
    df = raw_df.copy()
    
    # -----------------------------
    # 1. Remove duplicates
    # -----------------------------
    df = df.drop_duplicates()
    
    # -----------------------------
    # 2. Handle missing values
    # -----------------------------
    if 'store_id' in df.columns:
        df['store_id'] = df['store_id'].fillna(df['store_id'].mode()[0])
    if 'quantity_sold' in df.columns:
        df['quantity_sold'] = df['quantity_sold'].fillna(df['quantity_sold'].median())
    if 'unit_price' in df.columns:
        df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
    if 'product_category' in df.columns:
        df['product_category'] = df['product_category'].fillna('Unknown')
    
    # -----------------------------
    # 3. Fix negative values
    # -----------------------------
    if 'quantity_sold' in df.columns:
        df['quantity_sold'] = df['quantity_sold'].abs()
        # Replace zeros (optional safety)
        df.loc[df['quantity_sold'] == 0, 'quantity_sold'] = df['quantity_sold'].median()

    if 'unit_price' in df.columns:
        df['unit_price'] = df['unit_price'].abs()
        # Replace zeros (optional safety)
        df.loc[df['unit_price'] == 0, 'unit_price'] = df['unit_price'].median()
        
    # -----------------------------
    # 4. Fix date format (IMPORTANT)
    # -----------------------------
    if 'order_date' in df.columns:
        # Convert object → datetime
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        # Fill invalid dates
        df['order_date'] = df['order_date'].fillna(df['order_date'].mode()[0])
        
    # -----------------------------
    # 5. Standardize categories
    # -----------------------------
    if 'product_category' in df.columns:
        df['product_category'] = df['product_category'].str.lower()
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

if __name__ == "__main__":
    # Load dataset
    try:
        df = pd.read_csv("raw_sales_data_200_dirty.csv")
        cleaned_df = clean_data(df)
        # Save cleaned data
        cleaned_df.to_csv("cleaned_sales_data.csv", index=False)
        # Check result
        print("✅ Cleaned dataset ready")
        print("Final row count:", len(cleaned_df))
    except Exception as e:
        print(f"Error processing offline script: {e}")
