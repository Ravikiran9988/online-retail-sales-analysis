# Online Retail Sales Analysis dashboard
# Designed for Streamlit in Snowflake; reads from SALES_PROJECT.PUBLIC.CLEAN_ONLINE_RETAIL.

import io
import pandas as pd
import streamlit as st
import altair as alt
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Online Retail Sales Dashboard", page_icon="📊", layout="wide")
st.title("📊 Online Retail Sales Dashboard")
st.caption("Explore sales trends, products, countries, and customer spending.")

@st.cache_resource
def get_session():
    return get_active_session()

session = get_session()
TABLE_NAME = "SALES_PROJECT.PUBLIC.CLEAN_ONLINE_RETAIL"

@st.cache_data(ttl=300)
def load_filter_values():
    countries = session.sql(f"SELECT DISTINCT COUNTRY FROM {TABLE_NAME} WHERE COUNTRY IS NOT NULL ORDER BY COUNTRY").to_pandas()
    bounds = session.sql(f"SELECT MIN(INVOICE_DATE)::DATE AS MIN_DATE, MAX(INVOICE_DATE)::DATE AS MAX_DATE FROM {TABLE_NAME}").to_pandas()
    return countries["COUNTRY"].dropna().tolist(), pd.to_datetime(bounds.iloc[0]["MIN_DATE"]).date(), pd.to_datetime(bounds.iloc[0]["MAX_DATE"]).date()

countries, min_date, max_date = load_filter_values()

with st.sidebar:
    st.header("Filters")
    selected_dates = st.date_input("Invoice date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    selected_countries = st.multiselect("Country", options=countries, default=[],
                                        help="Leave empty to include all countries.")

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
    start_date = end_date = selected_dates[0]
else:
    start_date, end_date = min_date, max_date

where_parts = ["INVOICE_DATE >= TO_TIMESTAMP_NTZ(?)", "INVOICE_DATE < DATEADD(day, 1, TO_TIMESTAMP_NTZ(?))"]
params = [str(start_date), str(end_date)]
if selected_countries:
    placeholders = ", ".join(["?"] * len(selected_countries))
    where_parts.append(f"COUNTRY IN ({placeholders})")
    params.extend(selected_countries)
where_sql = " AND ".join(where_parts)

@st.cache_data(ttl=300)
def query_df(query, params_tuple=()):
    return session.sql(query, params=list(params_tuple)).to_pandas()

kpi_query = f"""
SELECT ROUND(COALESCE(SUM(SALES_AMOUNT), 0), 2) AS TOTAL_REVENUE,
       COUNT(DISTINCT INVOICENO) AS TOTAL_INVOICES,
       COUNT(DISTINCT CUSTOMERID) AS UNIQUE_CUSTOMERS,
       COUNT(DISTINCT STOCKCODE) AS UNIQUE_PRODUCTS,
       COALESCE(SUM(QUANTITY), 0) AS UNITS_SOLD,
       COUNT(*) AS SALES_RECORDS
FROM {TABLE_NAME}
WHERE {where_sql}
"""
kpis = query_df(kpi_query, tuple(params)).iloc[0]

def money(value):
    return f"£{float(value or 0):,.2f}"

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", money(kpis["TOTAL_REVENUE"]))
c2.metric("Total Invoices", f'{int(kpis["TOTAL_INVOICES"]):,}')
c3.metric("Unique Customers", f'{int(kpis["UNIQUE_CUSTOMERS"]):,}')
c4, c5, c6 = st.columns(3)
c4.metric("Unique Products", f'{int(kpis["UNIQUE_PRODUCTS"]):,}')
c5.metric("Units Sold", f'{int(kpis["UNITS_SOLD"]):,}')
c6.metric("Sales Records", f'{int(kpis["SALES_RECORDS"]):,}')

