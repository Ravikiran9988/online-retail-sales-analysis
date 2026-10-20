# Exported Snowflake Results

These CSV files are aggregated results exported from the project's Snowflake worksheets and used by the public portfolio dashboard.

- `monthly_revenue.csv`: monthly invoice counts, units, and revenue.
- `country_sales_analysis.csv`: country-level sales results.
- `best_sales_month.csv`: highest-revenue month.
- `project_kpis.csv` and `sales_kpis.csv`: overall KPI results.
- `final_validation.csv`: cleaned-table validation totals.
- `customer_segments_summary.csv`: aggregated customer segment totals only.
- `cancellation_summary.csv`: cancellation/data-quality summary.

Customer-level exports containing customer IDs are intentionally not published. The dashboard uses static exports and does not refresh automatically from Snowflake.
