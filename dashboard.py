import os
from dotenv import load_dotenv
import streamlit as st
import mysql.connector
import plotly.express as px

load_dotenv()

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# MYSQL CONNECTION
# --------------------------------------------------

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE", "ecommerce_dw")
)

cursor = connection.cursor()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🛒 E-Commerce Sales Analytics Dashboard")
st.write("Sales analytics from the MySQL Data Warehouse")

# --------------------------------------------------
# KPI QUERIES
# --------------------------------------------------

cursor.execute("""
    SELECT
        COUNT(*) AS total_sales,
        SUM(revenue) AS total_revenue
    FROM fact_sales
""")

sales_result = cursor.fetchone()

total_sales = sales_result[0]
total_revenue = sales_result[1]

cursor.execute("""
    SELECT COUNT(*)
    FROM dim_customer
""")

total_customers = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*)
    FROM dim_product
""")

total_products = cursor.fetchone()[0]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"{total_sales:,}"
    )

with col2:
    st.metric(
        "Total Revenue",
        f"{total_revenue:,.2f}"
    )

with col3:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "Products",
        f"{total_products:,}"
    )

st.divider()

# --------------------------------------------------
# MONTHLY REVENUE
# --------------------------------------------------

st.subheader("📈 Monthly Revenue")

cursor.execute("""
    SELECT
        CONCAT(year, '-', LPAD(month, 2, '0')) AS month,
        total_revenue
    FROM monthly_revenue
    ORDER BY year, month
""")

monthly_data = cursor.fetchall()

monthly_chart = {
    "Month": [row[0] for row in monthly_data],
    "Revenue": [float(row[1]) for row in monthly_data]
}

fig_monthly = px.line(
    monthly_chart,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

st.subheader("🏆 Top 10 Products by Revenue")

cursor.execute("""
    SELECT
        p.description,
        SUM(f.revenue) AS revenue
    FROM fact_sales f
    JOIN dim_product p
        ON f.stock_code = p.stock_code
    GROUP BY
        p.stock_code,
        p.description
    ORDER BY revenue DESC
    LIMIT 10
""")

product_data = cursor.fetchall()

product_chart = {
    "Product": [
        str(row[0])[:30] for row in product_data
    ],
    "Revenue": [
        float(row[1]) for row in product_data
    ]
}

fig_products = px.bar(
    product_chart,
    x="Revenue",
    y="Product",
    orientation="h",
    title="Top 10 Products by Revenue"
)

fig_products.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)
# --------------------------------------------------
# REVENUE BY COUNTRY
# --------------------------------------------------

st.subheader("🌍 Revenue by Country")

cursor.execute("""
    SELECT
        c.country,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_customer c
        ON f.customer_id = c.customer_id
    GROUP BY c.country
    ORDER BY total_revenue DESC
    LIMIT 10
""")

country_data = cursor.fetchall()

country_chart = {
    "Country": [row[0] for row in country_data],
    "Revenue": [float(row[1]) for row in country_data]
}

fig_country = px.bar(
    country_chart,
    x="Country",
    y="Revenue",
    title="Top 10 Countries by Revenue"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

# --------------------------------------------------
# CLOSE DATABASE CONNECTION
# --------------------------------------------------

cursor.close()
connection.close()