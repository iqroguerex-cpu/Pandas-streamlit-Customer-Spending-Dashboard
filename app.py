import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Customer Spending Dashboard", layout="wide")

st.title("📊 Advanced Customer Spending Dashboard")

file = st.file_uploader("Upload customers.csv", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()

    numeric_cols = ["age", "purchases", "avg_order_value"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Feature Engineering
    df["total_spent"] = df["purchases"] * df["avg_order_value"]

    conditions = [
        df["age"].between(18, 30),
        df["age"].between(31, 45),
        df["age"] >= 46
    ]
    labels = ["Young", "Mid", "Senior"]
    df["age_category"] = np.select(conditions, labels, default="Other")

    # Sidebar Filters
    st.sidebar.header("Filters")
    selected_city = st.sidebar.multiselect(
        "Select City",
        options=df["city"].unique(),
        default=df["city"].unique()
    )

    selected_gender = st.sidebar.multiselect(
        "Select Gender",
        options=df["gender"].unique(),
        default=df["gender"].unique()
    )

    df = df[(df["city"].isin(selected_city)) &
            (df["gender"].isin(selected_gender))]

    # KPIs
    st.subheader("📌 Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"${df['total_spent'].sum():,.0f}")
    col2.metric("Average Spending", f"${df['total_spent'].mean():,.0f}")
    col3.metric("Top Customer ID",
                df.loc[df["total_spent"].idxmax(), "customer_id"])

    st.divider()

    # 1️⃣ Bar Chart - Avg Spending per City
    city_avg = df.groupby("city")["total_spent"].mean().reset_index()
    fig1 = px.bar(city_avg,
                  x="city",
                  y="total_spent",
                  title="Average Spending per City",
                  color="city")
    st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Pie Chart - Spending by Gender
    gender_total = df.groupby("gender")["total_spent"].sum().reset_index()
    fig2 = px.pie(gender_total,
                  names="gender",
                  values="total_spent",
                  title="Total Spending by Gender")
    st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Histogram - Spending Distribution
    fig3 = px.histogram(df,
                        x="total_spent",
                        nbins=10,
                        title="Distribution of Customer Spending")
    st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Box Plot - Spending by City
    fig4 = px.box(df,
                  x="city",
                  y="total_spent",
                  title="Spending Spread by City",
                  color="city")
    st.plotly_chart(fig4, use_container_width=True)

    # 5️⃣ Scatter Plot - Age vs Spending
    fig5 = px.scatter(df,
                      x="age",
                      y="total_spent",
                      color="age_category",
                      size="purchases",
                      title="Age vs Spending (Bubble Size = Purchases)")
    st.plotly_chart(fig5, use_container_width=True)

    # 6️⃣ Top 5 Customers
    top5 = df.sort_values("total_spent", ascending=False).head(5)
    fig6 = px.bar(top5,
                  x="customer_id",
                  y="total_spent",
                  title="Top 5 Customers by Spending",
                  color="customer_id")
    st.plotly_chart(fig6, use_container_width=True)

    # 7️⃣ Spending by Age Category
    age_spend = df.groupby("age_category")["total_spent"].sum().reset_index()
    fig7 = px.bar(age_spend,
                  x="age_category",
                  y="total_spent",
                  title="Spending by Age Category",
                  color="age_category")
    st.plotly_chart(fig7, use_container_width=True)

else:
    st.info("Please upload customers.csv to begin.")
