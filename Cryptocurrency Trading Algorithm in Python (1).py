#!/usr/bin/env python
# coding: utf-8

# In[1]:


# First, we'll need a way to retrieve the cryptocurrency market data we need. 
# Yahoo Finance is a popular website and service that provides up-to-date financial news and market quotes. 
# Luckily, there is a Python library called yfinance that allows you to easily access and save this data.
# Let's go ahead and install it.




get_ipython().system('pip install yfinance')


# In[1]:


# Now let's import the libraries we're going to use.

import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter


# In[37]:


# Retrieve two weeks of Bitcoin to USD exchange rates with a 1 hour interval and save the dataframe to a variable.
BTC_USD = yf.download("BTC-USD", start='2022-01-01', end='2024-12-31', interval='1d')


# In[ ]:


# The yfinance library has a built-in method for retrieving historical market data.
# Let's use this to get the exchange rate of Bitcoin to US Dollars over the year of 2020.
# We use the download() method, passing in the ticker we're interested in ("BTC-USD"), 
# the start and end dates, and the time interval between datapoints. Let's use a 1 day interval.

# Now we have a dataframe assigned to the variable BTC_USD storing the historical BTC-USD exchange over 2020. 
# To get a sense for the data we have, try calling the head() method from the pandas library on the dataframe.


# In[38]:


BTC_USD.head()


# In[ ]:


# As you can see, the dataframe has 7 columns. The first column gives the date, 
# the second column gives the opening price of Bitcoin in USD for the day, 
#followed by the day's price high and low, 
#then the day's closing and adjusted closing prices, and finally, the trading volume.


# In[ ]:


# A great way to get a feel for the data you're working with is to create a basic plot to visualize it. 
# Price charts are an essential tool for understanding and analyzing a given stock or currency. 
# They are a time series showing an asset's price over time. 
# The most basic type of price chart is the line chart, so let's go ahead and make one of those.

# In a line chart, we connect the adjusted closing price of the asset at the end of each day with a continuous line.
# We can use the matploitlib library to easily create our price chart. Let's do it!


# In[39]:


fig, ax = plt.subplots(dpi=500)

# Formatting the date axis
date_format = DateFormatter("%h-%d-%y")
ax.xaxis.set_major_formatter(date_format)
ax.tick_params(axis='x', labelsize=8)
fig.autofmt_xdate()

# Plotting the closing price against the date (1 day interval)
ax.plot(BTC_USD['Close'], lw=0.75)

# Adding labels and title to the plot
ax.set_ylabel('Price of Bitcoin (USD)')
ax.set_title('Bitcoin to USD Exchange Rate')
ax.grid() # adding a grid

# Displaying the price chart
plt.show()


# In[ ]:


# Looks great! We can see how the exchange range of BTC to USD has changed over the course of 2020.
# Just with a first glance we see that there's a steep upward trend in Bitcoin price starting around October. 
# However, due to the somewhat random nature of short term price movements, the line chart fluctuates and looks noisy.

# To help reveal longer term trends and smooth out short term fluctuations,
# a common method is to calculate and study Moving Averages.


# In[40]:


# Compute a 9-day Simple Moving Average with pandas
BTC_USD['SMA_9'] = BTC_USD['Close'].rolling(window=9, min_periods=1).mean()


# In[41]:


BTC_USD['SMA_30'] = BTC_USD['Close'].rolling(window=30, min_periods=1).mean()


# In[42]:


# Display the last 5 entries of the dataframe
BTC_USD.tail()


# In[43]:


# Plot the Simple Moving Averages

fig, ax = plt.subplots(dpi=500)

# Formatting the date axis
date_format = DateFormatter("%h-%d-%y")
ax.xaxis.set_major_formatter(date_format)
ax.tick_params(axis='x', labelsize=8)
fig.autofmt_xdate()

# Plotting the closing price against the date (1 day interval)
ax.plot(BTC_USD['Close'], lw=0.75, label='Closing Price') # Added label

"""
You have already seen the code above earlier - we are simply reusing it.
Below we plot the 9 and 30 day Simple Moving Averages and give them the appropriate label
"""
ax.plot(BTC_USD['SMA_9'], lw=0.75, alpha=0.75, label='9 Day SMA')
ax.plot(BTC_USD['SMA_30'], lw=0.75, alpha=0.75, label='30 Day SMA')


# Adding labels and title to the plot
ax.set_ylabel('Price of Bitcoin (USD)')
ax.set_title('Bitcoin to USD Exchange Rate')
ax.grid() # adding a grid
ax.legend() # adding a legend

# Displaying the price chart
plt.show()


# In[ ]:


# From the plot you can see that the Simple Moving Averages had a smoothing effect on the line chart -
# much of the short term Bitcoin price fluctuations were smoothed out and the moving averages appear 
# to reveal some longer term trends.
# As expected, the 30 day interval had a more significant smoothing effect than the 9 day interval.


# In[44]:


# Create a pandas dataframe that is the same size as the BTC_USD dataframe and covers the same dates
trade_signals = pd.DataFrame(index=BTC_USD.index)

# Define the intervals for the Fast and Slow Simple Moving Averages (in days)
short_interval = 10
long_interval = 40

