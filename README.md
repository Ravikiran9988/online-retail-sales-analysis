# Online Retail Sales Analysis

An end-to-end retail analytics project built with **Snowflake SQL, Python, and Streamlit**. The project cleans and validates the UCI Online Retail dataset, analyzes sales performance, and presents business insights through a dashboard and downloadable report exports.

<p align="center">
  <a href="https://online-retail-sales-analysis-khhbhcmnmnenzrefjkzebw.streamlit.app/"><strong>🚀 Open Live Streamlit Demo</strong></a>
  &nbsp; • &nbsp;
  <a href="https://github.com/Ravikiran9988/online-retail-sales-analysis"><strong>📂 View GitHub Repository</strong></a>
  &nbsp; • &nbsp;
  <a href="https://archive.ics.uci.edu/dataset/352/online+retail"><strong>📊 Source Dataset</strong></a>
</p>

---

## Overview

The project follows an analytics workflow from raw data to cleaned records, SQL analysis, validation, and dashboard reporting.

**Business questions explored**
- How does revenue change over time?
- Which products generate the highest revenue?
- Which countries contribute most to sales?
- How are customers distributed across spending segments?
- What cancellation and data-quality issues exist in the source data?

## Dashboard

**[Launch the Streamlit demo](https://online-retail-sales-analysis-khhbhcmnmnenzrefjkzebw.streamlit.app/)**

The public demo presents exported, aggregated Snowflake results. It is intended as a portfolio preview and **does not connect directly to Snowflake or refresh automatically**. Dashboard features depend on the available exported reports.

The Snowflake-hosted app source is available at [app/streamlit_app.py](app/streamlit_app.py). It uses Snowflake's active session and is intended to run inside Streamlit in Snowflake.

## Key Results

Results from the current cleaned dataset and validation queries:

| Metric | Result |
|---|---:|
| Total revenue | £10,642,110.80 |
| Invoices | 19,960 |
| Unique customers | 4,338 |
| Unique products | 3,921 |
| Units sold | 5,572,416 |
| Clean sales records | 524,874 |
| Highest-revenue month | November 2011 |
| Revenue in highest-revenue month | £1,503,866.78 |
| United Kingdom revenue | £9,001,744.09 |

*Figures reflect the current Snowflake table and documented cleaning rules. Results may vary if the source data or transformation rules change.*

## Technology Stack

- **Snowflake SQL** — data profiling, cleaning, transformations, aggregation, and validation
- **Python** — dashboard data handling and application logic
- **Streamlit** — interactive analytics dashboard
- **Pandas and Altair** — data manipulation and charting in the public demo
- **GitHub** — source control and project documentation

## Analysis and Dashboard Features

- Data-quality checks and final validation
- Cleaning of invalid dates, cancelled invoices, non-positive quantities/prices, and duplicate records
- KPI overview for revenue, invoices, customers, products, units, and cleaned records
- Monthly revenue trend and best sales month
- Top-selling product analysis
- Country-level sales analysis
- Customer spending segments
- Cancellation and data-quality summary
- CSV downloads for selected reports

## SQL Scripts

The [sql/](sql/) directory contains 13 analysis scripts:

| Script | Purpose |
|---|---|
| [01_data_quality_checks.sql](sql/01_data_quality_checks.sql) | Profile missing values, invalid records, and duplicates |
| [02_clean_sales_data.sql](sql/02_clean_sales_data.sql) | Transform raw data and create the cleaned table |
| [03_monthly_sales_report.sql](sql/03_monthly_sales_report.sql) | Calculate monthly sales metrics |
| [04_top_selling_products.sql](sql/04_top_selling_products.sql) | Rank products by sales performance |
| [05_sales_by_country.sql](sql/05_sales_by_country.sql) | Summarize sales by country |
| [06_best_sales_month.sql](sql/06_best_sales_month.sql) | Identify the highest-revenue month |
| [07_sales_kpis.sql](sql/07_sales_kpis.sql) | Calculate overall business KPIs |
| [08_customer_analysis.sql](sql/08_customer_analysis.sql) | Analyze customer purchasing metrics |
| [09_country_sales_analysis.sql](sql/09_country_sales_analysis.sql) | Examine country-level revenue contribution |
| [10_sales_trends.sql](sql/10_sales_trends.sql) | Analyze sales trends over time |
| [11_return_analysis.sql](sql/11_return_analysis.sql) | Inspect cancellation activity in raw data |
| [12_customer_segments.sql](sql/12_customer_segments.sql) | Group customers by spending level |
| [13_final_validation.sql](sql/13_final_validation.sql) | Validate the final cleaned dataset and totals |

## Report Exports

The following aggregated CSV reports are committed to the repository for review and use by the public demo.

| Report | File |
|---|---|
| Top-selling products | [top_selling_products.csv](data/top_selling_products.csv) |
| Sales by country | [sales_by_country.csv](data/sales_by_country.csv) |
| Daily sales trends | [sales_trends.csv](data/sales_trends.csv) |
| Monthly revenue | [monthly_revenue.csv](data/monthly_revenue.csv) |
| Customer segment summary | [customer_segments_summary.csv](data/customer_segments_summary.csv) |
| Country sales analysis | [country_sales_analysis.csv](data/country_sales_analysis.csv) |
| Sales KPIs | [sales_kpis.csv](data/sales_kpis.csv) |
| Best sales month | [best_sales_month.csv](data/best_sales_month.csv) |
| Final validation | [final_validation.csv](data/final_validation.csv) |
| Cancellation and data-quality summary | [cancellation_summary.csv](data/cancellation_summary.csv) |

Only summarized report exports are included. Customer-level analysis files containing individual customer identifiers are intentionally excluded.

## Data Source

**UCI Machine Learning Repository — Online Retail**

Dataset page: [https://archive.ics.uci.edu/dataset/352/online+retail](https://archive.ics.uci.edu/dataset/352/online+retail)

Review the source dataset's description and terms before redistributing the original data.

## Data Cleaning Rules

The cleaned table is **SALES_PROJECT.PUBLIC.CLEAN_ONLINE_RETAIL**, created from **SALES_PROJECT.PUBLIC.RAW_ONLINE_RETAIL**.

The cleaning workflow:
1. Parses invoice dates using the source format **DD-MM-YYYY HH24:MI**.
2. Excludes records without a valid invoice date.
3. Excludes cancelled invoices whose invoice number starts with **C**.
4. Keeps rows with positive quantity and unit price.
5. Removes duplicates based on standardized transaction fields.
6. Calculates line revenue as **SALES_AMOUNT = QUANTITY * UNITPRICE**.

The cancellation analysis queries the raw table because cancelled invoices are excluded from the main cleaned sales table.

## Run in Snowflake

1. Obtain the source dataset from the [UCI dataset page](https://archive.ics.uci.edu/dataset/352/online+retail) and load it into **SALES_PROJECT.PUBLIC.RAW_ONLINE_RETAIL**.
2. Open Snowflake Snowsight and run the SQL scripts from the **sql/** directory. Perform the data-quality checks and run **02_clean_sales_data.sql** before the downstream reporting scripts.
3. Run **13_final_validation.sql** and verify the output against the expected results for your source data and cleaning rules.
4. Create a Streamlit in Snowflake app and use [app/streamlit_app.py](app/streamlit_app.py) as the app source.
5. Ensure the active Snowflake role has the required privileges on the database, schema, and tables.

### Hosting Notes

- **app/streamlit_app.py** uses **get_active_session()** and is intended for Streamlit in Snowflake.
- **app/public_demo.py** reads static CSV exports from the repository's **data/** directory for the public portfolio demo.
- The public demo does not use Snowflake credentials. Its report figures remain unchanged until the exported CSV files are updated and the app redeploys.

## Repository Structure

```text
online-retail-sales-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── app/
│   ├── streamlit_app.py
│   └── public_demo.py
├── data/
│   ├── best_sales_month.csv
│   ├── cancellation_summary.csv
│   ├── country_sales_analysis.csv
│   ├── customer_segments_summary.csv
│   ├── final_validation.csv
│   ├── monthly_revenue.csv
│   ├── sales_by_country.csv
│   ├── sales_kpis.csv
│   ├── sales_trends.csv
│   └── top_selling_products.csv
└── sql/
    ├── 01_data_quality_checks.sql
    ├── 02_clean_sales_data.sql
    ├── 03_monthly_sales_report.sql
    ├── 04_top_selling_products.sql
    ├── 05_sales_by_country.sql
    ├── 06_best_sales_month.sql
    ├── 07_sales_kpis.sql
    ├── 08_customer_analysis.sql
    ├── 09_country_sales_analysis.sql
    ├── 10_sales_trends.sql
    ├── 11_return_analysis.sql
    ├── 12_customer_segments.sql
    └── 13_final_validation.sql
```

## Security and Data Handling

- Never commit Snowflake passwords, private keys, tokens, or other credentials.
- Do not publish customer-level exports or sensitive records.
- Use a secrets manager or secure environment configuration for any future live connection.
- Check the dataset's usage and redistribution terms before sharing source data.

## Future Improvements

- Add verified dashboard screenshots and a short walkthrough video.
- Add automated tests for key metrics and data-cleaning assumptions.
- Add the daily sales trend visualization to the public demo.
- Consider a secure live-data architecture if automatic refresh is required.

## Author

**Ravi Kiran**  
GitHub: [@Ravikiran9988](https://github.com/Ravikiran9988)

---

If you find this project useful, feel free to explore the SQL scripts and exported reports.
