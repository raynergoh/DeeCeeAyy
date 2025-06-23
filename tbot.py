from datetime import datetime, timedelta
from config import ALPACA_CONFIG
from last_year import get_last_year
import logging

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
        self.sleeptime = "31D"
        self.symbol = "SPY"
        self.multiplier = self.parameters["multiplier"]
        self.DCA_amount = self.parameters["DCA_amount"]

    def fetch_pe_ratio(self, date):
        """
        Fetches the SPY PE ratio for a given date using yfinance.
        Args:
            date (str): Date in 'YYYY-MM-DD' format.
        Returns:
            float: PE ratio if available, else None.
        """
        try:
            spy = yf.Ticker(self.symbol)
            hist = spy.history(start=date, end=date)
            pe_ratio = spy.info.get("trailingPE", None)
            if pe_ratio is None:
                logging.warning(f"PE ratio not available for {date}.")
            return pe_ratio
        except Exception as e:
            logging.error(f"Error fetching PE ratio for {date}: {e}")
            return None

    def on_trading_iteration(self):
        try:
            currentDateTime = str(self.get_datetime())
            currentDate = currentDateTime[:10]
            firstDayOfMonth = currentDate[:8] + '01'
            dateLastYear = get_last_year(firstDayOfMonth)

            # Fetch current and last year's PE ratios dynamically
            currentPE = self.fetch_pe_ratio(firstDayOfMonth)
            lastYearPE = self.fetch_pe_ratio(dateLastYear)

            if currentPE is None or lastYearPE is None:
                logging.warning("Missing PE data. Skipping this iteration.")
                return

            currentPrice = self.get_last_price(self.symbol)
            # Get the data for SPY for the last 365 days
            bars = self.get_historical_prices(self.symbol, 365, "day")
            df = bars.df
            first_ohlc = df.iloc[1]  # 1 year ago
            lastYearPrice = first_ohlc['close']

            changeInPrice = (float(currentPrice) - float(lastYearPrice)) / float(lastYearPrice)
            changeInPE = (float(currentPE) - float(lastYearPE)) / float(lastYearPE)
            score = changeInPrice - changeInPE

            amountToInvest = self.DCA_amount - score * self.multiplier
            orderQty = amountToInvest / currentPrice

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
        backtesting_start = datetime(1998, 1, 1)
        backtesting_end = datetime(2015, 12, 31)
        strategy.run_backtest(
            YahooDataBacktesting,
            backtesting_start,
            backtesting_end,
        )
    else:
        # Run the strategy live
        trader.add_strategy(strategy)
        trader.run_all()
