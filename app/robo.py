
import os
import json
from functools import lru_cache
from dotenv import load_dotenv
import requests
from pandas import DataFrame
import plotly.express as px

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="abc123")

class RoboAdvisor:
    def __init__(self, symbol, api_key=API_KEY):
        self.symbol = symbol
        self.api_key = api_key
        self._parsed_response = None

    def fetch_data(self):
        # a private method of sorts - can alternatively be called _fetch_data() or something
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&apikey={self.api_key}"
        response = requests.get(request_url)
        return json.loads(response.text)

    @property
    @lru_cache(maxsize=None) # cache the results of this network request!
    def parsed_response(self):
        return self._parsed_response or self.fetch_data() # only make a real network request if we have not overridden / set this value (like we do when testing)

    @parsed_response.setter  # use a setter (mainly for testing purposes). see: https://docs.python.org/3/library/functions.html#property
    def parsed_response(self, value):
        self._parsed_response = value

    @property
    @lru_cache(maxsize=None) # cache the results of this data processing!
    def prices_df(self):
        if "Time Series (Daily)" not in list(self.parsed_response.keys()):
            return None

        records = []
        for date, daily_data in self.parsed_response["Time Series (Daily)"].items():
            records.append({
                "date": date,
                "open": float(daily_data["1. open"]),
                "high": float(daily_data["2. high"]),
                "low": float(daily_data["3. low"]),
                "close": float(daily_data["4. close"]),
                "volume": int(daily_data["5. volume"]),
            })
        return DataFrame(records)

    @property
    @lru_cache(maxsize=None) # cache the results of this data processing!
    def summary(self):
        """ Param : prices_df (pandas.DataFrame) """
        return {
            "latest_close": self.prices_df.iloc[0]["close"],
            "recent_high": self.prices_df["high"].max(),
            "recent_low": self.prices_df["low"].min(),
        }

    @property
    @lru_cache(maxsize=None) # cache the results of this data processing!
    def chart_df(self):
        """ Sorts the data by date ascending, so it can be charted """
        chart_df = self.prices_df.copy()
        chart_df.sort_values(by="date", ascending=True, inplace=True)
        return chart_df


if __name__ == '__main__':

    # FETCH DATA

    symbol = input("Please input a stock symbol (e.g. 'MSFT'): ")
    advisor = RoboAdvisor(symbol=symbol)

    # PROCESS DATA

    df = advisor.prices_df

    if isinstance(df, DataFrame):

        # DISPLAY RESULTS

        summary = advisor.summary

        print("LATEST CLOSING PRICE: ", summary["latest_close"])
        print("RECENT HIGH: ", summary["recent_high"])
        print("RECENT LOW: ", summary["recent_low"])

        # EXPORT PRICES TO CSV

        csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", f"{symbol.lower()}_prices.csv")
        df.to_csv(csv_filepath)

        # CHART PRICES OVER TIME

        fig = px.line(advisor.chart_df, x="date", y="close", title=f"Closing Prices for {symbol.upper()}") # see: https://plotly.com/python-api-reference/generated/plotly.express.line
        fig.show()
