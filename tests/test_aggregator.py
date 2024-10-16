import pytest
from multi_exchange_price_aggregator import ExchangePriceAggregator

def test_get_prices():
    exchanges_priority = ['binance', 'okx']
    aggregator = ExchangePriceAggregator(exchanges_priority)
    prices = aggregator.get_prices(symbol_suffix='USDT')
    assert isinstance(prices, dict)

def test_get_optimal_price():
    exchanges_priority = ['binance', 'okx']
    aggregator = ExchangePriceAggregator(exchanges_priority)
    optimal_prices = aggregator.get_optimal_price(symbols=['BTCUSDT'], mode='max')
    assert 'BTCUSDT' in optimal_prices