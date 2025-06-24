from datetime import datetime, timedelta
from config import ALPACA_CONFIG
from last_year import get_last_year
from scalar import to_scalar
from previous_trading_day import get_previous_trading_day
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
        "DCA_amount": 500
    }

    def initialize(self):
        # Will make on_trading_iteration() run every 30Days
        self.sleeptime = "1M"
        self.symbol = "SPY"
        self.multiplier = self.parameters["multiplier"]
        self.DCA_amount = self.parameters["DCA_amount"]

    def fetch_pe_ratio(self, date):
        """
        Fetches the SPY PE ratio for a given date using yfinance.
        Note: yfinance does not provide historical PE ratios, only the current one.
        Args:
            date (str): Date in 'YYYY-MM-DD' format.
        Returns:
            float: PE ratio if available, else None.
        """
        try:
            spy = yf.Ticker(self.symbol)
            pe_ratio = spy.info.get("trailingPE", None)
            if pe_ratio is None:
                logging.warning(f"PE ratio not available for {date}.")
            return pe_ratio
        except Exception as e:
            logging.error(f"Error fetching PE ratio for {date}: {e}")
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
            trading_date = get_previous_trading_day(currentDate)

            # Only proceed if this is the first trading day of the month
            if not self.is_first_trading_day_of_month(trading_date):
                logging.info(f"{trading_date} is not the first trading day of the month. Skipping iteration.")
                return
            
            firstDayOfMonth = trading_date[:8] + '01'
            dateLastYear = get_last_year(firstDayOfMonth)

            # Fetch current and last year's PE ratios dynamically
            currentPE = self.fetch_pe_ratio(firstDayOfMonth)
            lastYearPE = self.fetch_pe_ratio(dateLastYear)

            if currentPE is None or lastYearPE is None:
                logging.warning("Missing PE data. Skipping this iteration.")
                return

            # Get the data for SPY for the last 365 days
            # Fetch historical prices (ensure enough lookback for 1 year ago)
            bars = self.get_historical_prices(self.symbol, 366, "day")
            df = bars.df

            # Check for empty DataFrame
            if df.empty:
                logging.warning("No historical price data available. Skipping this iteration.")
                return

            # Get last available price for trading_date
            if trading_date in df.index:
                currentPrice = df.loc[trading_date]['close']
            elif not df.empty:
                # fallback: get last available close if DataFrame is not empty
                currentPrice = df['close'].iloc[-1]
            else:
                logging.warning("No current price data. Skipping this iteration.")
                return

            # Get price 1 year ago (find the row closest to trading_date minus 1 year)
            one_year_ago = (datetime.strptime(trading_date, "%Y-%m-%d") - timedelta(days=365)).strftime("%Y-%m-%d")
            one_year_ago_trading = get_previous_trading_day(one_year_ago)
            if one_year_ago_trading in df.index:
                lastYearPrice = df.loc[one_year_ago_trading]['close']
            elif not df.empty:
                # fallback to earliest available
                lastYearPrice = df['close'].iloc[0]
            else:
                logging.warning("No last year price data. Skipping this iteration.")
                return

            cp = to_scalar(currentPrice)
            lyp = to_scalar(lastYearPrice)
            changeInPrice = (cp - lyp) / lyp
            changeInPE = (float(currentPE) - float(lastYearPE)) / float(lastYearPE)            
            valuation_delta = changeInPrice - changeInPE

            amountToInvest = self.DCA_amount - valuation_delta * self.multiplier
            orderQty = amountToInvest / cp

            order = self.create_order(self.symbol, orderQty, "buy")
            self.submit_order(order)

            logging.info(f"Order submitted: {orderQty} shares at {currentPrice} (score: {score:.4f})")

        except Exception as e:
            logging.error(f"Error in trading iteration: {e}")

if __name__ == "__main__":
    live = False
    trader = Trader()
    broker = Alpaca(ALPACA_CONFIG)
    strategy = DCA(broker=broker)

    if not live:
        # Backtest this strategy
        backtesting_start = datetime(2015, 1, 1)
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
