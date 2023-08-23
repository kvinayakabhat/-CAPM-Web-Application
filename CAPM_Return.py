# import libraries

import datetime
import streamlit as streamlit
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import capm_functions
import numpy as np

streamlit.set_page_config(page_title="CAPM",
                   page_icon="chart_with_upwards_trend",
                   layout="wide") #to display the screen full wide

streamlit.title("Stock Capital Asset Pricing Model ") #title of the website

#user input

col1, col2 = streamlit.columns([1,1])    #column wise display
with col1:
    stocks_list = streamlit.multiselect("Choose 4 stocks",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
        #choosing any of the 4 stocks & []==(default stocks) they are stored in stockslist

with col2:
    year = streamlit.number_input("Number of years",1,10)

#download market data for SP500
try:
    end = datetime.date.today() #till this date
    start =datetime.date(datetime.date.today().year-year,datetime.date.today().month, datetime.date.today().day) #from this date
        #2023 minus no. of years selected by user

    SP500 = web.DataReader(['sp500'],'fred',start,end) #will have the sp500 data
            #fred is the data source
    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data =yf.download(stock, period = f'{year}y') #yf= yfinance api
        stocks_df[f'{stock}'] = data['Close']  #printing just the closing data
        
    stocks_df.reset_index(inplace = True)
    SP500.reset_index(inplace = True)
    SP500.columns = ['Date','sp500']
    stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
    stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10])
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df = pd.merge(stocks_df,SP500, on = 'Date', how ='inner')
    #print(stocks_df)

    col1,col2 = streamlit.columns([1,1])
    with col1:
        streamlit.markdown("### DataFrame head")
        streamlit.dataframe(stocks_df.head(), use_container_width =True) #contains the head value
    with col2:
        streamlit.markdown("### DataFrame tail")
        streamlit.dataframe(stocks_df.tail(), use_container_width =True) #contains the tail value


        #creating a chart

    col1,col2 =streamlit.columns([1,1])
    with col1:
        streamlit.markdown("### Price of all the stocks")
        streamlit.plotly_chart(capm_functions.interactive_plot(stocks_df)) #plotting stocks chart

    with col2:
        streamlit.markdown("### Price of all the stocks (After Normalization)")
        streamlit.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))#ploting normalized 

    stocks_daily_return = capm_functions.daily_return(stocks_df)  #daily returns print
    print(stocks_daily_return.head())

    #create 2 dict

    beta ={}
    alpha = {}

    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            b,a =capm_functions.calculate_beta(stocks_daily_return, i)

            beta[i] = b
            alpha[i]=a

    print (beta, alpha)

    beta_df =pd.DataFrame(columns =['Stock','Beta Value'])   #storing
    beta_df['Stock']= beta.keys()
    beta_df['Beta Value'] = [str(round(i,2)) for i in beta.values()]   #calculated values storing

    with col1:
        streamlit.markdown('### Calculated Beta Value')
        streamlit.dataframe(beta_df, use_container_width =True)    #beta value print

    rf = 0
    rm= stocks_daily_return['sp500'].mean()*252

    return_df = pd.DataFrame()    # for return values
    return_value =[]
    for stock, value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)),2))) #market return minus risk free return
    return_df['Stock']= stocks_list

    return_df['Return Value'] = return_value


    with col2:
        streamlit.markdown('### Calculated  Return using CAPM')
        streamlit.dataframe(return_df ,use_container_width = True )

except:
    streamlit.write("Please select valid input")