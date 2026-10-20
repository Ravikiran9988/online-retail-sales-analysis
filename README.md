# Online Retail Sales Analysis

An end-to-end data analysis project using **Snowflake SQL** and **Streamlit in Snowflake** to explore online retail sales, identify business trends, and understand product, country, and customer performance.

## Project Overview

This project analyzes the UCI Online Retail transaction dataset. The workflow includes data-quality checks, cleaning and validation, SQL-based analysis, and an interactive dashboard.

The dashboard is designed to help answer questions such as:
- How are sales changing month by month?
- Which products generate the most revenue?
- Which countries contribute the most sales?
- How do customers differ by spending level?
- What patterns can be seen in returns and cancellations?

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

Based on the cleaned dataset and current dashboard:

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

*Note: These figures reflect the current cleaned table and dashboard. Results can vary based on cleaning rules and filters.*

## SQL Analysis

The project contains 13 SQL worksheets covering:

1. Data quality checks
2. Clean sales data creation
3. Monthly sales report
4. Top-selling products
5. Sales by country
6. Best sales month
7. Sales KPIs
8. Customer analysis
9. Country sales analysis
10. Sales trends
11. Return analysis
12. Customer segments
13. Final validation

## Data Cleaning Approach

The cleaned sales table applies these core rules:
- Exclude records without an invoice date.
- Exclude cancelled invoices whose invoice number begins with `C`.
- Keep records with positive quantity and unit price.
- Calculate sales amount as `QUANTITY * UNITPRICE`.

These choices make the sales analysis more consistent, but they also mean that cancelled transactions are not included in the main sales figures.

## Project Structure

The repository is intended to include files organized in a structure like this:

```text
online-retail-sales-analysis/
├── README.md
├── sql/
│   ├── 01_data_quality_checks.sql
│   ├── 02_clean_sales_data.sql
│   ├── 03_monthly_sales_report.sql
│   ├── 04_top_selling_products.sql
│   ├── 05_sales_by_country.sql
│   ├── 06_best_sales_month.sql
│   ├── 07_sales_kpis.sql
│   ├── 08_customer_analysis.sql
│   ├── 09_country_sales_analysis.sql
│   ├── 10_sales_trends.sql
│   ├── 11_return_analysis.sql
│   ├── 12_customer_segments.sql
│   └── 13_final_validation.sql
├── app/
│   └── streamlit_app.py
└── screenshots/
```

*The structure above is a suggested layout. Add the folders and files as they are uploaded to the repository.*

## Running the Project

1. Load the source retail dataset into Snowflake.
2. Run the SQL scripts in order, updating database, schema, and table names if needed.
3. Confirm that the cleaned table and analysis queries complete successfully.
4. Open the Streamlit app in Snowflake and ensure the app's active role can read the required tables.
5. Adjust the dashboard filters to explore the sales results.

The current dashboard uses Snowflake data, so it will not run on another hosting platform without configuring a compatible data source and credentials.

## Dashboard Screenshots

Screenshots can be added to the `screenshots/` folder and displayed here. For example:

```markdown
![Sales dashboard](screenshots/dashboard.png)
```

## Data Source

The project is based on the **Online Retail** dataset from the UCI Machine Learning Repository. Review the dataset page and usage terms before redistributing the raw data:

https://archive.ics.uci.edu/dataset/352/online+retail

## Security Notes

- Never commit Snowflake passwords, private keys, access tokens, or connection secrets.
- Do not commit private or restricted data.
- Use a secrets manager or environment-specific configuration for credentials.
- Verify that any dataset you publish can legally be redistributed.

## Future Improvements

- Add dashboard screenshots and a short demo video.
- Add reproducible SQL files and setup instructions.
- Create a publicly accessible demo with a safe, non-secret data connection.
- Add tests or validation queries for key metrics.

## Author

**Ravi Kiran**

GitHub: https://github.com/Ravikiran9988

---

If you find this project useful, feel free to explore the SQL analysis and dashboard implementation.
