🚀 Sprint 0 Status Update
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


🚀 Next Steps (Sprint 1)
Implement data cleaning pipeline:
Handle null values
Remove duplicates
Fix data types
Apply business transformation rules
Generate analytics-ready dataset


## 🚀 Next Steps (Sprint 1)

### 🧹 Data Cleaning Pipeline

* Handle missing values using appropriate strategies (drop/impute)
* Remove duplicate records to maintain data integrity
* Fix inconsistent and mismatched data types
* Validate and correct date formats
* Standardize categorical values (e.g., category names)

---

### 🔍 Data Validation Layer

* Perform schema validation (column checks)
* Validate data types (numeric, datetime)
* Identify and handle invalid values:

  * Negative price and quantity
  * Incorrect or null dates
* Ensure data consistency before transformation

---

### 🔧 Business Transformation Layer *(Prasanth’s Role)*

* Apply business rules to filter valid transactions:

  * price > 0
  * quantity > 0

* Create derived columns:

  * `total_sales = price × quantity`
  * `order_month` (from order_date)
  * `order_year`

* Build business-ready dataset:

  * Structured and validated for analytics consumption

---

### 📊 Aggregation & Metrics

* Generate key business insights:

  * Sales by Category
  * Sales by Store
  * Monthly Sales Trends
  * Top Performing Products

---

### 💾 Data Storage (Processed Layer)

* Store transformed datasets in the database:

  * Business-level table
  * Aggregated tables
* Ensure proper schema design for efficient querying

---

### 📈 Analytics & Visualization *(Mithra’s Role)*

* Build dashboards for:

  * Category-wise sales performance
  * Monthly trends
  * Store-level insights
* Enable decision-making for Sales Executives

---

## 🎯 Expected Outcome (End of Sprint 1)

* Clean, validated, and structured dataset
* Business-ready transformation layer
* Aggregated insights for analytics
* Data prepared for visualization and reporting

---

## 🔥 Key Engineering Practices Followed

* Separation of concerns (Extract → Clean → Transform → Analyze)
* Handling of real-world dirty data scenarios
* Use of validation layers before transformations
* Modular and scalable pipeline design

---

## 💬 Summary

Sprint 0 focused on **data understanding, simulation, and pipeline setup**.
Sprint 1 will focus on **data quality, transformation logic, and analytics readiness**, ensuring the system delivers meaningful business insights.

