# Public portfolio demo for Online Retail Sales Analysis.
# This version uses illustrative data so it can run without Snowflake credentials.
# It is intentionally separate from app/streamlit_app.py, which uses Streamlit in Snowflake.

import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Online Retail Sales Analysis | Demo", page_icon="📊", layout="wide")
st.title("📊 Online Retail Sales Analysis")
st.caption("Public portfolio demo • Snowflake SQL + Streamlit")

st.info(
    "This public demo uses illustrative example data to demonstrate the dashboard layout. "
    "It is not connected to the live Snowflake table. The full Snowflake-connected app is separate."
)

# Illustrative summary values based on the project's current cleaned-table KPIs.
# Charts below use small illustrative examples, not the complete transaction-level dataset.
with st.sidebar:
    st.header("Explore the demo")
    date_range = st.select_slider(
        "Example reporting period",
        options=["All year", "First half", "Second half"],
        value="All year",
    )
    selected_country = st.selectbox(
        "Example country",
        ["All countries", "United Kingdom", "Germany", "France", "EIRE"],
    )

kpis = [
    ("Total revenue (project result)", "£10,642,110.80"),
    ("Invoices", "19,960"),
    ("Unique customers", "4,338"),
    ("Unique products", "3,921"),
    ("Units sold", "5,572,416"),
    ("Clean sales records", "524,874"),
]
cols = st.columns(3)
for i, (label, value) in enumerate(kpis):
    cols[i % 3].metric(label, value)

st.divider()

monthly = pd.DataFrame({
    "Month": pd.to_datetime([
        "2011-01-01", "2011-02-01", "2011-03-01", "2011-04-01",
        "2011-05-01", "2011-06-01", "2011-07-01", "2011-08-01",
        "2011-09-01", "2011-10-01", "2011-11-01", "2011-12-01",
    ]),
    "Revenue (£)": [560000, 500000, 680000, 490000, 720000, 700000,
                    680000, 710000, 980000, 1050000, 1503866.78, 800000],
})
products = pd.DataFrame({
    "Product": ["Product example A", "Product example B", "Product example C",
                "Product example D", "Product example E"],
    "Revenue (£)": [82000, 67000, 54000, 46000, 39000],
})
countries = pd.DataFrame({
    "Country": ["United Kingdom", "Germany", "France", "EIRE", "Spain"],
    "Revenue (£)": [9001744.09, 230000, 180000, 150000, 90000],
})

if date_range == "First half":
    monthly = monthly[monthly["Month"].dt.month <= 6]
elif date_range == "Second half":
    monthly = monthly[monthly["Month"].dt.month >= 7]

if selected_country != "All countries":
    countries = countries[countries["Country"] == selected_country]

left, right = st.columns(2)
with left:
    st.subheader("Monthly revenue trend")
    st.caption("Illustrative monthly series; peak-month value shown from the project result.")
    line = alt.Chart(monthly).mark_line(point=True).encode(
        x=alt.X("Month:T", title="Month"),
        y=alt.Y("Revenue (£):Q", title="Revenue (£)", axis=alt.Axis(format=",.0f")),
        tooltip=[alt.Tooltip("Month:T", title="Month"),
                 alt.Tooltip("Revenue (£):Q", format=",.2f")],
    ).properties(height=320)
    st.altair_chart(line, width="stretch")

with right:
    st.subheader("Top products")
    st.caption("Example products for demonstrating the chart.")
    bars = alt.Chart(products).mark_bar().encode(
        x=alt.X("Revenue (£):Q", title="Revenue (£)"),
        y=alt.Y("Product:N", sort="-x", title="Product"),
        tooltip=["Product", alt.Tooltip("Revenue (£):Q", format=",.2f")],
    ).properties(height=320)
    st.altair_chart(bars, width="stretch")

st.subheader("Country performance")
st.caption("United Kingdom revenue reflects the project result; other country values are illustrative examples.")
st.dataframe(countries, width="stretch", hide_index=True)

st.subheader("Customer spending segments")
segments = pd.DataFrame({
    "Customer segment": ["High value", "Medium value", "Low value"],
    "Example customers": [340, 1250, 2748],
})
seg_chart = alt.Chart(segments).mark_bar().encode(
    x=alt.X("Example customers:Q", title="Example customer count"),
    y=alt.Y("Customer segment:N", sort="-x", title="Segment"),
    tooltip=["Customer segment", "Example customers"],
).properties(height=220)
st.altair_chart(seg_chart, width="stretch")
st.caption("Customer-segment counts are illustrative and do not represent calculated final segment totals.")

csv = monthly.to_csv(index=False).encode("utf-8")
st.download_button("Download example monthly data (CSV)", csv, "example_monthly_revenue.csv", "text/csv")

st.markdown("---")
st.caption("Project repository: https://github.com/Ravikiran9988/online-retail-sales-analysis")
