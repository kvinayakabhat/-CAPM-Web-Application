# import libraries

import datetime
import streamlit as streamlit
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime

streamlit.set_page_config(page_title="CAPM",
                   page_icon="chart_with_upwards_trend",
                   layout="wide") #to display the screen full wide

streamlit.title("Capital Asset Pricing Model") #title of the website

#user input

col1, col2 = streamlit.columns([1,1])    #column wise display
with col1:
    stocks_list = streamlit.multiselect("Choose 4 stocks",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
        #choosing any of the 4 stocks & []==(default stocks) they are stored in stockslist

with col2:
    year = streamlit.number_input("Number of years",1,10)

#download market data for SP500

end = datetime.date.today()
start =datetime.date(datetime.date.today().year-year,datetime.date.today().month, datetime.date.today().day) 
    #2023 minus no. of years selected by user
SP500 = web.DataReader(['sp500'],'fred',start,end)
print(SP500.tail())

for stock in stocks_list:
    data =yf.download(stock, period = f'{year}y')
    print(data.head())