# inter_sales_dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns


# setting streamlit page layout
st.set_page_config(page_title="Sales Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide")


@st.cache # use the decorator to store the loaded dataset
def get_data_from_excel():
    # read excel file and convert to dataframe
    df = pd.read_excel('supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000
        )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df['Time'], format="%H:%M:%S").dt.hour
    return df
df = get_data_from_excel()


# ------ SIDEBAR ------
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique() # to select all unique cities upon starting the app
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique() # to select all unique customer upon starting the app
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique() # to select all unique gender upon starting the app
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


# ------ MAINPAGE ------
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


# TOP KPIs
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)


# creating 3 KPI column
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales:,}")
    # st.subheader("US $" "%.2f" %total_sales) # alternate way to input the value
with middle_column:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction")
    st.subheader(f"US $ {average_sale_by_transaction}")

    
st.markdown("---")
st.dataframe(df_selection)


#  SALES BY PRODUCT LINE (bar chart) 
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
# create a bar chart
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white"
)
# update the bar chart layout
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# show chart
# st.plotly_chart(fig_product_sales)


#  SALES BY HOUR (bar chart) 
sales_by_bour = (
    df_selection.groupby(by=["hour"]).sum()[["Total"]]
)
# create a bar chart
fig_hourly_sales = px.bar(
    sales_by_bour,
    x=sales_by_bour.index,
    y="Total",
    title="<b>Sales Per Hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_bour),
    template="plotly_white"
)
# update the bar chart layout
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)
# show chart
# st.plotly_chart(fig_hourly_sales)


# creating chart column
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_hourly_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
 


