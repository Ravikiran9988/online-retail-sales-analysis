
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Online Retail Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

session = get_active_session()
TABLE = "SALES_PROJECT.PUBLIC.CLEAN_ONLINE_RETAIL"


# =========================================================
# CUSTOM STYLING
# =========================================================
st.markdown("""
<style>
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }

    h1 {
        letter-spacing: -1px;
        font-weight: 700;
    }

    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.20);
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.20);
    }

    div[data-testid="stMetricLabel"] p {
        font-size: 0.95rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.65rem;
    }

    .dashboard-caption {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA LOADER
# =========================================================
@st.cache_data(ttl=300, show_spinner=False)
def load_data(query):
    return session.sql(query).to_pandas()


def safe_int(value):
    return int(value) if pd.notna(value) else 0


def safe_money(value):
    return f"£{value:,.2f}" if pd.notna(value) else "£0.00"


def safe_sql_string(value):
    return str(value).replace("'", "''")


# =========================================================
# HEADER
# =========================================================
st.title("📊 Online Retail Analytics")

st.markdown(
    "Explore sales performance, product intelligence, "
    "geographic trends, and customer spending."
)

st.caption("DATA SOURCE  /  Snowflake · Online Retail Dataset")


# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.title("Dashboard Controls")
st.sidebar.caption(
    "Filter all dashboard metrics, charts, and reports."
)

date_limits = load_data(f"""
    SELECT
        MIN(TO_DATE(INVOICE_DATE)) AS MIN_DATE,
        MAX(TO_DATE(INVOICE_DATE)) AS MAX_DATE
    FROM {TABLE}
""")

if date_limits.empty or pd.isna(date_limits.iloc[0]["MIN_DATE"]):
    st.error("No valid invoice dates were found in the cleaned dataset.")
    st.stop()

min_date = pd.to_datetime(
    date_limits.iloc[0]["MIN_DATE"]
).date()

max_date = pd.to_datetime(
    date_limits.iloc[0]["MAX_DATE"]
).date()

country_df = load_data(f"""
    SELECT DISTINCT COUNTRY
    FROM {TABLE}
    WHERE COUNTRY IS NOT NULL
    ORDER BY COUNTRY
""")

country_options = (
    ["All Countries"] + country_df["COUNTRY"].astype(str).tolist()
)

date_range = st.sidebar.date_input(
    "Invoice date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="YYYY-MM-DD"
)

selected_country = st.sidebar.selectbox(
    "Country",
    options=country_options,
    index=0
)

st.sidebar.divider()

st.sidebar.markdown("**Active Filters**")
st.sidebar.caption(f"Country: {selected_country}")
st.sidebar.caption(
    f"Date range: {date_range[0]} to "
    f"{date_range[1] if isinstance(date_range, (tuple, list)) and len(date_range) == 2 else 'Select end date'}"
)

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.info("Please select both a start date and an end date.")
    st.stop()

start_date, end_date = date_range

if start_date > end_date:
    st.warning("The start date cannot be later than the end date.")
    st.stop()

start_sql = start_date.strftime("%Y-%m-%d")
end_sql = end_date.strftime("%Y-%m-%d")

country_condition = ""

if selected_country != "All Countries":
    country_condition = (
        f" AND COUNTRY = '{safe_sql_string(selected_country)}'"
    )

# This shared filter is applied to every dashboard query.
FILTER = f"""
    TO_DATE(INVOICE_DATE)
        BETWEEN '{start_sql}' AND '{end_sql}'
    {country_condition}
"""


# =========================================================
# PERFORMANCE OVERVIEW
# =========================================================
st.divider()
st.header("Performance Overview")
st.caption("Key metrics for the selected dates and country.")

kpi_df = load_data(f"""
    SELECT
        COUNT(*) AS SALES_RECORDS,
        COUNT(DISTINCT INVOICENO) AS TOTAL_INVOICES,
        COUNT(DISTINCT CUSTOMERID) AS UNIQUE_CUSTOMERS,
        COUNT(DISTINCT STOCKCODE) AS UNIQUE_PRODUCTS,
        COALESCE(SUM(QUANTITY), 0) AS TOTAL_UNITS_SOLD,
        COALESCE(ROUND(SUM(SALES_AMOUNT), 2), 0) AS TOTAL_REVENUE
    FROM {TABLE}
    WHERE {FILTER}
""")

kpi = kpi_df.iloc[0]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Revenue",
    safe_money(kpi["TOTAL_REVENUE"])
)

c2.metric(
    "Total Invoices",
    f'{safe_int(kpi["TOTAL_INVOICES"]):,}'
)

c3.metric(
    "Unique Customers",
    f'{safe_int(kpi["UNIQUE_CUSTOMERS"]):,}'
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Unique Products",
    f'{safe_int(kpi["UNIQUE_PRODUCTS"]):,}'
)

c5.metric(
    "Units Sold",
    f'{safe_int(kpi["TOTAL_UNITS_SOLD"]):,}'
)

c6.metric(
    "Sales Records",
    f'{safe_int(kpi["SALES_RECORDS"]):,}'
)


# =========================================================
# MONTHLY REVENUE TREND
# =========================================================
st.divider()
st.header("📈 Monthly Revenue Trend")

monthly = load_data(f"""
    SELECT
        TO_CHAR(
            DATE_TRUNC('MONTH', INVOICE_DATE),
            'YYYY-MM'
        ) AS SALES_MONTH,
        ROUND(SUM(SALES_AMOUNT), 2) AS MONTHLY_REVENUE
    FROM {TABLE}
    WHERE {FILTER}
    GROUP BY 1
    ORDER BY 1
""")

if not monthly.empty:
    peak = monthly.loc[monthly["MONTHLY_REVENUE"].idxmax()]

    st.success(
        f"Peak month: {peak['SALES_MONTH']} · "
        f"Revenue: {safe_money(peak['MONTHLY_REVENUE'])}"
    )

    monthly_chart = monthly.copy()
    monthly_chart["SALES_MONTH"] = pd.to_datetime(
        monthly_chart["SALES_MONTH"],
        format="%Y-%m"
    )

    st.line_chart(
        monthly_chart.set_index("SALES_MONTH")["MONTHLY_REVENUE"],
        x_label="Month",
        y_label="Revenue (£)",
        height=380,
        width="stretch"
    )

    with st.expander("View monthly revenue data"):
        monthly_display = monthly.rename(columns={
            "SALES_MONTH": "Month",
            "MONTHLY_REVENUE": "Revenue (£)"
        })

        st.dataframe(
            monthly_display,
            width="stretch",
            hide_index=True,
            column_config={
                "Revenue (£)": st.column_config.NumberColumn(
                    "Revenue (£)", format="£%.2f"
                )
            }
        )

    st.download_button(
        "Download monthly revenue CSV",
        data=monthly.to_csv(index=False).encode("utf-8"),
        file_name="monthly_revenue.csv",
        mime="text/csv",
        width="stretch"
    )
else:
    st.info("No monthly revenue data for the selected filters.")


# =========================================================
# PRODUCT PERFORMANCE
# =========================================================
st.divider()
st.header("🏆 Product Performance")

products = load_data(f"""
    SELECT
        STOCKCODE,
        MAX(DESCRIPTION) AS DESCRIPTION,
        SUM(QUANTITY) AS TOTAL_UNITS_SOLD,
        ROUND(SUM(SALES_AMOUNT), 2) AS TOTAL_REVENUE
    FROM {TABLE}
    WHERE {FILTER}
    GROUP BY STOCKCODE
    ORDER BY TOTAL_REVENUE DESC
    LIMIT 10
""")

if not products.empty:
    products["PRODUCT_LABEL"] = (
        products["STOCKCODE"].astype(str)
        + " · "
        + products["DESCRIPTION"]
            .fillna("Unknown product")
            .astype(str)
            .str.slice(0, 28)
    )

    st.bar_chart(
        products.set_index("PRODUCT_LABEL")["TOTAL_REVENUE"],
        x_label="Revenue (£)",
        y_label="Product",
        horizontal=True,
        height=430,
        width="stretch"
    )

    products_display = products.drop(
        columns=["PRODUCT_LABEL"]
    ).rename(columns={
        "STOCKCODE": "Product Code",
        "DESCRIPTION": "Product Description",
        "TOTAL_UNITS_SOLD": "Units Sold",
        "TOTAL_REVENUE": "Revenue (£)"
    })

    st.dataframe(
        products_display,
        width="stretch",
        hide_index=True,
        column_config={
            "Product Code": st.column_config.TextColumn(
                "Product Code"
            ),
            "Product Description": st.column_config.TextColumn(
                "Product Description"
            ),
            "Units Sold": st.column_config.NumberColumn(
                "Units Sold", format="%d"
            ),
            "Revenue (£)": st.column_config.NumberColumn(
                "Revenue (£)", format="£%.2f"
            )
        }
    )

    st.download_button(
        "Download top products CSV",
        data=products_display.to_csv(index=False).encode("utf-8"),
        file_name="top_products.csv",
        mime="text/csv",
        width="stretch"
    )
else:
    st.info("No product data for the selected filters.")


# =========================================================
# COUNTRY PERFORMANCE
# =========================================================
st.divider()
st.header("🌍 Country Performance")

countries = load_data(f"""
    SELECT
        COUNTRY,
        COUNT(DISTINCT INVOICENO) AS TOTAL_INVOICES,
        COUNT(DISTINCT CUSTOMERID) AS UNIQUE_CUSTOMERS,
        ROUND(SUM(SALES_AMOUNT), 2) AS TOTAL_REVENUE
    FROM {TABLE}
    WHERE {FILTER}
    GROUP BY COUNTRY
    ORDER BY TOTAL_REVENUE DESC
    LIMIT 10
""")

if not countries.empty:
    st.bar_chart(
        countries.set_index("COUNTRY")["TOTAL_REVENUE"],
        x_label="Revenue (£)",
        y_label="Country",
        horizontal=True,
        height=430,
        width="stretch"
    )

    countries_display = countries.rename(columns={
        "COUNTRY": "Country",
        "TOTAL_INVOICES": "Invoices",
        "UNIQUE_CUSTOMERS": "Unique Customers",
        "TOTAL_REVENUE": "Revenue (£)"
    })

    st.dataframe(
        countries_display,
        width="stretch",
        hide_index=True,
        column_config={
            "Country": st.column_config.TextColumn("Country"),
            "Invoices": st.column_config.NumberColumn(
                "Invoices", format="%d"
            ),
            "Unique Customers": st.column_config.NumberColumn(
                "Unique Customers", format="%d"
            ),
            "Revenue (£)": st.column_config.NumberColumn(
                "Revenue (£)", format="£%.2f"
            )
        }
    )

    st.download_button(
        "Download country performance CSV",
        data=countries_display.to_csv(index=False).encode("utf-8"),
        file_name="country_performance.csv",
        mime="text/csv",
        width="stretch"
    )
else:
    st.info("No country data for the selected filters.")


# =========================================================
# CUSTOMER SPENDING ANALYSIS
# =========================================================
st.divider()
st.header("👥 Customer Spending Analysis")

st.caption(
    "Customer segments are calculated from spending within the "
    "currently selected date range and country."
)

segments = load_data(f"""
    WITH CUSTOMER_SPENDING AS (
        SELECT
            CUSTOMERID,
            SUM(SALES_AMOUNT) AS TOTAL_SPENDING
        FROM {TABLE}
        WHERE {FILTER}
          AND CUSTOMERID IS NOT NULL
        GROUP BY CUSTOMERID
    )
    SELECT
        CASE
            WHEN TOTAL_SPENDING >= 10000 THEN 'High Spending'
            WHEN TOTAL_SPENDING >= 1000 THEN 'Regular Spending'
            ELSE 'Low Spending'
        END AS CUSTOMER_SEGMENT,
        COUNT(*) AS CUSTOMER_COUNT,
        ROUND(SUM(TOTAL_SPENDING), 2) AS SEGMENT_REVENUE
    FROM CUSTOMER_SPENDING
    GROUP BY 1
""")

segment_order = [
    "High Spending",
    "Regular Spending",
    "Low Spending"
]

if not segments.empty:
    segments["CUSTOMER_SEGMENT"] = pd.Categorical(
        segments["CUSTOMER_SEGMENT"],
        categories=segment_order,
        ordered=True
    )

    segments = segments.sort_values(
        "CUSTOMER_SEGMENT"
    ).copy()

    left, right = st.columns([1, 1])

    with left:
        segment_chart = segments.set_index(
            "CUSTOMER_SEGMENT"
        )["CUSTOMER_COUNT"]

        st.bar_chart(
            segment_chart,
            x_label="Customer Segment",
            y_label="Number of Customers",
            height=350,
            width="stretch"
        )

    with right:
        segments_display = segments.rename(columns={
            "CUSTOMER_SEGMENT": "Customer Segment",
            "CUSTOMER_COUNT": "Customers",
            "SEGMENT_REVENUE": "Revenue (£)"
        })

        st.dataframe(
            segments_display,
            width="stretch",
            hide_index=True,
            column_config={
                "Customer Segment": st.column_config.TextColumn(
                    "Customer Segment"
                ),
                "Customers": st.column_config.NumberColumn(
                    "Customers", format="%d"
                ),
                "Revenue (£)": st.column_config.NumberColumn(
                    "Revenue (£)", format="£%.2f"
                )
            }
        )
else:
    st.info("No identifiable customers for the selected filters.")


# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "Built with Streamlit and Snowflake SQL · "
    "Data source: SALES_PROJECT.PUBLIC.CLEAN_ONLINE_RETAIL"
)