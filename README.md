🚀 Sprint 1 Status Update
✅ Design Phase
Data model and system design have been reviewed and approved
Identified that the API structure does not align with business requirements



⚠️ Key Challenge Identified
The API (fake-store-api) provides product-level data
Business requirement needs transaction-level (sales) data


👉 Decision Taken:

Generate synthetic (random) sales data to simulate real-world retail transactions
📊 Data Strategy
Created a custom dataset (100 records)
Included:
Order-level data (order_id, quantity, order_date)
Product-level mapping
Store-level simulation
Introduced real-world data issues:
Duplicates
Null values
Invalid dates
Negative values
Category inconsistencies



👉 Purpose: To test robustness of ETL pipeline

👥 Team Responsibilities
Module	Owner	Responsibility
Extraction & Cleaning	Yagnesh	Data ingestion, raw storage, cleaning
Database & Schema Design	Sudheer	Table design (raw, cleaned, aggregated)
Business Transformations	Prasanth	Derived metrics, business rules
Analytics & UI	Mithra	Dashboard, insights, visualization
📦 Current Progress
✅ Dataset successfully generated and stored
✅ Folder structure implemented
✅ Raw data ingestion completed
⏳ Data cleaning (in progress)
⏳ Transformation logic (pending)
🎯 Sprint 1 Deliverables Completed



Data source analysis
Gap identification (API vs business needs)
Synthetic dataset creation
Initial ETL structure setup


🚀 Next Steps (Sprint 2)
Implement data cleaning pipeline:
Handle null values
Remove duplicates
Fix data types
Apply business transformation rules
Generate analytics-ready dataset
