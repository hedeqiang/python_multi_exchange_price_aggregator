# Multi Exchange Price Aggregator

The **Multi Exchange Price Aggregator** is a Python package that collects cryptocurrency prices from various exchanges such as Binance, OKX, Bitget, Kucoin, and more. The package aggregates prices from these exchanges, allowing users to query and retrieve price information, aggregate data across exchanges based on priority, and find optimal prices for specific trading pairs.

## Features

- Fetch real-time cryptocurrency prices from multiple exchanges.
- Aggregate price data across exchanges based on priority.
- Retrieve and filter trading pairs based on a specified symbol suffix (e.g., "USDT").
- Retrieve optimal prices (maximum or minimum) for specified trading pairs.
- Fully customizable exchange list and symbol suffix.

## Supported Exchanges

The following exchanges are supported:
- Binance
- Bitget
- OKX
- Kucoin
- MEXC
- Gate.io

## Installation

You can install the package via `pip`:

```bash
pip install multi_exchange_price_aggregator
```

## Basic Usage

Here’s a quick guide on how to use the **Multi Exchange Price Aggregator**:

### 1. Initialize the Aggregator

First, define the priority of exchanges you'd like to query, and create an instance of `ExchangePriceAggregator`:

```python
from multi_exchange_price_aggregator import ExchangePriceAggregator

# Define exchange priority
exchanges_priority = ['binance', 'okx', 'bitget', 'kucoin', 'mexc', 'gate']

# Create the aggregator instance
aggregator = ExchangePriceAggregator(exchanges_priority)
```


### 2. Aggregate Trading Pairs with Exchange Priority

You can aggregate trading pairs based on exchange priority using the `get_aggregated_pairs_with_priority()` method. This method returns the price data for each trading pair from the highest-priority exchange where the pair is available:

```python
# Aggregate pairs based on exchange priority
aggregated_pairs = aggregator.get_aggregated_pairs_with_priority(symbol_suffix='USDT')

print(aggregated_pairs)
```

- **Output**: This method returns a dictionary where each trading pair appears only once, based on the highest-priority exchange that has the pair.

```json
{
  "BTCUSDT": {
    "symbol": "BTCUSDT",
    "exchange": "binance",
    "price": 50000.0,
    "timestamp": 1634567890
  },
  "ETHUSDT": {
    "symbol": "ETHUSDT",
    "exchange": "okx",
    "price": 3498.0,
    "timestamp": 1634567891
  }
}
```

### 3. Retrieve Optimal Prices Across Exchanges

You can retrieve the optimal prices (either maximum or minimum) for each trading pair across exchanges using the `get_optimal_price()` method. You can specify the mode as either `'max'` or `'min'`:

```python
# Get the maximum price for each pair
max_prices = aggregator.get_optimal_price(mode='max', symbols=['BTCUSDT', 'ETHUSDT'])

print(max_prices)

# Get the minimum price for each pair
min_prices = aggregator.get_optimal_price(mode='min', symbols=['BTCUSDT', 'ETHUSDT'])

print(min_prices)
```

- **Output**: This method returns the highest or lowest price for each trading pair across all exchanges:

```json
{
  "BTCUSDT": {
    "exchange": "binance",
    "price": 50000.0
  },
  "ETHUSDT": {
    "exchange": "binance",
    "price": 3500.0
  }
}
```

### 4. Fetch Prices for Specific Symbols

If you want to fetch prices for specific symbols only, pass a list of symbols to the `get_prices()` method:

```python
# Fetch prices for specific symbols only
prices = aggregator.get_prices(symbol_suffix='USDT')
print(prices)

# Filter out and fetch prices for only BTCUSDT and ETHUSDT
aggregated_pairs = aggregator.get_aggregated_pairs_with_priority(symbols=['BTCUSDT', 'ETHUSDT'], symbol_suffix='USDT')
print(aggregated_pairs)
```

## License: [MIT](LICENSE)