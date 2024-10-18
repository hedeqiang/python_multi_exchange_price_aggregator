import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor


class ExchangePriceAggregator:
    API_URLS = {
        'binance': 'https://api.binance.com/api/v3/ticker/price',
        'bitget': 'https://api.bitget.com/api/v2/spot/market/tickers',
        'okx': 'https://www.okx.com/api/v5/market/tickers?instType=SPOT',
        'kucoin': 'https://api.kucoin.com/api/v1/market/allTickers',
        'mexc': 'https://api.mexc.com/api/v3/ticker/price',
        'gate': 'https://api.gateio.ws/api/v4/spot/tickers',
        'kraken': 'https://api.kraken.com/0/public/Ticker',
        'huobi': 'https://api.huobi.pro/market/tickers',
        'bybit': 'https://api.bybit.com/v5/market/tickers?category=spot',
    }

    def __init__(self, exchanges_priority):
        self.exchanges_priority = exchanges_priority

    def _filter_pairs(self, data, exchange, symbol_suffix):
        """Filter and return trading pairs with unified symbol format."""
        pairs = {}
        try:
            if exchange == 'binance':
                for item in data:
                    if item['symbol'].endswith(symbol_suffix) and item['price'] not in [None, '']:
                        try:
                            pairs[item['symbol']] = float(item['price'])
                        except ValueError:
                            print(f"Invalid price data for {item['symbol']}: {item['price']}")

            elif exchange == 'bitget':
                for item in data.get('data', []):
                    if item['symbol'].endswith(symbol_suffix) and item['lastPr'] not in [None, '']:
                        try:
                            pairs[item['symbol'].upper()] = float(item['lastPr'])
                        except ValueError:
                            print(f"Invalid price data for {item['symbol']}: {item['lastPr']}")

            elif exchange == 'okx':
                for item in data.get('data', []):
                    if item['instId'].endswith(f'-{symbol_suffix}') and item['last'] not in [None, '']:
                        try:
                            pairs[item['instId'].replace(f'-{symbol_suffix}', symbol_suffix)] = float(item['last'])
                        except ValueError:
                            print(f"Invalid price data for {item['instId']}: {item['last']}")

            elif exchange == 'kucoin':
                for item in data.get('data', {}).get('ticker', []):
                    if item['symbol'].endswith(f'-{symbol_suffix}') and item['last'] not in [None, '']:
                        try:
                            pairs[item['symbol'].replace(f'-{symbol_suffix}', symbol_suffix)] = float(item['last'])
                        except ValueError:
                            print(f"Invalid price data for {item['symbol']}: {item['last']}")

            elif exchange == 'mexc':
                for item in data:
                    if item['symbol'].endswith(symbol_suffix) and item['price'] not in [None, '']:
                        try:
                            pairs[item['symbol']] = float(item['price'])
                        except ValueError:
                            print(f"Invalid price data for {item['symbol']}: {item['price']}")

            elif exchange == 'gate':
                for item in data:
                    if item['currency_pair'].endswith(f'_{symbol_suffix}') and item['last'] not in [None, '']:
                        try:
                            pairs[item['currency_pair'].replace(f'_{symbol_suffix}', symbol_suffix)] = float(
                                item['last'])
                        except ValueError:
                            print(f"Invalid price data for {item['currency_pair']}: {item['last']}")

            elif exchange == 'kraken':
                for pair, info in data.get('result', {}).items():
                    if pair.endswith(symbol_suffix):
                        try:
                            pairs[pair.replace(f'X{symbol_suffix}', symbol_suffix)] = float(info['c'][0])
                        except (KeyError, ValueError, IndexError):
                            print(f"Invalid price data for {pair}: {info}")

            elif exchange == 'huobi':
                for item in data.get('data', []):
                    if item['symbol'].endswith(symbol_suffix.lower()) and item['close'] not in [None, '']:
                        try:
                            pairs[item['symbol'].upper()] = float(item['close'])
                        except ValueError:
                            print(f"Invalid price data for {item['symbol']}: {item['close']}")

            elif exchange == 'bybit':
                for item in data.get('result', {}).get('list', []):
                    if item['symbol'].endswith(symbol_suffix) and item['lastPrice'] not in [None, '']:
                        try:
                            pairs[item['symbol']] = float(item['lastPrice'])
                        except ValueError:
                            print(f"Invalid price data for {item['symbol']}: {item['lastPrice']}")

        except (KeyError, TypeError, ValueError) as e:
            print(f"Error processing data for {exchange}: {e}")

        return pairs

    def _fetch_exchange_data(self, session, exchange):
        """Fetch data from a specific exchange."""
        try:
            url = self.API_URLS[exchange]
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return exchange, response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from {exchange}: {e}")
            return exchange, {}

    def _get_all_supported_pairs(self, session, exchange, symbol_suffix):
        """Fetch and filter trading pairs from an exchange."""
        exchange, data = self._fetch_exchange_data(session, exchange)
        if data:
            return self._filter_pairs(data, exchange, symbol_suffix)
        return {}

    def get_prices(self, symbol_suffix='USDT'):
        """Fetch and return unified price data from all exchanges."""
        unified_data = {}
        with requests.Session() as session, ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._get_all_supported_pairs, session, exchange, symbol_suffix): exchange
                       for exchange in self.exchanges_priority}

            for future in futures:
                exchange = futures[future]
                pairs = future.result()
                if pairs:
                    unified_data[exchange] = pairs

        return unified_data

    def get_aggregated_pairs_with_priority(self, symbols=None, symbol_suffix='USDT'):
        """Aggregate data according to exchange priority and return specified pairs."""
        aggregated_data = {}
        unified_data = self.get_prices(symbol_suffix)

        for exchange in self.exchanges_priority:
            pairs = unified_data.get(exchange, {})
            if not pairs:
                continue
            for symbol, price in pairs.items():
                if symbols is None or symbol in symbols:
                    if symbol not in aggregated_data:
                        aggregated_data[symbol] = {
                            "symbol": symbol,
                            "exchange": exchange,
                            "price": price,
                            "timestamp": int(time.time())
                        }

        return aggregated_data

    def get_aggregated_prices(self, symbols=None, symbol_suffix='USDT'):
        """Aggregate prices across exchanges."""
        unified_data = self.get_prices(symbol_suffix)

        aggregated_data = {}
        for exchange, pairs in unified_data.items():
            for symbol, price in pairs.items():
                if symbols is None or symbol in symbols:
                    if symbol not in aggregated_data:
                        aggregated_data[symbol] = []
                    aggregated_data[symbol].append({"exchange": exchange, "price": price})

        return aggregated_data

    def get_optimal_price(self, mode='max', symbols=None, symbol_suffix='USDT'):
        """Return optimal price (max or min) for each pair."""
        aggregated_data = self.get_aggregated_prices(symbols, symbol_suffix)

        optimal_data = {}
        for symbol, price_list in aggregated_data.items():
            if mode == 'max':
                optimal_entry = max(price_list, key=lambda x: x['price'])
            elif mode == 'min':
                optimal_entry = min(price_list, key=lambda x: x['price'])
            optimal_data[symbol] = optimal_entry

        return optimal_data