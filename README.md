# Earnings-Notifier
A basic earnings notifier.

## Usage
```
python3 earnings_notifier.py
```
* Can update `exchanges.txt`, `tickers.txt` as needed.
* Requires a few pip modules.
  ```
  pip3 install requests
  pip3 install bs4
  pip3 install lxml
  pip3 install aiohttp
  pip3 install aiohttp_retry
  pip3 install httpx
  ```

tickers.txt contains a list of companies with market cap > USD 10B rated as strong buy.
List from https://www.nasdaq.com/market-activity/stocks/screener updated as of July 19, 2023.
