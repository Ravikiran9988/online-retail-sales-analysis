# Public portfolio dashboard built from aggregated Snowflake exports.
# This app intentionally avoids Snowflake credentials and customer-level records.
import pandas as pd
import streamlit as st
import altair as alt
from pathlib import Path

st.set_page_config(
    page_title="Online Retail Sales Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

st.title("📊 Online Retail Sales Analysis")
st.markdown(
    "Explore cleaned retail sales, monthly trends, country performance, "
    "customer segments, and data-quality findings."
)
st.caption("PORTFOLIO DEMO  /  Snowflake SQL · Streamlit · Aggregated exported results")

@st.cache_data
def load_csv(name):
    path = DATA_DIR / name
    if not path.exists():
        return None
    return pd.read_csv(path)

monthly = load_csv("monthly_revenue.csv")
kpis_df = load_csv("project_kpis.csv")
segments = load_csv("customer_segments_summary.csv")
quality_df = load_csv("cancellation_summary.csv")
countries = load_csv("country_sales_analysis.csv")
best_month_df = load_csv("best_sales_month.csv")
sales_kpis = load_csv("sales_kpis.csv")

if monthly is None or kpis_df is None:
    st.error("Required exported result files are missing from the repository's data/ folder.")
    st.stop()

monthly["SALES_MONTH"] = pd.to_datetime(monthly["SALES_MONTH"], errors="coerce")
monthly = monthly.dropna(subset=["SALES_MONTH"]).sort_values("SALES_MONTH")
kpis = kpis_df.iloc[0]

# Sidebar date filters affect monthly reports and trends. Summary KPI cards remain
# full-dataset figures, matching the exported final validation results.
with st.sidebar:
    st.header("Dashboard Controls")
    st.caption("Filter the monthly trend and report.")
    min_month = monthly["SALES_MONTH"].min().date()
    max_month = monthly["SALES_MONTH"].max().date()
    start_date = st.date_input(
        "Start date",
        value=min_month,
        min_value=min_month,
        max_value=max_month,
    )
    end_date = st.date_input(
        "End date",
        value=max_month,
        min_value=min_month,
        max_value=max_month,
    )

if start_date > end_date:
    st.error("The start date cannot be later than the end date.")
    st.stop()

filtered_monthly = monthly[
    monthly["SALES_MONTH"].dt.date.between(start_date, end_date)
].copy()

st.divider()
st.header("Performance Overview")
st.caption("Full cleaned-dataset totals from the exported Snowflake validation results.")

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"£{float(kpis['TOTAL_REVENUE']):,.2f}")
c2.metric("Total Invoices", f"{int(kpis['TOTAL_INVOICES']):,}")
c3.metric("Unique Customers", f"{int(kpis['UNIQUE_CUSTOMERS']):,}")
c4, c5, c6 = st.columns(3)
c4.metric("Unique Products", f"{int(kpis['UNIQUE_PRODUCTS']):,}")
c5.metric("Units Sold", f"{int(kpis['TOTAL_UNITS_SOLD']):,}")
c6.metric("Clean Sales Records", f"{int(kpis['TOTAL_ROWS']):,}")

if best_month_df is not None and not best_month_df.empty:
    best = best_month_df.iloc[0]
    month_name = str(best.iloc[0])[:7]
    revenue_value = pd.to_numeric(best.iloc[-1], errors="coerce")
    if pd.notna(revenue_value):
        st.success(f"Best sales month: {month_name} · Revenue: £{revenue_value:,.2f}")

st.info(
    "This public dashboard uses static, aggregated exports from Snowflake. "
    "The date filter updates monthly charts and tables; KPI cards show full-dataset totals. "
    "The demo does not connect to Snowflake or refresh automatically."
)

st.divider()
st.header("📈 Monthly Revenue Trend")
if filtered_monthly.empty:
    st.info("No monthly results exist for the selected dates.")
