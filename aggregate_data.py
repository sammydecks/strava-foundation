
"""
Print the top five indexes by largest size in size readable format (GB)
Args:
data: JSON data dictionary
"""
def print_largest_indexes(data):
    print("Printing largest indexes by storage size")
    # sort by the size (desc order) and take the first 5 in the sorted results
    sort_by_size = sorted(data, key=lambda x: int(x['pri.store.size']), reverse=True)[:5]
    for index in sort_by_size:
        # convert to readable format (byte to GB) rounded to hundreth
        byte_conversion = round((int(index['pri.store.size']) / (10 ** 9)),2)
        print("Index:", index['index'])
        print("Size:", byte_conversion, "GB")
    # extra newline (match example format)
    print()

def print_avg(data):
    print("Printing average of all index sizes")
    sum = 0
    count = 0
    for index in data:
        sum += int(index['pri.store.size'])
        count += 1
    avg = sum / count
    byte_conversion = round((int(avg) / (10 ** 9)),2)
    print("Average index size:", byte_conversion, "GB")

"""
Print the top five indexes by largest largest shard count
Args:
data: JSON data dictionary
"""
def print_most_shards(data):
    print("Printing largest indexes by shard count")
    # sort by the shard count (desc order) and take the first 5 in the sorted results
    sort_by_shards = sorted(data, key=lambda x: int(x['pri']), reverse=True)[:5]
    for index in sort_by_shards:
        print("Index:", index['index'])
        print("Shards:", index['pri'])
    # extra newline (match example format)
    print()

"""
Print the top 5 largest size (GB) to shard count ratios, as well as
the recommended shard count to have the recommended ratio of 1 shard 
for every 30GB
Args:
data: JSON data dictionary
"""
def print_least_balanced(data):
    print("Printing least balanced indexes")
    index_info = []
    rec_ratio = 30
    # calc the GB size and balance ration for each index
    for index in data:
        size_gb = round((int(index['pri.store.size']) / (10 ** 9)),2)
        balance_ratio = size_gb / int(index['pri'])
        index_info.append({
            "index": index['index'],
            "size": size_gb,
            "shards": int(index['pri']),
            "ratio": balance_ratio
        })
    # sort by balance ratio desc order and take top 5
    sort_by_ratio = sorted(index_info, key=lambda x: int(x['ratio']), reverse=True)[:5]
    for index in sort_by_ratio:
        print("Index:", index['index'])
        print("Size:", index['size'], "GB")
        print("Shard:", index['shards'])
        # round to integer
        print("Balance Ratio:", int(index['ratio']))
        # round to the next higher integer <------------------------????
        print("Recommended shard count is", int(int(index['size'])/rec_ratio))
