# E-Commerce Sales ETL & SQL Analytics Pipeline

[![PySpark](https://img.shields.io/badge/Apache%20PySpark-4.2.0-orange?style=flat&logo=apachespark)](https://spark.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=flat&logo=docker)](https://www.docker.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=flat&logo=mysql)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.x-brightgreen?style=flat&logo=python)](https://www.python.org/)

An end-to-end data engineering pipeline built using the Online Retail dataset. The pipeline extracts raw retail data, transforms and cleans it using **Apache PySpark**, loads the structured data into a **MySQL** Data Warehouse using a Star Schema, performs automated data-quality validations, and exposes SQL analytics and views for business intelligence.

---

## Architecture Overview

```text
Online Retail Excel Dataset
            |
            v
     Python / OpenPyXL
            |
            v
       Raw CSV Data
            |
            v
   Apache PySpark + Docker
            |
            |-- Remove missing values
            |-- Remove invalid transactions
            |-- Remove duplicates
            |-- Clean text fields
            |-- Calculate Revenue (Quantity x Unit Price)
            |
            v
     Cleaned CSV Data
            |
            v
   MySQL Data Warehouse (Star Schema)
            |
            +-- dim_customer
            +-- dim_product
            +-- dim_date
            +-- fact_sales
            |
            v
  Data Quality Validation (Automated Checks)
            |
            v
      SQL Analytics & Views
```

---

## Key Data Engineering Concepts Demonstrated

* **ETL Pipeline Development**: Batch extraction, transformation, and database loading workflows.
* **Large-Scale Data Processing**: Apache PySpark DataFrames for distributed data cleaning and feature engineering.
* **Containerization**: Docker and Docker Compose for predictable, reproducible runtime environments.
* **Data Warehousing & Dimensional Modeling**: Star Schema design with optimized Fact and Dimension tables.
* **Data Quality & Governance**: Automated verification scripts ensuring data integrity, calculation accuracy, and referential checks.
* **Database Performance Tuning**: Indexing strategy on join/filter keys and reusable analytical views (`monthly_revenue`).

---

## Dataset Information

This project uses the **Online Retail** dataset, which contains transactional records from an e-commerce retailer:

* **InvoiceNo**: Unique invoice number assigned to each transaction.
* **StockCode**: Product/item code.
* **Description**: Product description name.
* **Quantity**: Quantity of each product per transaction.
* **InvoiceDate**: Transaction date and time.
* **UnitPrice**: Product price per unit.
* **CustomerID**: Unique identifier assigned to each customer.
* **Country**: Name of the country where the customer resides.

---

## Data Warehouse Design (Star Schema)

The MySQL Data Warehouse is structured as a Star Schema optimized for OLAP analytics.

### Fact Table

* **`fact_sales`**: Stores numerical measurements and keys linking to dimensions (`invoice_no`, `stock_code`, `customer_id`, `date_key`, `quantity`, `unit_price`, `revenue`).

### Dimension Tables

* **`dim_customer`**: Holds customer profiles and geographic attributes (`customer_id`, `country`).
* **`dim_product`**: Holds product details (`stock_code`, `description`).
* **`dim_date`**: Time dimension for chronological analysis (`date_key`, `full_date`, `year`, `month`, `day`).

---

## Performance Optimizations & Data Quality

### Database Indexing

Indexes were applied to heavily queried columns to accelerate join and aggregation execution:

* `customer_id`
* `stock_code`
* `date_key`
* `invoice_no`

### Automated Data Quality Checks

The automated pipeline executes sanity checks before serving analytics:

* Validation of positive quantities, unit prices, and overall revenue.
* Audit of missing Customer IDs and referential integrity between Fact and Dimension tables.
* *Finding*: During automated checks, 4 zero-price records were detected and filtered out prior to final analytics.

---

## Key Metrics & Pipeline Results

* **Valid Sales Records**: 392,688
* **Unique Customers**: 4,338
* **Unique Products**: 3,922
* **Date Granularity**: 305 unique days
* **Total Calculated Revenue**: ~$8.89 Million

---

## Project Structure

```text
ecommerce-data-engineering/
├── data/
│   ├── cleaned_retail/      # Output directory for processed CSV files
│   ├── Online Retail.xlsx   # Source raw Excel dataset
│   └── online_retail.csv    # Converted raw CSV data
├── src/
│   ├── prepare_data.py      # Converts XLSX to CSV using OpenPyXL
│   ├── transform.py         # PySpark ETL script (cleaning & transformations)
│   ├── load_to_mysql.py     # Batch loader to MySQL Data Warehouse
│   └── data_quality.py      # Data Quality and integrity checking script
├── docker-compose.yml       # Spins up isolated MySQL service
├── requirements.txt         # Python dependency manifest
├── sql_queries.sql          # Analytical queries and SQL views
└── README.md                # Project documentation
```

---

## Tech Stack

* **Language**: Python 3.x
* **Processing Framework**: Apache PySpark
* **Excel Parsing**: OpenPyXL
* **Database**: MySQL 8.0
* **Database Connector**: `mysql-connector-python`
* **Infrastructure**: Docker & Docker Compose
* **Version Control**: Git

---

## Getting Started

### Prerequisites

* [Python 3.8+](https://www.python.org/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Step-by-Step Execution Guide

#### 1. Clone the Repository & Install Dependencies

```bash
git clone https://github.com/your-username/ecommerce-data-engineering.git
cd ecommerce-data-engineering
pip install -r requirements.txt
```

#### 2. Convert Excel Dataset to CSV

Convert the raw `.xlsx` file into standard CSV format:

```bash
python src/prepare_data.py
```

#### 3. Execute PySpark ETL Engine via Docker

Process raw data using the PySpark Docker container (replace `PROJECT_PATH` with your local directory path):

```bash
docker run --rm -it \
  -v "PROJECT_PATH:/workspace" \
  -w /workspace \
  apache/spark:4.2.0-python3 \
  /opt/spark/bin/spark-submit src/transform.py
```

#### 4. Spin Up MySQL Database

Launch the MySQL container defined in `docker-compose.yml`:

```bash
docker compose up -d
```

#### 5. Load Cleaned Data into Data Warehouse

Populate the Star Schema dimension and fact tables:

```bash
python src/load_to_mysql.py
```

#### 6. Run Automated Data Quality Checks

Execute the data-quality validation suite:

```bash
python src/data_quality.py
```

#### 7. Execute Analytics Queries

Run the analytical queries and build database views using `sql_queries.sql` on your MySQL instance. Analytics cover:

* Total revenue & average order value (AOV)
* Monthly and yearly revenue trends
* Top-performing products & countries by revenue
* High-value customer identification