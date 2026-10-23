# Vendor Performance & Inventory Analytics System

A data engineering and analytics pipeline that automates the ingestion of fragmented supply chain data into a relational database, providing programmatic insights into vendor efficiency, procurement metrics, and inventory health.

---

## 📌 Project Overview
In retail and wholesale operations, supply chain visibility is often hindered by disconnected data silos (separate CSVs for invoices, sales, and inventory). This project bridges that gap by:
1. *Data Engineering:* Building an automated Python pipeline (ingestion_db.py) that cleans and loads raw retail records into a unified relational database (inventory.db).
2. *Advanced Analytics:* Querying and analyzing the database via Python/SQL (Vendor Performance Analysis.ipynb) to evaluate vendor delivery reliability, pricing structures, and inventory velocity.
3. *Business Intelligence:* Outlining core performance gaps to optimize working capital and minimize stockout risks.

---

## 🛠️ Tech Stack & Toolkit
* *Language:* Python 3.x
* *Database Engine:* SQL / SQLite (sqlite3)
* *Data Manipulation:* Pandas, NumPy
* *Data Visualization:* Matplotlib, Seaborn
* *Reporting:* Apple Pages / Power BI

---

## 📂 Repository Architecture & Data Flow

text
├── Data Ingestion Pipeline
│   ├── ingestion_db.py               # Database schema builder & ETL ingestion script
│   └── ingestion_db.log              # Tracks automated pipeline logs & data integrity
│
├── Relational Database
│   └── inventory.db                  # Local SQLite database containing structured tables
│
├── Analytical Workspaces
│   ├── Exploratry data analysis.ipynb # Data profiling, missing value handling & anomaly checks
│   └── Vendor Performance Analysis.ipynb # Advanced SQL queries, KPI math, and visualizations
│
└── Business Outputs
    └── vendor_performance_report.pages # Executive report outlining vendor performance scores


### Raw Datasets Handled (Ingested into inventory.db):
* 📦 *Stock Tracking:* begin_inventory.csv, end_inventory.csv
* 💰 *Financial & Invoicing:* purchase_prices.csv, vendor_invoice.csv
* 🛒 *Transaction Streams:* purchases.csv, sales.csv

---

## 📈 Core Analytical Objectives & KPIs Monitored

* *Vendor Price Variances:* Compares purchase_prices.csv against actual vendor_invoice.csv totals to detect overcharging, hidden fees, or fulfillment discrepancies.
* *Inventory Turnover Ratio (ITR):* Evaluates how efficiently stock moves from begin_inventory through sales to end_inventory, identifying dead stock.
* *Sell-Through & Profitability Analysis:* Measures gross profit margins across varying vendor brands to isolate high-performing products.
* *Data Pipeline Integrity:* Uses structured logging (ingestion_db.log) to audit rows processed, flagging schema errors or null data injection attempts.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed with the necessary data stack packages:
bash
pip install pandas numpy matplotlib seaborn


### 2. Run the Data Pipeline
Execute the ingestion script to build the local SQLite database from your raw CSV files:
bash
python ingestion_db.py

Verify the setup by checking ingestion_db.log to confirm all tables loaded successfully.

### 3. Open the Analytics Workspace
Launch Jupyter Notebook to inspect the statistical models, SQL queries, and visual charts:
bash
jupyter notebook

Open *Vendor Performance Analysis.ipynb* to execute the end-to-end analytical workflow.
