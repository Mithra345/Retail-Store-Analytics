import pandas as pd

def clean_data(raw_df):
    """
    Clean raw data: remove duplicates, handle missing values, fix data types
    """
    df = raw_df.copy()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Fill missing values
    if 'store_id' in df.columns:
        df['store_id'] = df['store_id'].fillna(df['store_id'].mode()[0] if len(df['store_id'].mode()) > 0 else 1)
    if 'quantity_sold' in df.columns:
        df['quantity_sold'] = df['quantity_sold'].fillna(df['quantity_sold'].median() if df['quantity_sold'].notna().any() else 0)
    if 'unit_price' in df.columns:
        df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median() if df['unit_price'].notna().any() else 0)
    if 'product_category' in df.columns:
        df['product_category'] = df['product_category'].fillna('Unknown')
    
    # Fix negative values
    if 'quantity_sold' in df.columns:
        df['quantity_sold'] = df['quantity_sold'].abs()
    if 'unit_price' in df.columns:
        df['unit_price'] = df['unit_price'].abs()
    
    # Replace zeros with median
    if 'quantity_sold' in df.columns:
        median_qty = df[df['quantity_sold'] > 0]['quantity_sold'].median() if (df['quantity_sold'] > 0).any() else 2
        df.loc[df['quantity_sold'] == 0, 'quantity_sold'] = median_qty
    
    if 'unit_price' in df.columns:
        median_price = df[df['unit_price'] > 0]['unit_price'].median() if (df['unit_price'] > 0).any() else 50
        df.loc[df['unit_price'] == 0, 'unit_price'] = median_price
    
    # Fix date format
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['order_date'] = df['order_date'].fillna(df['order_date'].mode()[0] if len(df['order_date'].mode()) > 0 else pd.Timestamp.now())
    
    # Standardize categories
    if 'product_category' in df.columns:
        df['product_category'] = df['product_category'].str.lower()
        df['product_category'] = df['product_category'].replace({
            'electronics': 'Electronics',
            'clothng': 'Clothing',
            'clothing': 'Clothing',
            'grocery': 'Grocery'
        })
    
    df = df.reset_index(drop=True)
    return df

def apply_business_constraints(cleaned_df=None):
    """
    Load cleaned sales data or use provided df and apply business constraints.
    Returns dataframe with total_sales, order_month, order_day
    """
    if cleaned_df is None:
        cleaned_df = pd.read_csv("cleaned_sales_data.csv")
    
    # Convert order_date to datetime
    df = cleaned_df.copy()
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Apply business constraints
    df['total_sales'] = df['quantity_sold'] * df['unit_price']
    df['order_month'] = df['order_date'].dt.month
    df['order_day'] = df['order_date'].dt.day
    
    # Return only required columns
    return df[['total_sales', 'order_month', 'order_day']]

def get_data_types(df=None):
    """
    Get data types of cleaned sales data before aggregation
    """
    if df is None:
        df = pd.read_csv("cleaned_sales_data.csv")
        df['order_date'] = pd.to_datetime(df['order_date'])
    
    return df.dtypes


def get_aggregated_data(constraints_df):
    """
    Get aggregated business metrics from constraints dataframe
    """
    if constraints_df is None or len(constraints_df) == 0:
        return {}
    
    aggregated = {
        'total_revenue': constraints_df['total_sales'].sum(),
        'avg_transaction': constraints_df['total_sales'].mean(),
        'max_transaction': constraints_df['total_sales'].max(),
        'min_transaction': constraints_df['total_sales'].min(),
        'total_records': len(constraints_df),
        'month_distribution': constraints_df['order_month'].value_counts().sort_index().to_dict(),
        'day_distribution': constraints_df['order_day'].value_counts().sort_index().to_dict(),
    }
    
    return aggregated


def validate_raw_data(raw_df):
    """
    Validate raw data and return quality metrics
    """
    metrics = {
        'total_records': len(raw_df),
        'duplicates': raw_df.duplicated().sum(),
        'null_values': raw_df.isnull().sum().sum(),
        'null_per_column': raw_df.isnull().sum().to_dict(),
        'negative_quantity': (raw_df['quantity_sold'] < 0).sum() if 'quantity_sold' in raw_df.columns else 0,
        'negative_price': (raw_df['unit_price'] < 0).sum() if 'unit_price' in raw_df.columns else 0,
    }
    return metrics
