import os

# Securely load Alpaca API credentials from environment variables.
# This prevents accidental exposure of sensitive keys in code repositories.

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise EnvironmentError("Missing Alpaca API credentials. "
                           "Set ALPACA_API_KEY and ALPACA_SECRET_KEY as environment variables.")

ALPACA_CONFIG = {
# Put your own Alpaca key here:
"API_KEY": API_KEY,
# Put your own Alpaca secret here:
"API_SECRET": SECRET_KEY,
# If you want to go live, you must change this. It is currently set for paper trading
"PAPER": True
}
