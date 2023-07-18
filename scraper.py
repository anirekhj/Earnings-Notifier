import argparse
import concurrent.futures
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import time

# Create argument parser
parser = argparse.ArgumentParser(description='Scrape earnings data for a list of stock symbols.')
parser.add_argument('input_file', type=str, help='Input file containing a list of tickers')

# Parse the command-line arguments
args = parser.parse_args()

# Read the tickers from the input file
tickers = []
with open(args.input_file, 'r') as file:
    tickers = file.read().splitlines()

# Define base URL
base_url = 'https://www.marketbeat.com'

# Read the exchanges from the input file
exchanges_file = "exchanges.txt"
exchanges = []
with open(exchanges_file, 'r') as file:
    for line in file:
        exchange = line.strip()
        exchanges.append(exchange)

# Initialize a list to store ticker details
ticker_details = []

# Define a function to fetch earnings data for a given ticker and exchange
def fetch_earnings(ticker, exchange):
    url = f'{base_url}/stocks/{exchange}/{ticker}/earnings/'
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    response = requests.get(url, headers=agent)
    if response.ok:
        soup = BS(response.content, 'html.parser')
        element = soup.find('dd', class_='stat-summary-heading my-1')
        if element:
            values = list(element.stripped_strings)
            date_string = values[0]
            current_date = datetime.now().date()
            current_year = datetime.now().year
            earnings_date = datetime.strptime(date_string + ' ' + str(current_year), '%b. %d %Y').date()
            days_until_earnings = (earnings_date - current_date).days

            if 0 <= days_until_earnings <= 30:
                return (ticker, exchange, days_until_earnings, earnings_date, ' '.join(values[1:]))

# Start measuring the execution time
start_time = time.time()

# Process each ticker and exchange using multiprocessing
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Use concurrent futures to execute fetch_earnings for each ticker and exchange combination
    futures = []
    for stock_symbol in tickers:
        for exchange in exchanges:
            futures.append(executor.submit(fetch_earnings, stock_symbol, exchange))

    # Collect the results from completed futures
    ticker_details = []
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result is not None:
            ticker_details.append(result)

# Sort the ticker details based on days until earnings in descending order
ticker_details.sort(key=lambda x: x[2], reverse=True)

# Print the ticker details
for ticker_detail in ticker_details:
    stock_symbol, exchange, days_until_earnings, earnings_date, additional_values = ticker_detail
    print(f"Ticker: {stock_symbol}")
    print(f"Exchange: {exchange}")
    print(f"Earnings date is {days_until_earnings} days from today: {earnings_date.strftime('%b. %d, %Y')}")
    print(additional_values)
    print()

# Calculate the elapsed time
elapsed_time = time.time() - start_time

# Print the elapsed time with 3 decimal places
print(f"Execution time: {round(elapsed_time, 3)} seconds")
