from alpha_vantage.sectorperformance import SectorPerformances
import matplotlib.pyplot as plt
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import matplotlib.pyplot as plt

base_url = 'https://www.alphavantage.co/query?'
params = {'function': 'OVERVIEW',
         'symbol': 'IBM',
         'apikey': keys}

response = requests.get(base_url, params=params)
print(response.json())
