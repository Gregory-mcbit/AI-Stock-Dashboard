import os
import dotenv
import requests
import pandas as pd


dotenv.load_dotenv(".env")


class StockApiClient:
	_base_url = "https://www.alphavantage.co/query?function="
	_api_token = os.getenv("API_TOKEN")


	def __init__(self, ticker, start_date, end_date, output_size="full", function="TIME_SERIES_DAILY"):
		self.ticker = ticker
		self.function = function
		self.output_size = output_size
		self.start_date = start_date
		self.end_date = end_date
		self.url = self._base_url + function + "&symbol=" + ticker + "&outputsize=" + self.output_size + "&apikey=" + self._api_token


	def get_data(self):
		self.data = requests.get(self.url).json()
		result = self._data_preprocessing()

		return result


	def _data_preprocessing(self):
		df = pd.DataFrame(self.data["Time Series (Daily)"])
		df = df.T
		df.columns = ["open", "high", "low", "close", "volume"]
		df.index.name = "date"

		return df.loc[self.start_date:self.end_date]
