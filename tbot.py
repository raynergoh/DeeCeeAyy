from datetime import datetime
from config import ALPACA_CONFIG
from last_year import get_last_year
import csv

from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader




class DCA(Strategy):
    parameters = {
        "multiplier": 300,
        "DCA_amount": 500,
    }

    def initialize(self):
        # Will make on_trading_iteration() run every 30Days
        self.sleeptime = "31D"

    def on_trading_iteration(self):
        currentDateTime = str(self.get_datetime())
        currentDate = currentDateTime[:10]
        # Date is in the format of YYYY-MM-DD
        firstDayOfMonth = currentDate[:8] + '01'
        dateLastYear = get_last_year(firstDayOfMonth)

        reader_obj = csv.DictReader(open("sp500_PE.csv"))
        currentPE = None
        for row in reader_obj:
            if row['date'] == firstDayOfMonth:
                currentPE = row['value']
            if row['date'] == dateLastYear:
                lastYearPE = row['value']

        symbol = "SPY"
        currentPrice = self.get_last_price(symbol)
        # Get the data for SPY for the last 365 days
        bars =  self.get_historical_prices("SPY", 365, "day")
        # To get the DataFrame of SPY data
        df = bars.df
        first_ohlc = df.iloc[1] # Get the first row of the DataFrame (1 year ago)
        lastYearPrice = first_ohlc['close']

        changeInPrice = (float(currentPrice) - float(lastYearPrice)) / float(lastYearPrice)
        changeInPE = (float(currentPE) - float(lastYearPE)) / float(lastYearPE)
        score = changeInPrice - changeInPE

        multiplier = self.parameters["multiplier"]
        DCA_amount = self.parameters["DCA_amount"]
        amountToInvest = DCA_amount - score * multiplier
        orderQty = amountToInvest / currentPrice
        order = self.create_order(symbol, orderQty,"buy")
        self.submit_order(order)

if __name__ == "__main__":
    live = False

    trader = Trader()
    broker = Alpaca(ALPACA_CONFIG)
    strategy = DCA(broker=broker)

    if not live:
        # Backtest this strategy
        backtesting_start = datetime(1998, 1, 1)
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