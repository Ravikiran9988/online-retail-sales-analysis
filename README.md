# Online Retail Sales Analysis

An end-to-end data analysis project using **Snowflake SQL** and **Streamlit in Snowflake** to explore online retail sales, identify business trends, and understand product, country, and customer performance.

## Project Overview

This project analyzes the UCI Online Retail transaction dataset. The workflow includes data-quality checks, cleaning and validation, SQL-based analysis, and an interactive dashboard.

The dashboard is designed to help answer questions such as:
- How are sales changing month by month?
- Which products generate the most revenue?
- Which countries contribute the most sales?
- How do customers differ by spending level?
- What patterns can be seen in cancellations?

## Tools and Technologies

- **Snowflake SQL** — data cleaning, validation, aggregations, and analysis
- **Streamlit in Snowflake** — interactive dashboard
- **Python** — dashboard logic and visualizations
- **GitHub** — project documentation and version control

## Dashboard Features

- Date-range and country filters
- KPI cards for total revenue, invoices, customers, products, units sold, and sales records
- Monthly revenue trend
- Top 10 products by sales
- Country-level sales performance
- Customer spending segmentation
- CSV downloads for analysis results

## Key Results

Based on the current cleaned dataset and dashboard:

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

*These results reflect the current Snowflake table and cleaning choices. Re-running the scripts with different source data or cleaning rules may change the figures.*

## SQL Analysis

The `sql/` folder contains 13 scripts:

1. `01_data_quality_checks.sql` — inspect missing values, invalid records, and duplicates
2. `02_clean_sales_data.sql` — standardize and create the cleaned table
3. `03_monthly_sales_report.sql` — monthly revenue and order metrics
4. `04_top_selling_products.sql` — products ranked by revenue
5. `05_sales_by_country.sql` — sales metrics by country
6. `06_best_sales_month.sql` — highest-revenue month
7. `07_sales_kpis.sql` — overall business KPIs
8. `08_customer_analysis.sql` — customer-level purchasing metrics
9. `09_country_sales_analysis.sql` — revenue contribution by country
10. `10_sales_trends.sql` — month-over-month revenue changes
11. `11_return_analysis.sql` — cancellation activity in the raw data
12. `12_customer_segments.sql` — spending-based customer segments
13. `13_final_validation.sql` — final table and data-quality checks

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
│   ├── monthly_revenue.csv
│   ├── customer_segments_summary.csv
│   ├── country_sales_analysis.csv
│   └── other aggregated report CSVs
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

## Data Cleaning Approach

The cleaned table:
- Parses invoice dates using the source format `DD-MM-YYYY HH24:MI`.
- Excludes rows without a valid invoice date.
- Excludes cancelled invoices whose invoice number begins with `C`.
- Keeps records with positive quantity and unit price.
- Removes duplicate rows based on the standardized transaction fields.
- Calculates `SALES_AMOUNT = QUANTITY * UNITPRICE`.

Cancelled invoices are excluded from the main sales table; the cancellation analysis therefore queries the raw table.

## Setup and Usage

1. Load the Online Retail source dataset into `SALES_PROJECT.PUBLIC.RAW_ONLINE_RETAIL`.
2. Open Snowflake Snowsight and run the SQL scripts in `sql/` as appropriate. Run the data-cleaning script before the reporting scripts.
3. Confirm that `SALES_PROJECT.PUBLIC.CLEAN_ONLINE_RETAIL` exists and that the validation query returns sensible results.
4. Create or open a Streamlit app in Snowflake and use `app/streamlit_app.py` as the app source.
5. Ensure the active Snowflake role has permission to query the required database, schema, and table.
6. Use the date and country filters to explore results and download the displayed analysis as CSV files.

**Hosting note:** The dashboard code uses `get_active_session()`, which is intended for Streamlit in Snowflake. It will not run unchanged on Streamlit Community Cloud or another standalone host; that requires a separate secure Snowflake connection or a different data source.

## Screenshots

Dashboard screenshots can be added to a `screenshots/` folder and embedded here once available.

## Data Source and CSV Reports

The project uses the **Online Retail** dataset from the UCI Machine Learning Repository. Visit the dataset page to review the description, download options, and usage terms:

[Online Retail Dataset — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail)

The repository also includes aggregated CSV exports of selected Snowflake query results for the public Streamlit demo:

- [Top-selling products](data/top_selling_products.csv)
- [Sales by country](data/sales_by_country.csv)
- [Monthly revenue report](data/monthly_revenue.csv)
- [Customer segment summary](data/customer_segments_summary.csv)
- [Country sales analysis](data/country_sales_analysis.csv)
- [Sales KPIs](data/sales_kpis.csv)
- [Best sales month](data/best_sales_month.csv)
- [Final validation results](data/final_validation.csv)
- [Cancellation and data-quality summary](data/cancellation_summary.csv)

These CSV files contain summarized analysis results, not the original transaction-level dataset. Individual customer-level files are intentionally not published. The public demo uses static exports, so the figures do not automatically refresh when the Snowflake table changes.

## Security Notes

- Never commit Snowflake passwords, private keys, access tokens, or connection secrets.
- Do not commit private or restricted data.
- Use a secrets manager or environment-specific configuration for credentials.
- Verify that any dataset you publish can legally be redistributed.

## Future Improvements

- Add dashboard screenshots and a short demo video.
- Add automated checks for key metrics and cleaning assumptions.
- Create a publicly accessible demo with a safe, non-secret data connection.
- Document the Snowflake setup and permissions in more detail.

## Author

**Ravi Kiran**

GitHub: https://github.com/Ravikiran9988

---

Thanks for checking out this project!
