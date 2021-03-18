import os
import pytest
from pandas import DataFrame

from app.robo import RoboAdvisor

# expect default environment variable setting of "CI=true" on Travis CI. see: https://docs.travis-ci.com/user/environment-variables/#default-environment-variables
CI_ENV = os.getenv("CI") == "true"

@pytest.mark.skipif(CI_ENV==True, reason="avoid issuing HTTP requests on the CI server") # skips this test on CI
def test_parsed_response(googl_advisor, oops_advisor):
    # with valid symbol, should containing certain expected characteristics (time series data with daily prices):
    parsed_response = googl_advisor.parsed_response
    response_keys = list(parsed_response.keys()) # we are testing the fetch_data function indirectly through our fixture (see conftest.py)
    assert "Meta Data" in response_keys
    assert "Time Series (Daily)" in response_keys
    daily_prices = list(parsed_response["Time Series (Daily)"].values())[0] #> {'1. open': '2068.4700', '2. high': '2099.0000', '3. low': '2044.1218', '4. close': '2082.2200', '5. volume': '1319126'}
    price_keys = list(daily_prices.keys())
    assert price_keys == ["1. open", "2. high", "3. low", "4. close", "5. volume"]

    # with invalid symbol, should contain an error message / not the expected data:
    parsed_response = oops_advisor.parsed_response
    response_keys = list(parsed_response.keys()) # we are testing the fetch_data function indirectly through our fixture (see conftest.py)
    assert "Meta Data" not in response_keys
    assert "Time Series (Daily)" not in response_keys


@pytest.mark.skipif(CI_ENV==True, reason="avoid issuing HTTP requests on the CI server") # skips this test on CI
def test_prices_df(googl_advisor, oops_advisor):
    # with valid symbol, should provide a dataframe with expected headers:
    assert isinstance(googl_advisor.prices_df, DataFrame)
    assert len(googl_advisor.prices_df) == 100
    assert list(googl_advisor.prices_df.columns) == ["date", "open", "high", "low", "close", "volume"]

    # with invalid symbol, should gracefully handle response errors / be null:
    assert oops_advisor.prices_df is None

def test_summary(mock_msft_advisor, mock_amzn_advisor):
    # should summarize and aggregate the data, noting the latest close, recent high, and recent low:
    assert mock_msft_advisor.summary == {
        'latest_close': 237.71,
        'recent_high': 240.055,
        'recent_low': 231.81
    }
    assert mock_amzn_advisor.summary == {
        'latest_close': 3091.86,
        'recent_high': 3131.7843,
        'recent_low': 3030.05
    }

def test_charting(mock_amzn_advisor):
    # it should sort dates in the proper order (ascending) for charting:
    assert mock_amzn_advisor.chart_df["date"].tolist() == ['2030-03-10', '2030-03-11', '2030-03-12', '2030-03-15', '2030-03-16']
