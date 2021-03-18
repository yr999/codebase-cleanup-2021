
from unittest import mock
from conftest import mock_msft_response, mock_amzn_response #, mock_error_response, mock_rate_limit_response
from pandas import DataFrame

from app.robo import RoboAdvisor

# SKIP CI
def test_fetch(parsed_googl_response):
    # it should fetch data containing certain expected characteristics:
    response_keys = list(parsed_googl_response.keys()) # we are testing the fetch_data function indirectly through our fixture (see conftest.py)
    assert "Meta Data" in response_keys
    assert "Time Series (Daily)" in response_keys
    # ... including time series data with daily prices:
    daily_prices = list(parsed_googl_response["Time Series (Daily)"].values())[0] #> {'1. open': '2068.4700', '2. high': '2099.0000', '3. low': '2044.1218', '4. close': '2082.2200', '5. volume': '1319126'}
    price_keys = list(daily_prices.keys())
    assert price_keys == ["1. open", "2. high", "3. low", "4. close", "5. volume"]

# SKIP CI
def test_prices_df(parsed_googl_response, parsed_oops_response):
    # it should process the nested response data:
    advisor = RoboAdvisor(symbol="GOOGL") # SETUP STEP
    advisor.parsed_response = parsed_googl_response # SETUP STEP / OVERRIDE WITH MOCK DATA
    assert isinstance(advisor.prices_df, DataFrame)
    assert len(advisor.prices_df) == 100
    assert list(advisor.prices_df.columns) == ["date", "open", "high", "low", "close", "volume"]

    # it should gracefully handle response errors:
    advisor = RoboAdvisor(symbol="OOPS") # SETUP STEP
    advisor.parsed_response = parsed_oops_response # SETUP STEP / OVERRIDE WITH MOCK DATA
    assert advisor.prices_df is None

def test_summary():
    # it should summarize and aggregate the data:

    advisor = RoboAdvisor(symbol="MSFT") # SETUP STEP
    advisor.parsed_response = mock_msft_response # SETUP STEP / OVERRIDE WITH MOCK DATA
    assert advisor.summary == {
        'latest_close': 237.71,
        'recent_high': 240.055,
        'recent_low': 231.81
    }

    advisor = RoboAdvisor(symbol="AMZN") # SETUP STEP
    advisor.parsed_response = mock_amzn_response # SETUP STEP / OVERRIDE WITH MOCK DATA
    assert advisor.summary == {
        'latest_close': 3091.86,
        'recent_high': 3131.7843,
        'recent_low': 3030.05
    }





def test_charting():
    advisor = RoboAdvisor(symbol="AMZN") # SETUP STEP
    advisor.parsed_response = mock_amzn_response # SETUP STEP / OVERRIDE WITH MOCK DATA
    # it should sort dates in the proper order (ascending) for charting:
    assert advisor.chart_df["date"].tolist() == ['2030-03-10', '2030-03-11', '2030-03-12', '2030-03-15', '2030-03-16']
