import pandas as pd

def apply_business_constraints():
    """
    Load cleaned sales data and apply business constraints.
    Returns dataframe with total_sales, order_month, order_day
    """
    # Load cleaned data
    df = pd.read_csv("cleaned_sales_data.csv")
    
    # Convert order_date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Apply business constraints
    df['total_sales'] = df['quantity_sold'] * df['unit_price']
    df['order_month'] = df['order_date'].dt.month
    df['order_day'] = df['order_date'].dt.day
    
    # Return only required columns
    return df[['total_sales', 'order_month', 'order_day']]


def get_data_types():
    """
    Get data types of cleaned sales data before aggregation
    """
    df = pd.read_csv("cleaned_sales_data.csv")
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df.dtypes


def get_aggregated_data():
    """
    Get aggregated business metrics
    """
    df = apply_business_constraints()
    
    aggregated = {
        'total_revenue': df['total_sales'].sum(),
        'avg_transaction': df['total_sales'].mean(),
        'max_transaction': df['total_sales'].max(),
        'min_transaction': df['total_sales'].min(),
        'total_records': len(df),
        'month_distribution': df['order_month'].value_counts().sort_index().to_dict(),
        'day_distribution': df['order_day'].value_counts().sort_index().to_dict(),
    }
    
    return aggregated
