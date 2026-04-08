import streamlit as st
import pandas as pd
streamlit run app_streamlit.pyfrom business_logic import (
    clean_data, 
    apply_business_constraints, 
    get_data_types, 
    get_aggregated_data,
    validate_raw_data
)

st.set_page_config(page_title="Retail Analytics Pipeline", layout="wide")

st.title("📊 Retail Store Analytics - ETL Pipeline")

st.markdown("---")

# File upload section
uploaded_file = st.file_uploader("Upload CSV Data", type="csv")

if uploaded_file:
    # Load raw data
    raw_df = pd.read_csv(uploaded_file)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📥 Raw Data", 
        "🔧 Data Cleaning", 
        "✅ Cleaned Data", 
        "📊 Business Logic", 
        "📈 Aggregations"
    ])
    
    with tab1:
        st.header("Raw Data Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        raw_metrics = validate_raw_data(raw_df)
        col1.metric("Total Records", raw_metrics['total_records'])
        col2.metric("Duplicates", raw_metrics['duplicates'])
        col3.metric("NULL Values", raw_metrics['null_values'])
        col4.metric("Negative Qty", raw_metrics['negative_quantity'])
        
        st.subheader("Raw Data Sample")
        st.dataframe(raw_df.head(10), use_container_width=True)
        
        st.subheader("NULL Values per Column")
        null_df = pd.DataFrame({
            'Column': raw_metrics['null_per_column'].keys(),
            'NULL Count': raw_metrics['null_per_column'].values()
        })
        st.bar_chart(null_df.set_index('Column'))
    
    with tab2:
        st.header("Data Cleaning Process")
        
        st.info("🔄 Cleaning includes:")
        st.write("- ✅ Remove duplicates")
        st.write("- ✅ Fill missing values")
        st.write("- ✅ Fix negative values")
        st.write("- ✅ Fix date formats")
        st.write("- ✅ Standardize categories")
        
        # Clean the data
        cleaned_df = clean_data(raw_df)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Records Before", len(raw_df))
        col2.metric("Records After", len(cleaned_df))
        col3.metric("Records Removed", len(raw_df) - len(cleaned_df))
        
        st.subheader("Comparison")
        comparison_data = {
            'Metric': ['Duplicates', 'NULL Values', 'Negative Qty', 'Negative Price'],
            'Before Cleaning': [
                raw_metrics['duplicates'],
                raw_metrics['null_values'],
                raw_metrics['negative_quantity'],
                raw_metrics['negative_price']
            ],
            'After Cleaning': [
                cleaned_df.duplicated().sum(),
                cleaned_df.isnull().sum().sum(),
                (cleaned_df['quantity_sold'] < 0).sum() if 'quantity_sold' in cleaned_df.columns else 0,
                (cleaned_df['unit_price'] < 0).sum() if 'unit_price' in cleaned_df.columns else 0
            ]
        }
        st.bar_chart(pd.DataFrame(comparison_data).set_index('Metric'))
    
    with tab3:
        st.header("Cleaned Data")
        
        cleaned_df = clean_data(raw_df)
        
        st.subheader("Data Types")
        dtypes_df = pd.DataFrame({
            'Column': get_data_types(cleaned_df).index,
            'Data Type': get_data_types(cleaned_df).values
        })
        st.dataframe(dtypes_df)
        
        st.subheader("Cleaned Data Sample")
        st.dataframe(cleaned_df.head(10), use_container_width=True)
        
        st.subheader("Statistical Summary")
        st.dataframe(cleaned_df.describe(), use_container_width=True)
    
    with tab4:
        st.header("Business Constraints Applied")
        
        cleaned_df = clean_data(raw_df)
        constraints_df = apply_business_constraints(cleaned_df)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Records", len(constraints_df))
        col2.metric("Total Revenue", f"${constraints_df['total_sales'].sum():,.2f}")
        col3.metric("Avg Transaction", f"${constraints_df['total_sales'].mean():,.2f}")
        col4.metric("Max Transaction", f"${constraints_df['total_sales'].max():,.2f}")
        col5.metric("Min Transaction", f"${constraints_df['total_sales'].min():,.2f}")
        
        st.subheader("Constrained Data (total_sales, order_month, order_day)")
        st.dataframe(constraints_df, use_container_width=True)
    
    with tab5:
        st.header("Aggregated Analytics")
        
        cleaned_df = clean_data(raw_df)
        constraints_df = apply_business_constraints(cleaned_df)
        agg_data = get_aggregated_data(constraints_df)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Revenue", f"${agg_data['total_revenue']:,.2f}")
        col2.metric("Total Orders", agg_data['total_records'])
        col3.metric("Avg Order Value", f"${agg_data['avg_transaction']:,.2f}")
        col4.metric("Highest Order", f"${agg_data['max_transaction']:,.2f}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sales by Month")
            monthly_data = pd.Series(agg_data['month_distribution'])
            st.bar_chart(monthly_data)
        
        with col2:
            st.subheader("Sales by Day")
            daily_data = pd.Series(agg_data['day_distribution'])
            st.line_chart(daily_data)
else:
    st.info("👉 Upload a CSV file to start the ETL pipeline")
    st.markdown("""
    ### Expected CSV Columns:
    - `order_id` - Unique order identifier
    - `order_date` - Date of the order
    - `store_id` - Store identifier
    - `product_id` - Product identifier
    - `product_category` - Product category
    - `quantity_sold` - Quantity sold
    - `unit_price` - Price per unit
    """)
