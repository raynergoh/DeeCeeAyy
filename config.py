import os
from dotenv import load_dotenv  

load_dotenv()  

API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise EnvironmentError("Missing Alpaca API credentials. "
                           "Set ALPACA_API_KEY and ALPACA_SECRET_KEY in your .env file.")

# ALPACA_CONFIG = {
#     "API_KEY": API_KEY,
#     "API_SECRET": SECRET_KEY,
#     # Set this to False to use a live account
#     "ENDPOINT": "https://paper-api.alpaca.markets/v2",  
# }

# ALPACA_CONFIG = {
#     "APCA_API_KEY_ID": "PK8HBMWNX2FEK70T4LHG",
#     "APCA_API_SECRET_KEY": "RC156zq3b7I6DmkiRgfInXVe82HG8dL63nfih9Ro",
#     # Set this to False to use a live account
#     "ENDPOINT": "https://paper-api.alpaca.markets/v2",  
# }

ALPACA_CONFIG = {
    "API_KEY": API_KEY,
    "API_SECRET": SECRET_KEY,
    # Set this to False to use a live account
    "PAPER": True,  
}

# print("API KEY:", os.getenv("ALPACA_SECRET_KEY")) 
# print("ALPACA_CONFIG:", ALPACA_CONFIG)
