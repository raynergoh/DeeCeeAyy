# DCA Valuation-Aware Trading Bot

A Python trading bot that dynamically adjusts dollar-cost-averaging (DCA) investments in the S&P 500 based on market valuation, using the difference between the S&P 500 index price and its PE ratio as a relative value indicator.

## Features

- **Valuation-Aware DCA**: Invests more when the market is "cheap" (PE-adjusted), and less when "expensive."
- **Automated Data Fetching**: Pulls up-to-date S&P 500 PE ratios and prices from online sources.
- **Backtesting Support**: Includes historical backtesting using the Lumibot library.
- **Broker Integration**: Supports live and paper trading via Alpaca.
- **Configurable Parameters**: Easily adjust DCA amount and valuation sensitivity.
- **Secure Credentials**: API keys are managed via environment variables.
- **Robust Logging**: All trades and errors are logged for transparency.

## How It Works

1. **Fetches Current and Year-Ago S&P 500 PE Ratios** from live data.
2. **Calculates Relative Expensiveness**: Compares YoY change in index price to YoY change in PE ratio.
3. **Adjusts Investment Amount**: If the market is relatively cheap (price growth < PE growth), increases DCA; otherwise, decreases.
4. **Executes Trades Automatically** via the Alpaca API.

## Setup

1. Clone the repository.
2. Install dependencies:

Install dependencies:

bash
pip install -r requirements.txt
Set up your Alpaca API keys as environment variables.

Run the bot in backtest or live mode.

Example Usage
python
python tbot.py
Data Sources
S&P 500 PE ratios: Yahoo Finance via yfinance

S&P 500 prices: Yahoo Finance via yfinance

## Why This Outperforms Fixed DCA
By dynamically adjusting investment size based on relative market valuation, this strategy aims to buy more when the market is undervalued and less when overvalued, potentially improving risk-adjusted returns compared to fixed-amount DCA.

## Backtesting
Backtesting results (see /results/) demonstrate improved performance over traditional DCA, with higher returns and/or lower drawdowns over multiple market cycles.

## Disclaimer
This is a research project and not financial advice. Use at your own risk.
