import streamlit as st
import pandas as pd

# Import from divided files
from database import create_db_tables, load_data_to_db, get_dashboard_data
from data_cleaning import read_and_rename_columns, clean_data
from business_logic import apply_business_rules

# Run it once so the SQL file is created!
create_db_tables()

st.title("Simple Retail Sales App")

# Beginner friendly sidebar approach instead of session states
menu = st.sidebar.selectbox("Select Page", ["1. Upload Data", "2. Transform & Load", "3. Dashboard Analytics"])

if menu == "1. Upload Data":
    st.header("Upload your File")
    my_file = st.file_uploader("Upload CSV file")
    
    if my_file is not None:
        df = read_and_rename_columns(my_file)
        st.write("Here is your uploaded data:")
        st.dataframe(df)
        
        # Save temporarily out of easiest approach!
        df.to_csv("data/temp_raw.csv", index=False)
        st.success("File uploaded to system! Go to next step.")

elif menu == "2. Transform & Load":
    st.header("Clean and Load Data to Database")
    try:
        df = pd.read_csv("data/temp_raw.csv")
        st.write("Reading raw file:")
        st.dataframe(df.head())
        if st.button("Process My Data"):
            # Step 1: Clean data using Teammate 2's code
            clean_df = clean_data(df)
            clean_df.to_csv("data/temp_clean.csv", index=False)
            # Step 2: Apply business logic using Teammate 3's code
            business_df = apply_business_rules(clean_df)
            business_df.to_csv("data/temp_transformed.csv", index=False)
            
            st.write("Here is the cleaned and processed data:")
            st.dataframe(business_df.head())
            
            st.success("Cleaned and processed successfully! Now click Load.")
            
        if st.button("Load Data into Database"):
            raw_df = pd.read_csv("data/temp_raw.csv")
            clean_df = pd.read_csv("data/temp_clean.csv")
            transformed_df = pd.read_csv("data/temp_transformed.csv")
            
            # Step 3: Load using Teammate 1's code
            load_data_to_db(raw_df, "raw_sales")
            load_data_to_db(clean_df, "cleaned_sales")
            load_data_to_db(transformed_df, "transformed_sales")
            
            st.success("All 3 stages (Raw, Cleaned, Transformed) are now saved into SQLite!")
            
    except Exception as e:
        st.error("Please upload the data in step 1 first.")

elif menu == "3. Dashboard Analytics":
    st.header("Analytics View")
    
    if st.button("Show Charts"):
        # Use Teammate 1's database queries
        df_store, df_category, df_date = get_dashboard_data()
        
        # Using built-in simple charts
        st.subheader("Sales by Store")
        chart_data_store = df_store.set_index('store_id')
        st.bar_chart(chart_data_store['total_sales'])
        
        st.subheader("Sales by Category")
        chart_data_category = df_category.set_index('product_category')
        st.bar_chart(chart_data_category['total_sales'])
        
        st.subheader("Sales by Date")
        chart_data_date = df_date.set_index('order_date_day')
        st.line_chart(chart_data_date['total_sales'])
