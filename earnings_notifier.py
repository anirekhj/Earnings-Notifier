import subprocess

# Clean up exchanges.txt
process_input_exchanges = subprocess.Popen(['python3', 'process_input.py', "exchanges.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Clean up tickers.txt
process_input_tickers = subprocess.Popen(['python3', 'process_input.py', "tickers.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for both process_input.py processes to finish
process_input_exchanges.wait()
process_input_tickers.wait()

# Run the scraper
subprocess.run(['python3', 'scraper.py', "tickers.txt"], check=True)
