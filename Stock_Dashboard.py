import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.title("Stock Dashboard")
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

data = yf.download(ticker, start=start_date, end=end_date)
fig = px.line(data, x=data.index, y=data["Adj Close"], title=ticker)
st.plotly_chart(fig)

pricing_data, fundametal_data, news = st.tabs(
    ["Pricing Data", "Fundamental Data", "Top 10 News"]
)

with pricing_data:
    st.header("Price Movements")
    st.write(data)

with fundametal_data:
    st.write("Fundamental")

with news:
    st.write("News")
