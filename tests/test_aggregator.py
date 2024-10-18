import pytest
from multi_exchange_price_aggregator import ExchangePriceAggregator

def test_get_prices():
    exchanges_priority =  ['binance', 'okx', 'bitget', 'kucoin', 'mexc', 'gate', 'kraken', 'huobi', 'bybit']
    aggregator = ExchangePriceAggregator(exchanges_priority)
    prices = aggregator.get_prices(symbol_suffix='USDT')
    print(prices)
    # assert isinstance(prices, dict)

def test_get_optimal_price():
    exchanges_priority = ['binance', 'okx', 'bitget', 'kucoin', 'mexc', 'gate']
    aggregator = ExchangePriceAggregator(exchanges_priority)
    optimal_prices = aggregator.get_optimal_price(symbols=['BTCUSDT'], mode='max')
    print(optimal_prices)

    aggregator = ExchangePriceAggregator(exchanges_priority)
    optimal_prices = aggregator.get_optimal_price(symbols=['BTCUSDT'], mode='min')
    print(optimal_prices)
