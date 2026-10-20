# Public portfolio dashboard using actual aggregated Snowflake exports.
# No Snowflake credentials or customer-level records are included.
import pandas as pd
import streamlit as st
import altair as alt
from pathlib import Path

st.set_page_config(page_title="Online Retail Sales Analysis", page_icon="📊", layout="wide")
st.title("📊 Online Retail Sales Analysis")
st.caption("Public portfolio dashboard • Snowflake SQL + Streamlit")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_csv(name):
    return pd.read_csv(DATA_DIR / name)

monthly = load_csv("monthly_revenue.csv")
segments = load_csv("customer_segments_summary.csv")
kpis = load_csv("project_kpis.csv").iloc[0]
returns = load_csv("cancellation_summary.csv").iloc[0]

monthly["SALES_MONTH"] = pd.to_datetime(monthly["SALES_MONTH"])
segments["CUSTOMER_SEGMENT"] = segments["CUSTOMER_SEGMENT"].astype(str)

with st.sidebar:
    st.header("Filters")
    start_date = st.date_input("Start month", value=monthly["SALES_MONTH"].min().date(),
                               min_value=monthly["SALES_MONTH"].min().date(),
                               max_value=monthly["SALES_MONTH"].max().date())
    end_date = st.date_input("End month", value=monthly["SALES_MONTH"].max().date(),
                             min_value=monthly["SALES_MONTH"].min().date(),
                             max_value=monthly["SALES_MONTH"].max().date())

if start_date > end_date:
    st.error("Start month must be before or equal to end month.")
    st.stop()

filtered_monthly = monthly[
    (monthly["SALES_MONTH"].dt.date >= start_date) &
    (monthly["SALES_MONTH"].dt.date <= end_date)
].copy()

# Totals at project level are the actual final validation values. When a date filter
# narrows the view, the monthly chart and table respond to that filter.
c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue (full dataset)", f"£{float(kpis['TOTAL_REVENUE']):,.2f}")
c2.metric("Invoices (full dataset)", f"{int(kpis['TOTAL_INVOICES']):,}")
c3.metric("Unique Customers", f"{int(kpis['UNIQUE_CUSTOMERS']):,}")
c4, c5, c6 = st.columns(3)
c4.metric("Unique Products", f"{int(kpis['UNIQUE_PRODUCTS']):,}")
c5.metric("Units Sold", f"{int(kpis['TOTAL_UNITS_SOLD']):,}")
c6.metric("Clean Sales Records", f"{int(kpis['TOTAL_ROWS']):,}")

st.info("All KPI values and report figures shown here are based on exported Snowflake results. The date filter affects the monthly report chart and table; overall KPI cards represent the full cleaned dataset.")

left, right = st.columns(2)
with left:
    st.subheader("Monthly Revenue Trend")
    chart = alt.Chart(filtered_monthly).mark_line(point=True).encode(
        x=alt.X("SALES_MONTH:T", title="Month"),
        y=alt.Y("MONTHLY_REVENUE:Q", title="Revenue (£)", axis=alt.Axis(format=",.0f")),
        tooltip=[
            alt.Tooltip("SALES_MONTH:T", title="Month"),
            alt.Tooltip("MONTHLY_REVENUE:Q", title="Revenue", format=",.2f"),
            alt.Tooltip("TOTAL_INVOICES:Q", title="Invoices", format=","),
            alt.Tooltip("TOTAL_UNITS_SOLD:Q", title="Units sold", format=","),
        ],
    ).properties(height=330)
    st.altair_chart(chart, width="stretch")

with right:
    st.subheader("Customer Spending Segments")
    seg_chart = alt.Chart(segments).mark_bar().encode(
        x=alt.X("CUSTOMER_COUNT:Q", title="Customers"),
        y=alt.Y("CUSTOMER_SEGMENT:N", sort="-x", title="Segment"),
        color=alt.Color("CUSTOMER_SEGMENT:N", legend=None),
        tooltip=[
            alt.Tooltip("CUSTOMER_SEGMENT:N", title="Segment"),
            alt.Tooltip("CUSTOMER_COUNT:Q", title="Customers", format=","),
            alt.Tooltip("TOTAL_REVENUE:Q", title="Segment revenue", format=",.2f"),
        ],
    ).properties(height=250)
    st.altair_chart(seg_chart, width="stretch")
    st.dataframe(segments, width="stretch", hide_index=True)

st.subheader("Monthly Sales Report")
display_monthly = filtered_monthly.copy()
display_monthly["SALES_MONTH"] = display_monthly["SALES_MONTH"].dt.strftime("%Y-%m")
display_monthly["MONTHLY_REVENUE"] = display_monthly["MONTHLY_REVENUE"].map(lambda x: f"£{x:,.2f}")
st.dataframe(display_monthly, width="stretch", hide_index=True)

st.subheader("Cancellation and Data-Quality Summary")
r1, r2, r3, r4 = st.columns(4)
r1.metric("Cancelled rows", f"{int(returns['CANCELLED_ROWS']):,}")
r2.metric("Negative quantity rows", f"{int(returns['NEGATIVE_QUANTITY_ROWS']):,}")
r3.metric("Non-positive price rows", f"{int(returns['NONPOSITIVE_PRICE_ROWS']):,}")
r4.metric("Negative-quantity value", f"£{float(returns['NEGATIVE_QUANTITY_VALUE']):,.2f}")

st.download_button(
    "Download monthly report CSV",
    filtered_monthly.to_csv(index=False).encode("utf-8"),
    "monthly_revenue.csv",
    "text/csv",
)
st.download_button(
    "Download customer segment summary CSV",
    segments.to_csv(index=False).encode("utf-8"),
    "customer_segments_summary.csv",
    "text/csv",
)
st.caption("Data is a static export of aggregated Snowflake query results. It does not refresh automatically from Snowflake.")
