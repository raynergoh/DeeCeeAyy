import requests
from bs4 import BeautifulSoup
import time

url = f'https://www.multpl.com/s-p-500-pe-ratio'

response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')

class1 = "current"

currentPE = float(soup.find(id = class1).text.strip()[26:32])


