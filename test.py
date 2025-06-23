import os
import requests
from dotenv import load_dotenv  

load_dotenv()  

API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

response = requests.get(f"{BASE_URL}/v2/positions", headers=headers)
print("Status:", response.status_code)
print("Response:", response.text)
