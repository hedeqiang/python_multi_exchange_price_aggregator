# Multi Exchange Price Aggregator

The Multi Exchange Price Aggregator is a Python package that collects cryptocurrency prices from various exchanges such as Binance, OKX, Bitget, Kucoin, and more, and aggregates them into a unified format.

## Features

- Fetch price data from multiple cryptocurrency exchanges
- Aggregate data across exchanges based on priority
- Filter and retrieve optimal prices for specific trading pairs

## Installation

```bash
pip install multi_exchange_price_aggregator
```

## Usage
```python
from multi_exchange_price_aggregator import ExchangePriceAggregator

# Define exchange priority
exchanges_priority = ['binance', 'okx', 'bitget', 'kucoin', 'mexc', 'gate']

# Create aggregator instance
aggregator = ExchangePriceAggregator(exchanges_priority)

# Get aggregated pairs with priority
aggregated_pairs = aggregator.get_aggregated_pairs_with_priority(symbol_suffix='BTC')
print(aggregated_pairs)

```