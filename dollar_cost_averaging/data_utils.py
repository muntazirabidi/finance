import yfinance as yf
import pandas as pd

def fetch_data(ticker='^GSPC', start_date='2000-01-01', end_date='2023-01-01'):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    print(stock_data)  # Check if data is being fetched
    return stock_data['Adj Close']


def compute_dca(data, frequency, lumpsum):
    num_periods = 1  # default for lumpsum

    if frequency == 'monthly':
        dates = pd.date_range(data.index[0], data.index[-1], freq='MS')
    elif frequency == 'weekly':
        dates = pd.date_range(data.index[0], data.index[-1], freq='W-MON')
    elif frequency == 'biweekly':
        dates = pd.date_range(data.index[0], data.index[-1], freq='2W-MON')
    elif frequency == 'lumpsum':
        dates = [data.index[0]]  # lumpsum will be invested on the first date
    else:
        raise ValueError("Invalid frequency")
    
    num_periods = len(dates)
    amount_per_period = lumpsum / num_periods

    invested = 0
    shares_bought = 0

    for date in dates:
        closest_date = data.index[data.index.get_loc(date, method='nearest')]
        shares_bought += amount_per_period / data[closest_date]
        invested += amount_per_period

    total_value = shares_bought * data.iloc[-1]
    return total_value, invested
