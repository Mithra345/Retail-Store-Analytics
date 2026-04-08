import pandas as pd

def apply_business_rules(df):
    """
    Apply business rules to the cleaned data:
    - Calculate total_amount = quantity_sold * unit_price
    - Extract order_month and order_day from order_date
    """
    # Calculate total amount
    df['total_amount'] = df['quantity_sold'] * df['unit_price']
    
    # Extract month and day from order_date
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['order_month'] = df['order_date'].dt.month
    df['order_day'] = df['order_date'].dt.day
    
    return df
