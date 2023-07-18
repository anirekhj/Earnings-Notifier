import argparse
import asyncio
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import time
import httpx

# Create argument parser
parser = argparse.ArgumentParser(description='Scrape earnings data for a list of stock symbols.')
parser.add_argument('input_file', type=str, help='Input file containing a list of tickers')

# Parse the command-line arguments
args = parser.parse_args()

# Read the tickers from the input file
with open(args.input_file, 'r') as file:
    tickers = file.read().splitlines()

# Define base URL
base_url = 'https://www.marketbeat.com'

# Read the exchanges from the input file
exchanges_file = "exchanges.txt"
with open(exchanges_file, 'r') as file:
    exchanges = [line.strip() for line in file]

# Initialize a list to store ticker details
ticker_details = []

# Define a function to fetch earnings data for a given ticker and exchange
async def fetch_earnings(session, ticker, exchange):
    url = f'{base_url}/stocks/{exchange}/{ticker}/earnings/'
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    response = await session.get(url, headers=agent)
    if response.status_code == 200:
        content = response.content
        soup = BS(content, 'lxml')  # Use lxml parser for faster parsing

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

async def main():
    tasks = []
    async with httpx.AsyncClient() as client:
        for ticker in tickers:
            for exchange in exchanges:
                tasks.append(fetch_earnings(client, ticker, exchange))

        ticker_details = await asyncio.gather(*tasks)

    # Remove None values and sort the ticker details based on days until earnings in descending order
    ticker_details = [td for td in ticker_details if td is not None]
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

# Run the event loop
asyncio.run(main())
