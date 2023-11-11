import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from fund_data import epic_code
from stocknews import StockNews

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
    data2 = data
    data2["% Change"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data)
    annual_return = data2["% Change"].mean() * 252 * 100
    st.write("Average Annual Return is", annual_return, "%")
    stdev = np.std(data2["% Change"]) * np.sqrt(252)
    st.write("Standard deviation is", stdev * 100, "%")
    st.write("Risk Adj. Return", annual_return / (stdev * 100))


with fundametal_data:
    key = epic_code
    fd = FundamentalData(key, output_format="pandas")
    st.subheader("Balance Sheet")
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader("Income Statement")
    income_statement = fd.get_income_statement_annual(ticker)[0]
    ics = income_statement.T[2:]
    ics.columns = list(income_statement.T.iloc[0])
    st.write(ics)
    st.subheader("Cash Flow")
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)

with news:
    st.header(f"News of {ticker}")
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.write(df_news["published"][i])
        st.write(df_news["title"][i])
        st.write(df_news["summary"][i])
        title_sentiment = df_news["sentiment_title"][i]
        st.write(f"Title Sentiment{title_sentiment}")
        news_sentiment = df_news["sentiment_summary"][i]
        st.write(f"News Sentiment{news_sentiment}")
# Great
