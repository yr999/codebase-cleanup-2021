
from conftest import mock_msft_response, mock_amzn_response #, mock_error_response, mock_rate_limit_response
from pandas import DataFrame

from app.robo import process_data, summarize_data

def test_fetch(parsed_googl_response):
    # we are testing the fetch_data function indirectly through our fixture (see conftest.py)

    response_keys = list(parsed_googl_response.keys())
    assert "Meta Data" in response_keys
    assert "Time Series (Daily)" in response_keys

    prices = list(parsed_googl_response["Time Series (Daily)"].values())[0] #> {'1. open': '2068.4700', '2. high': '2099.0000', '3. low': '2044.1218', '4. close': '2082.2200', '5. volume': '1319126'}
    price_keys = list(prices.keys())
    assert price_keys == ["1. open", "2. high", "3. low", "4. close", "5. volume"]

def test_process(parsed_googl_response):
    googl_df = process_data(parsed_googl_response)
    assert isinstance(googl_df, DataFrame)
    assert len(googl_df) == 100
    assert list(googl_df.columns) == ["date", "open", "high", "low", "close", "volume"]

def test_summarize():
    assert summarize_data(process_data(mock_msft_response)) == {
        'latest_close': 237.71,
        'recent_high': 240.055,
        'recent_low': 231.81
    }
    assert summarize_data(process_data(mock_amzn_response)) == {
        'latest_close': 3091.86,
        'recent_high': 3131.7843,
        'recent_low': 3030.05
    }
