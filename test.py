import os
import requests
from dotenv import load_dotenv  

load_dotenv()  

API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets/v2/positions"

headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

print(requests.get(BASE_URL, headers=headers).text)

response = requests.get(f"{BASE_URL}", headers=headers)
print("Status:", response.status_code)
print("Response:", response.text)
