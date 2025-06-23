# 📈 DCA Valuation-Aware Trading Bot

A Python trading bot that dynamically adjusts dollar-cost-averaging (DCA) investments in the S&P 500 (SPY) based on market valuation, using the difference between the S&P 500 index price and its PE ratio as a relative value indicator.

---

## 🔧 Features

- **Valuation-Aware DCA**: Allocates more capital when the market is "cheap" (by PE ratio), and less when "expensive".
- **Automated Data Fetching**: Dynamically retrieves up-to-date S&P 500 PE ratios and prices.
- **Backtesting Support**: Evaluate strategy performance on historical data.
- **Live Trading Capability**: Integrates with Alpaca for real or paper trading.
- **Configurable Parameters**: Easily adjust DCA amount and valuation sensitivity.
- **Secure Credentials**: API keys are managed via environment variables or a `.env` file.
- **Robust Logging**: All trades and errors are logged for transparency.

---

## ⚙️ How It Works

1. **Fetches PE Data**  
   Gets current and year-ago S&P 500 PE ratios using dynamic data sources (e.g., Yahoo Finance via `yfinance`).

2. **Calculates Relative Expensiveness**  
   Compares the year-over-year (YoY) change in index price to the YoY change in PE ratio.

3. **Adjusts Investment Amount**  
   - If the market is relatively cheap (price growth < PE growth), increases DCA.
   - If expensive, decreases DCA.

4. **Executes Trades Automatically**  
   Places buy orders for SPY via the Alpaca API at monthly intervals.

---
