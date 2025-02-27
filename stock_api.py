import os
import dotenv
import requests


dotenv.load_dotenv(".env")


class StockApiClient:
	_base_url = "https://www.alphavantage.co/query?function="
	_api_token = os.getenv("API_TOKEN")


	def __init__(self, ticker, date, function="HISTORICAL_OPTIONS"):
		self.ticker = ticker
		self.function = function
		self.date = date
		self.url = self._base_url + function + "&symbol=" + ticker + "&date=" + self.date + "&apikey=" + self._api_token
	
	
	def get_data(self):
		data = requests.get(self.url).json()
		return data


client = StockApiClient("IBM", "2017-11-02")
print(client.get_data())