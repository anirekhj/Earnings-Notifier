import argparse
import fileinput

# Create argument parser
parser = argparse.ArgumentParser(description='Process input text file and remove repetitions.')
parser.add_argument('input_file', type=str, help='Input file containing a list of values')

# Parse the command-line arguments
args = parser.parse_args()

# Read the values from the input file, convert to uppercase, and remove repetitions
values = set()
for line in fileinput.input(args.input_file, inplace=True):
    value = line.strip().upper()  # Convert the value to uppercase
    if value:
        if value not in values:
            values.add(value)
            print(value)
