import argparse
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta

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

# Initialize a list to store ticker details
ticker_details = []

# Process each ticker
for stock_symbol in tickers:
    # Initialize the values variable
    values = []

    # Try different exchanges until the ticker is found or no exchanges left
    # Read the exchange from the input file
    exchanges_file = "exchanges.txt"
    exchanges = []
    with open(exchanges_file, 'r') as file:
        for line in file:
            exchange = line.strip()
            exchanges.append(exchange)

    # Try different exchanges until the ticker is found or no exchanges left
    for exchange in exchanges:
        url = f'{base_url}/stocks/{exchange}/{stock_symbol}/earnings/'
        agent = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }
        response = requests.get(url, headers=agent)
        if response.ok:
            soup = BS(response.content, 'html.parser')
            element = soup.find('dd', class_='stat-summary-heading my-1')
            if element:
                values.extend(element.stripped_strings)
                break

    # Check if the value exists and compare it to today's date
    if values:
        date_string = list(values)[0]
        current_date = datetime.now().date()
        current_year = datetime.now().year
        earnings_date = datetime.strptime(date_string + ' ' + str(current_year), '%b. %d %Y').date()
        days_until_earnings = (earnings_date - current_date).days

        if 0 <= days_until_earnings <= 30:
            ticker_details.append((stock_symbol, days_until_earnings, earnings_date, ' '.join(values[1:])))

# Sort the ticker details based on days until earnings in descending order
ticker_details.sort(key=lambda x: x[1], reverse=True)

# Print the ticker details
for ticker_detail in ticker_details:
    stock_symbol, days_until_earnings, earnings_date, additional_values = ticker_detail
    print(f"Ticker: {stock_symbol}")
    print(f"Earnings date is {days_until_earnings} days from today: {earnings_date.strftime('%b. %d, %Y')}")
    print(additional_values)
    print()