else:
    chart = alt.Chart(filtered_monthly).mark_line(point=True).encode(
        x=alt.X("SALES_MONTH:T", title="Month"),
        y=alt.Y("MONTHLY_REVENUE:Q", title="Revenue (£)", axis=alt.Axis(format=",.0f")),
        tooltip=[
            alt.Tooltip("SALES_MONTH:T", title="Month"),
            alt.Tooltip("MONTHLY_REVENUE:Q", title="Revenue", format=",.2f"),
            alt.Tooltip("TOTAL_INVOICES:Q", title="Invoices", format=","),
            alt.Tooltip("TOTAL_UNITS_SOLD:Q", title="Units sold", format=","),
        ],
    ).properties(height=350)
    st.altair_chart(chart, width="stretch")

    monthly_display = filtered_monthly.copy()
    monthly_display["SALES_MONTH"] = monthly_display["SALES_MONTH"].dt.strftime("%Y-%m")
    st.subheader("Monthly Sales Report")
    st.dataframe(monthly_display, width="stretch", hide_index=True)
    st.download_button(
        "Download monthly report CSV",
        filtered_monthly.to_csv(index=False).encode("utf-8"),
        "monthly_revenue.csv",
        "text/csv",
    )

if countries is not None and not countries.empty:
    st.divider()
    st.header("🌍 Country Performance")
    country_revenue_col = "TOTAL_REVENUE" if "TOTAL_REVENUE" in countries.columns else None
    country_name_col = "COUNTRY" if "COUNTRY" in countries.columns else None
    if country_revenue_col and country_name_col:
        countries[country_revenue_col] = pd.to_numeric(countries[country_revenue_col], errors="coerce")
        top_countries = countries.sort_values(country_revenue_col, ascending=False).head(10)
        country_chart = alt.Chart(top_countries).mark_bar().encode(
            x=alt.X(f"{country_revenue_col}:Q", title="Revenue (£)", axis=alt.Axis(format=",.0f")),
            y=alt.Y(f"{country_name_col}:N", sort="-x", title="Country"),
            tooltip=[
                alt.Tooltip(f"{country_name_col}:N", title="Country"),
                alt.Tooltip(f"{country_revenue_col}:Q", title="Revenue", format=",.2f"),
            ],
        ).properties(height=360)
        st.altair_chart(country_chart, width="stretch")
    st.dataframe(countries, width="stretch", hide_index=True)
    st.download_button(
        "Download country analysis CSV",
        countries.to_csv(index=False).encode("utf-8"),
        "country_sales_analysis.csv",
        "text/csv",
    )

if segments is not None and not segments.empty:
    st.divider()
    st.header("👥 Customer Spending Segments")
    st.caption("Aggregated segment totals only; individual customer IDs are not published.")
    count_col = "CUSTOMER_COUNT" if "CUSTOMER_COUNT" in segments.columns else None
    segment_col = "CUSTOMER_SEGMENT" if "CUSTOMER_SEGMENT" in segments.columns else None
    if count_col and segment_col:
        seg_chart = alt.Chart(segments).mark_bar().encode(
            x=alt.X(f"{count_col}:Q", title="Customers"),
            y=alt.Y(f"{segment_col}:N", sort="-x", title="Segment"),
            tooltip=[
                alt.Tooltip(f"{segment_col}:N", title="Segment"),
                alt.Tooltip(f"{count_col}:Q", title="Customers", format=","),
            ],
        ).properties(height=280)
        st.altair_chart(seg_chart, width="stretch")
    st.dataframe(segments, width="stretch", hide_index=True)
    st.download_button(
        "Download customer segment summary CSV",
        segments.to_csv(index=False).encode("utf-8"),
        "customer_segments_summary.csv",
        "text/csv",
    )

if quality_df is not None and not quality_df.empty:
    st.divider()
    st.header("🧹 Cancellation & Data-Quality Summary")
    quality = quality_df.iloc[0]
    metric_columns = st.columns(min(4, len(quality_df.columns)))
    for i, col in enumerate(quality_df.columns):
        value = pd.to_numeric(pd.Series([quality[col]]), errors="coerce").iloc[0]
        if pd.notna(value):
            label = col.replace("_", " ").title()
            if "VALUE" in col:
                metric_columns[i % len(metric_columns)].metric(label, f"£{value:,.2f}")
            else:
                metric_columns[i % len(metric_columns)].metric(label, f"{int(value):,}")
    st.dataframe(quality_df, width="stretch", hide_index=True)

if sales_kpis is not None and not sales_kpis.empty:
    with st.expander("View additional exported KPI validation"):
        st.dataframe(sales_kpis, width="stretch", hide_index=True)

st.divider()
st.caption(
    "Built with Streamlit and Snowflake SQL. Public demo uses static aggregated CSV exports; "
    "the Snowflake-hosted app queries the cleaned Snowflake table directly."
)
