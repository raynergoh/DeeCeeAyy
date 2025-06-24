import pandas as pd

def get_previous_trading_day(date_str):
    date = pd.to_datetime(date_str)
    # If it's a business day, return as is; otherwise, get previous business day
    if pd.Timestamp(date).isoweekday() in range(1,6):
        return date.strftime('%Y-%m-%d')
    else:
        previous_trading_day = date - pd.tseries.offsets.BDay(1)
        return previous_trading_day.strftime('%Y-%m-%d')
