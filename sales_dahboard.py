import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Load data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.title("📊 Sales Dashboard")

    # Sidebar filters
    st.sidebar.header("Filter Data")
    region = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())
    product = st.sidebar.multiselect("Select Product", options=df["Product"].unique(), default=df["Product"].unique())

    filtered_df = df[(df["Region"].isin(region)) & (df["Product"].isin(product))]

    # KPIs
    total_sales = filtered_df["Sales"].sum()
    total_units = filtered_df["Units Sold"].sum()
    avg_price = round(filtered_df["Sales"].sum() / filtered_df["Units Sold"].sum(), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Units Sold", f"{total_units:,}")
    col3.metric("Average Price", f"${avg_price}")

    # Charts
    fig_sales_by_region = px.bar(
        filtered_df.groupby("Region").sum(numeric_only=True).reset_index(),
        x="Region", y="Sales", title="Sales by Region"
    )
    fig_sales_by_product = px.pie(
        filtered_df, names="Product", values="Sales", title="Sales Distribution by Product"
    )

    st.plotly_chart(fig_sales_by_region, use_container_width=True)
    st.plotly_chart(fig_sales_by_product, use_container_width=True)

    st.markdown("### Data Preview")
    st.dataframe(filtered_df.head(10))
else:
    st.info("Please upload a CSV file to start.")
