# 🛒 My Store ETL Data Pipeline

## Overview

**My Store ETL Pipeline** is an end-to-end data engineering project built with Python that extracts customer and purchase data from multiple sources, performs data quality checks and transformations, enriches the dataset with additional analytical fields, and loads the final dataset into PostgreSQL.

The project also includes a data visualization component that queries the PostgreSQL database and generates visual reports for understanding customer spending, purchasing patterns, and purchase amount distribution.

The pipeline demonstrates the core stages of an **ETL (Extract, Transform, Load)** workflow.

---

## 🔄 Pipeline Architecture

```text
                    DATA SOURCES
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
       customers.csv         purchases.json
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
                 EXTRACT
                        │
                        ▼
              DATA QUALITY CHECKS
                        │
                        ▼
                 TRANSFORM
                        │
             ┌──────────┼───────────┐
             │          │           │
             ▼          ▼           ▼
          Remove      Merge       Clean
         Duplicates  Datasets     Data
             │          │           │
             └──────────┼───────────┘
                        │
                        ▼
                   ENRICH DATA
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
        USD Conversion      Purchase Category
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
                Final Validation
                        │
                        ▼
                 PostgreSQL
                  sales_data
                        │
                        ▼
                 SQL Analytics
                        │
                        ▼
                 Visualizations
```

---

## 🎯 Project Objectives

The pipeline was designed to:

* Extract customer data from a CSV file.
* Extract purchase data from a JSON file.
* Perform initial data quality checks.
* Identify duplicate and missing records.
* Remove duplicate records.
* Merge customer and purchase datasets.
* Handle missing purchase amounts.
* Remove negative purchase amounts.
* Convert purchase amounts to USD.
* Categorize purchases based on their value.
* Extract customer email domains.
* Validate the transformed dataset.
* Load the processed data into PostgreSQL.
* Query the database for analytical insights.
* Generate visualizations from the processed data.

---

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **PostgreSQL**
* **SQLAlchemy**
* **psycopg2**
* **Matplotlib**
* **CSV**
* **JSON**
* **SQL**

---

## 📁 Data Sources

The pipeline works with two input sources.

### Customers

Customer information is stored in:

```text
data/customers.csv
```

The pipeline expects approximately **50 customer records**.

The customer dataset is joined to the purchase data using:

```text
customer_id
```

### Purchases

Purchase information is stored in:

```text
data/purchases.json
```

The pipeline expects approximately **51 purchase records**.

The JSON data is loaded into a Pandas DataFrame before transformation.

---

# 🔍 Step 1 — Extract

The first stage of the pipeline extracts data from the two source files.

# 🔄 Step 2 — Transform

- Duplicate customer and purchase records are removed while keeping the first occurrence.
- The pipeline creates additional fields that make the dataset more useful for analysis.
- The pipeline extracts the domain portion of each customer's email address.
- Before loading the data into PostgreSQL, the pipeline performs final validation checks.
- The pipeline also validates that the expected numerical data types are present.
---

# 🗄️ Step 3 — Load

- The transformed dataset is loaded into **PostgreSQL** using SQLAlchemy.

- The pipeline then queries PostgreSQL to verify that the expected number of records were successfully loaded.

---

# 📂 Project Structure

```text
my_store/
│
├── data/
│   ├── customers.csv
│   └── purchases.json
│
├── scripts/
│   ├── pipeline.py
│   └── visualize_results.py
│
├── visualizations/
│   ├── top_customers_spending.png
│   ├── purchases_by_location.png
│   └── amount_distribution.png
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd my_store
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Database Configuration

The pipeline uses environment variables for PostgreSQL connection details.

Set the following variables:

```text
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DB_NAME
```

Example:

```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=data_engineering
```

> **Security note:** Database credentials should not be hard-coded or committed to GitHub. Use environment variables or a `.env` file that is excluded from version control.

---

# ▶️ Running the Pipeline

Run the ETL pipeline:

```bash
python scripts/pipeline.py
```

The pipeline will:

1. Extract customer data.
2. Extract purchase data.
3. Perform data quality checks.
4. Remove duplicates.
5. Merge the datasets.
6. Clean invalid values.
7. Convert purchase amounts to USD.
8. Categorize purchases.
9. Extract email domains.
10. Validate the transformed data.
11. Load the dataset into PostgreSQL.
12. Verify the database records.

---

# 📈 Running the Visualizations

After the ETL pipeline successfully loads the data into PostgreSQL, run:

```bash
python scripts/visualize_results.py
```

This generates:

```text
top_customers_spending.png
purchases_by_location.png
amount_distribution.png
```

---

# 📌 Example Pipeline Output

The pipeline provides console feedback throughout execution.

Example:

```text
============================================================
STEP 1: EXTRACTING DATA FROM SOURCES
============================================================

✅ Customers data loaded successfully!
   Shape: (50, 4)

✅ Purchases data loaded successfully!
   Shape: (51, 4)

============================================================
STEP 2: TRANSFORMING DATA
============================================================

🧹 Removing duplicates...
   ✅ Removed duplicate customer(s)
   ✅ Removed duplicate purchase(s)

🔗 Merging customers and purchases...
   ✅ Merge complete!

🧼 Cleaning data...
   ✅ No missing values detected!

💰 Enriching data with currency conversion...
   ✅ Added 'amount_usd' column
   ✅ Added 'purchase_category' column

============================================================
STEP 3: LOADING DATA TO POSTGRESQL
============================================================

🔌 Connecting to PostgreSQL database...
   ✅ Database connection successful!

💾 Loading data to 'sales_data' table...
   ✅ Data loaded successfully!

============================================================
✅ ETL PIPELINE COMPLETED SUCCESSFULLY!
============================================================
```

---

# 🧠 Key Data Engineering Concepts Demonstrated

This project demonstrates practical knowledge of:

* ETL pipeline development
* Data ingestion from multiple file formats
* CSV processing
* JSON processing
* Data quality assessment
* Duplicate detection
* Missing-value handling
* Data transformation
* Dataset joining
* Feature engineering
* Data enrichment
* PostgreSQL integration
* SQL querying
* SQLAlchemy
* Data validation
* Analytical visualization
* Error handling

---

# 🚀 Future Improvements

Potential improvements to the pipeline include:

* Add **Apache Airflow** for workflow orchestration.
* Replace hard-coded configuration with a `.env` file.
* Add automated unit tests.
* Add more robust data-quality validation.
* Implement incremental database loading instead of replacing the table.
* Add logging instead of relying primarily on `print()` statements.
* Containerize the pipeline with Docker.
* Add database indexes for frequently queried columns.
* Build a BI dashboard using Power BI, Tableau, or another visualization platform.
* Add automated scheduling.
* Implement a proper currency exchange-rate API instead of a fixed conversion factor.

---

# 👨‍💻 Project Summary

**My Store ETL Pipeline** demonstrates how raw customer and transaction data can be transformed into an analysis-ready dataset using a structured ETL workflow.

The project combines **Python, Pandas, SQLAlchemy, PostgreSQL, SQL, and Matplotlib** to create a complete workflow from raw data ingestion through transformation, database storage, and analytical visualization.

It serves as a practical foundation for developing more scalable and production-oriented data engineering pipelines.

---

# Author

**Gift David**

Aspiring Data Engineer passionate about building scalable data pipelines, workflow automation, and analytics solutions.

Feel free to connect or explore my other projects.