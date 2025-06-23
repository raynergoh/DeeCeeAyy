import os
from dotenv import load_dotenv  

load_dotenv()  

API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise EnvironmentError("Missing Alpaca API credentials. "
                           "Set ALPACA_API_KEY and ALPACA_SECRET_KEY in your .env file.")

ALPACA_CONFIG = {
    "API_KEY": API_KEY,
    "API_SECRET": SECRET_KEY,
    # Set this to False to use a live account
    "PAPER": True,  
}

