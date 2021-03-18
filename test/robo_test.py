
#from app.robo import fetch_data

from conftest import mock_msft_response

def test_fetch_data(parsed_googl_response):
    keys = list(parsed_googl_response.keys())
    assert "Meta Data" in keys
    assert "Time Series (Daily)" in keys
