# Foundation Take Home Index Data Aggregator

## Requirements

Make sure you have Python 3 installed and the following Python packages:

```bash
pip install requests
```

## Running with Live API Endpoint

```bash
python main.py --endpoint baseurl --days 3
```

Arguments:

- --endpoint: The base URL of the logging server
- --days: (Optional) Number of days of data to fetch, counting backward from yesterda (default: 7)

## Running in Debug Mode with Local File

```bash
python main.py --debug --file path/to/input.json
```

Arguments:

- --debug: Run in debug mode, loading data from a file instead of making API requests
- --file: Path to a JSON file containing index data

## Output

Once data is loaded, the script will:

- Print the top 5 indexes with the largest primary store size in readable format (GB)
- Print the top 5 indexes with the most shards
- Print the top 5 least balanced indexes (based on shard balance ratio) with recommended shard count

## File Overview

- main.py: Main driver script
- aggregate_data.py: Contains helper functions to process and analyze the loaded data

## Resources Used:

- Reading JSON: https://www.geeksforgeeks.org/read-json-file-using-python/
- Sort dict: https://www.geeksforgeeks.org/python-sorted-function/
- Iterate over dates: https://www.geeksforgeeks.org/python-iterating-through-a-range-of-dates/
- Making API requests: https://www.geeksforgeeks.org/how-to-make-api-calls-using-python/

## Questions

For the last calculations on the balance ratios, I was a bit confused on the rounding expectations. It seems like for the ratio itself, this is an integer result where you always round to the floor int? For the recomended shard count it also seemed that for most cases you round to the floor int? This workedthe majority of the time, but there were a couple cases from the example (swirly and oblivion) where I had some rounding issues and I just wanted to clarify what the actual expectations were.

I am assuming, for the case of making the API requests that given the number of days, we would then request data from the n previous days. So from the example in the prompt, if today is April 15th, 2025 and we specified --days 1 then we would just request data from April 14th, 2025.
