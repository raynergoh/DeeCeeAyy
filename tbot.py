from datetime import datetime, timedelta

from config import ALPACA_CONFIG
from last_year import get_last_year
from scalar import to_scalar
from previous_trading_day import get_previous_trading_day
from multpl import fetch_multpl_pe_table

import logging
import pandas as pd
import yfinance as yf

from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader

# Setup logging for better error tracking and debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tbot.log"),
        logging.StreamHandler()
    ]
)

class DCA(Strategy):
    parameters = {
        "multiplier": 300,
        "DCA_amount": 500,
        "min_investment_pct": 0.7
    }

    def initialize(self):
        # Will make on_trading_iteration() run everyday
        # However, if it is not the first trading day of the month, it will skip the iteration
        self.sleeptime = "1D"
        self.symbol = "SPY"
        self.multiplier = self.parameters["multiplier"]
        self.DCA_amount = self.parameters["DCA_amount"]
        self.min_investment_pct = self.parameters["min_investment_pct"]
        
        # Fetch PE ratio history from Multpl.com (separate DataFrame)
        self.pe_table = fetch_multpl_pe_table()
        if self.pe_table is not None:
            logging.info(f"PE ratio table loaded with {len(self.pe_table)} rows.")
        else:
            logging.warning("PE ratio table not available.")

        # 2. Fetch SPY price history for the same date range
        self.price_history = yf.download(
            self.symbol,
            start="2000-01-01",
            end="2025-01-01",
            auto_adjust=True,
            progress=False
        )
        self.price_history.index = pd.to_datetime(self.price_history.index)
        logging.info(f"SPY price history loaded with {len(self.price_history)} rows.")

    def get_pe(self, date_str):
        if self.pe_table is not None:
            date = pd.to_datetime(date_str)
            if date in self.pe_table.index:
                return self.pe_table.loc[date, 'PE_Ratio']
            # Fallback: get last available PE before date
            prev_dates = self.pe_table.index[self.pe_table.index <= date]
            if len(prev_dates) > 0:
                return self.pe_table.loc[prev_dates[-1], 'PE_Ratio']
        return None

    def get_price(self, date_str):
        if self.price_history is not None:
            date = pd.to_datetime(date_str)
            if date in self.price_history.index:
                return self.price_history.loc[date, 'Close']
            # Fallback: get last available price before date
            prev_dates = self.price_history.index[self.price_history.index <= date]
            if len(prev_dates) > 0:
                return self.price_history.loc[prev_dates[-1], 'Close']
        return None
    
    def is_first_trading_day_of_month(self, date_str):
        """Return True if the given date is the first trading day of its month."""
        date = pd.to_datetime(date_str)
        # Generate all business days for the month
        month_start = date.replace(day=1)
        month_end = (month_start + pd.offsets.MonthEnd(0))
        business_days = pd.bdate_range(start=month_start, end=month_end)
        if len(business_days) == 0:
            return False
        return date == business_days[0]

    def on_trading_iteration(self):
        try:
            currentDateTime = str(self.get_datetime())
            currentDate = currentDateTime[:10]
            trading_date = currentDate
            logging.info(f"Running iteration for trading_date: {trading_date}")

            # Only proceed if this is the first trading day of the month
            if not self.is_first_trading_day_of_month(trading_date):
                logging.info(f"{trading_date} is not the first trading day of the month. Skipping iteration.")
                return
            
            firstDayOfMonth = trading_date[:8] + '01'
            dateLastYear = get_last_year(firstDayOfMonth)

            # Try to fetch current and last year's PE ratios and price 
            currentPE = self.get_pe(firstDayOfMonth)
            lastYearPE = self.get_pe(dateLastYear)
            currentPrice = self.get_price(trading_date)
            # Get price 1 year ago
            one_year_ago = (pd.to_datetime(trading_date) - timedelta(days=365)).strftime('%Y-%m-%d')
            lastYearPrice = self.get_price(one_year_ago)

            # If any data is missing, do default DCA
            if (currentPE is None or lastYearPE is None or
                currentPrice is None or lastYearPrice is None):
                if currentPrice is not None:
                    cp = to_scalar(currentPrice)
                    orderQty = self.DCA_amount / cp
                    order = self.create_order(self.symbol, orderQty, "buy")
                    self.submit_order(order)
                    logging.info(f"Default DCA order submitted: {orderQty} shares at {cp} (missing data)")
                else:
                    logging.warning("No price available even for default DCA. Skipping order this iteration.")
                return

            # Normal DCA logic
            cp = to_scalar(currentPrice)
            lyp = to_scalar(lastYearPrice)
            changeInPrice = (cp - lyp) / lyp
            changeInPE = (float(currentPE) - float(lastYearPE)) / float(lastYearPE)            
            valuation_delta = changeInPrice - changeInPE

            min_investment = self.min_investment_pct * self.DCA_amount 
            amountToInvest = self.DCA_amount - valuation_delta * self.multiplier
            # Cap the minimum investment
            amountToInvest = max(amountToInvest, min_investment)
            orderQty = amountToInvest / cp

            order = self.create_order(self.symbol, orderQty, "buy")
            self.submit_order(order)

            logging.info(f"Order submitted: {orderQty} shares at {currentPrice} (valuation_delta: {valuation_delta:.4f})")

        except Exception as e:
            logging.error(f"Error in trading iteration: {e}")

if __name__ == "__main__":
    live = False
    trader = Trader()
    broker = Alpaca(ALPACA_CONFIG)
    strategy = DCA(broker=broker)

    if not live:
        # Backtest this strategy
        backtesting_start = datetime(2005, 1, 1)
        backtesting_end = datetime(2015, 12, 31)
        strategy.backtest(
            YahooDataBacktesting,
            backtesting_start,
            backtesting_end,
        )
    else:
        # Run the strategy live
        trader.add_strategy(strategy)
        trader.run_all()
