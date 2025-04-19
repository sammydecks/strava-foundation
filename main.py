import argparse
import sys
import json
import requests
from datetime import date, timedelta
from aggregate_data import *

"""
Read the data from a JSON file and return as dictionary
Args:
file_path (str): path to JSON being read from
Returns:
list of dict of JSON data or None if error occurs
"""
def get_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as err:
        sys.exit("Error loading JSON data:", err)
        return None

"""
Fetches index data from a logging server for the past N days.
Args:
endpoint (str): The base URL of the logging server
days (int): Number of days of data to retrieve, starting from yesterday.
Returns:
list of dict of JSON data
"""
def get_data_from_server(endpoint, days):
    data = []
    start_date = date.today()
    delta = timedelta(days=1)
    current_date = start_date - delta
    # from yesterday, create the API query for each of the n previous days
    for _ in range(days):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        url=f"https://{endpoint}/_cat/indices/*{year:04d}*{month:02d}*{day:02d}?v&h=index,pri.store.size,pri&format=json&bytes=b"
        data.extend(fetch_data(url))
        current_date -= delta
    return data

"""
Sends a GET request to the specified URL and returns the JSON response.
Args:
url (str): The complete URL for the API request.
Returns:
JSON Reponse (dict) for one day's worth of data
"""
def fetch_data(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            day_data = response.json()
            return day_data
        else:
            print('Error:', response.status_code)
            return None
    except Exception as err:
        print('Error:', err)
        return None
    

def main():
    parser = argparse.ArgumentParser(description="Process index data.")
    parser.add_argument("--endpoint", type=str, default="",
                        help="Logging endpoint")
    parser.add_argument("--debug", action="store_true",
                        help="Debug flag used to run locally")
    parser.add_argument("--days", type=int, default=7,
                        help="Number of days of data to parse")
    # add file path as command line arg
    parser.add_argument("--file", type=str,
                    help="Path to JSON input when using debug mode")
    args = parser.parse_args()

    data = None

    if args.debug:
        try:
            data = get_data_from_file(args.file)
        except Exception as err:
            sys.exit("Error reading data from file. Error: " + str(err))
    else:
        try:
            data = get_data_from_server(args.endpoint, args.days)
        except Exception as err:
            sys.exit("Error reading data from API endpoint. Error: " + str(err))

    # only run data aggregation if data has been loaded
    if data is not None:
        print_largest_indexes(data)
        print_most_shards(data)
        print_least_balanced(data)
    else:
        sys.exit("No data was loaded.")

if __name__ == '__main__':
    main()