st.divider()
monthly = query_df(f"""
SELECT DATE_TRUNC('MONTH', INVOICE_DATE)::DATE AS SALES_MONTH,
       ROUND(SUM(SALES_AMOUNT), 2) AS REVENUE
FROM {TABLE_NAME}
WHERE {where_sql}
GROUP BY 1 ORDER BY 1
""", tuple(params))
products = query_df(f"""
SELECT STOCKCODE, MAX(DESCRIPTION) AS DESCRIPTION,
       SUM(QUANTITY) AS UNITS_SOLD, ROUND(SUM(SALES_AMOUNT), 2) AS REVENUE
FROM {TABLE_NAME}
WHERE {where_sql}
GROUP BY STOCKCODE ORDER BY REVENUE DESC LIMIT 10
""", tuple(params))
country_sales = query_df(f"""
SELECT COUNTRY, ROUND(SUM(SALES_AMOUNT), 2) AS REVENUE,
       COUNT(DISTINCT INVOICENO) AS INVOICES
FROM {TABLE_NAME}
WHERE {where_sql}
GROUP BY COUNTRY ORDER BY REVENUE DESC LIMIT 15
""", tuple(params))
segments = query_df(f"""
WITH customer_spend AS (
    SELECT CUSTOMERID, SUM(SALES_AMOUNT) AS TOTAL_SPEND
    FROM {TABLE_NAME}
    WHERE {where_sql} AND CUSTOMERID IS NOT NULL
    GROUP BY CUSTOMERID
)
SELECT CASE WHEN TOTAL_SPEND >= 5000 THEN 'High Value'
            WHEN TOTAL_SPEND >= 1000 THEN 'Medium Value'
            ELSE 'Low Value' END AS CUSTOMER_SEGMENT,
       COUNT(*) AS CUSTOMER_COUNT,
       ROUND(SUM(TOTAL_SPEND), 2) AS REVENUE
FROM customer_spend
GROUP BY 1 ORDER BY REVENUE DESC
""", tuple(params))

left, right = st.columns(2)
with left:
    st.subheader("Monthly Revenue Trend")
    if not monthly.empty:
        chart = alt.Chart(monthly).mark_line(point=True).encode(
            x=alt.X("SALES_MONTH:T", title="Month"),
            y=alt.Y("REVENUE:Q", title="Revenue (£)", axis=alt.Axis(format=",.0f")),
            tooltip=["SALES_MONTH:T", alt.Tooltip("REVENUE:Q", format=",.2f")]
        ).properties(height=320)
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No monthly data for these filters.")
with right:
    st.subheader("Top 10 Products by Revenue")
    if not products.empty:
        products["PRODUCT_LABEL"] = products["STOCKCODE"].astype(str) + " — " + products["DESCRIPTION"].fillna("").astype(str).str.slice(0, 40)
        chart = alt.Chart(products).mark_bar().encode(
            x=alt.X("REVENUE:Q", title="Revenue (£)"),
            y=alt.Y("PRODUCT_LABEL:N", sort="-x", title="Product"),
            tooltip=["STOCKCODE:N", "DESCRIPTION:N", "UNITS_SOLD:Q", alt.Tooltip("REVENUE:Q", format=",.2f")]
        ).properties(height=360)
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No product data for these filters.")

left, right = st.columns(2)
with left:
    st.subheader("Country Performance")
    st.dataframe(country_sales, width="stretch", hide_index=True)
with right:
    st.subheader("Customer Spending Segments")
    if not segments.empty:
        st.bar_chart(segments.set_index("CUSTOMER_SEGMENT")[["CUSTOMER_COUNT"]], width="stretch")
        st.dataframe(segments, width="stretch", hide_index=True)
    else:
        st.info("No customer data for these filters.")

st.subheader("Download Results")
d1, d2, d3, d4 = st.columns(4)
d1.download_button("Monthly revenue CSV", monthly.to_csv(index=False).encode("utf-8"), "monthly_revenue.csv", "text/csv")
d2.download_button("Top products CSV", products.to_csv(index=False).encode("utf-8"), "top_products.csv", "text/csv")
d3.download_button("Country sales CSV", country_sales.to_csv(index=False).encode("utf-8"), "country_sales.csv", "text/csv")
d4.download_button("Customer segments CSV", segments.to_csv(index=False).encode("utf-8"), "customer_segments.csv", "text/csv")

st.caption("Data source: SALES_PROJECT.PUBLIC.CLEAN_ONLINE_RETAIL. Results reflect the selected date and country filters.")