# Compute the Simple Moving Averages and add it to the dateframe as new columns
trade_signals['Short'] = BTC_USD['Close'].rolling(window=short_interval, min_periods=1).mean()
trade_signals['Long'] = BTC_USD['Close'].rolling(window=long_interval, min_periods=1).mean()


# In[45]:


# Create a new column populated with zeros
trade_signals['Signal'] = 0.0

# Wherever the Shorter term SMA is above the Longer term SMA, set the Signal column to 1, otherwise 0
trade_signals['Signal'] = np.where(trade_signals['Short'] > trade_signals['Long'], 1.0, 0.0)   


# In[46]:


trade_signals['Position'] = trade_signals['Signal'].diff()


# In[47]:


fig, ax = plt.subplots(dpi=500)

# Formatting the date axis
date_format = DateFormatter("%h-%d-%y")
ax.xaxis.set_major_formatter(date_format)
ax.tick_params(axis='x', labelsize=8)
fig.autofmt_xdate()


# Plotting the Bitcoin closing price against the date (1 day interval)
ax.plot(BTC_USD['Close'], lw=0.75, label='Closing Price')

# Plot the shorter-term moving average
ax.plot(trade_signals['Short'], lw=0.75, alpha=0.75, color='orange', label='Short-term SMA')

# Plot the longer-term moving average
ax.plot(trade_signals['Long'], lw=0.75, alpha=0.75, color='purple', label='Long-term SMA')


# Adding green arrows to indicate buy orders
ax.plot(trade_signals.loc[trade_signals['Position']==1.0].index, trade_signals.Short[trade_signals['Position'] == 1.0],
 marker=6, ms=4, linestyle='none', color='green')

 # Adding red arrows to indicate sell orders
ax.plot(trade_signals.loc[trade_signals['Position'] == -1.0].index, trade_signals.Short[trade_signals['Position'] == -1.0],
 marker=7, ms=4, linestyle='none', color='red')


# Adding labels and title to the plot
ax.set_ylabel('Price of Bitcoin (USD)')
ax.set_title('Bitcoin to USD Exchange Rate')
ax.grid() # adding a grid
ax.legend() # adding a legend

# Displaying the price chart
plt.show()


# In[48]:


# Backtest your Algorithm
# Define how much money you will start with (in USD)
initial_balance = 10000.0 # ten thousand USD

# Create dataframe containing all the dates considered
backtest = pd.DataFrame(index=trade_signals.index)

# Add column containing the daily percent returns of Bitcoin
backtest['BTC_Return'] = BTC_USD['Close'] / BTC_USD['Close'].shift(1) # Current closing price / yesterday's closing price


# In[ ]:


# Now to compute the daily returns of the trading algorithm, let's assume that at any given point, 
# our portfolio is either all in on Bitcoin or is entirely holding USD. 
# This means that whenever the algorithm is currently holding Bitcoin, 
# it's daily returns are the same as the daily returns of Bitcoin.
# On the other hand, when the algorithm is holding USD, its returns are entirely detached from Bitcoin price movements.
# Thus when holding USD, the value of the portfolio remains constant during that period. 
# We will also make the simplifying assumption that we are able to perform zero comission trades.
# This reasoning is condensed into the following two lines of code


# In[50]:



# Add column containing the daily percent returns of the Moving Average Crossover strategy
backtest['Alg_Return'] = np.where(trade_signals.Signal == 1, backtest.BTC_Return, 1.0)

# Add column containing the daily value of the portfolio using the Crossover strategy
backtest['Balance'] = initial_balance * backtest.Alg_Return.cumprod() # cumulative product


# In[ ]:


# Let's make a plot comparing the performance of trading algorithm we implemented and a simple "Buy and Hold" strategy
# which will serve as a baseline. Plot the value of the portfolio using either strategy over the course of 2020.


# In[51]:


fig, ax = plt.subplots(dpi=500)

# Formatting the date axis
date_format = DateFormatter("%h-%d-%y")
ax.xaxis.set_major_formatter(date_format)
ax.tick_params(axis='x', labelsize=8)
fig.autofmt_xdate()

# Plotting the value of Buy and Hold Strategy
ax.plot(initial_balance*backtest.BTC_Return.cumprod(), lw=0.75, alpha=0.75, label='Buy and Hold')

# Plotting total value of Crossing Averages Strategy
ax.plot(backtest['Balance'], lw=0.75, alpha=0.75, label='Crossing Averages')

# Adding labels and title to the plot
ax.set_ylabel('USD')
ax.set_title('Value of Portfolio')
ax.grid() # adding a grid
ax.legend() # adding a legend

# Displaying the price chart
plt.show()


# In[ ]:


# From the plot you can see that both strategies produced in an enormous return on investment,
# more than quadrupling the value of our portfolio. 
# Obviously this was due to the meteoric rise of Bitcoin prices near the end of the year and you should certainly not 
# consistently expect similar returns in the future.

# However, it's reassuring to see that the trading algorithm at least appears to be feasible, 
# even slightly out performing the baseline Buy and Hold strategy. 
# In the plot you can clearly see the periods in which the algorithm was all in on Bitcoin and the periods where it was 
# holding USD. 
# In the former periods, the growth of the portfolio mirrored the growth of Bitcoin. 
# In the latter period, mostly where Bitcoin was trending downwards, the portfolio remained constant in value and was not 
# brought down by falling Bitcoin prices.


# In[ ]:





# In[ ]:




