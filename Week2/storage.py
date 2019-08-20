import os
import tempfile
import argparse
import json
from collections import OrderedDict

parser = argparse.ArgumentParser(description='Key - value storage')
parser.add_argument('--key', help='Write key --key, without value --value to get value from storage.')
parser.add_argument('--val', help='Write value --value, to add this value with your key --key to the storage.')
args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
if not os.path.isfile(storage_path):
    with open(storage_path, 'w') as f:
        f.write('{}')
with open(storage_path, 'r') as f:
    my_dict = OrderedDict(json.load(f))
    result = my_dict.get(args.key, None)
if args.val is None:
    if result is None:
        print(None)
    else:
        for i in range(len(result) - 1):
            print(result[i], end=', ')
        print(result[len(result) - 1])
else:
    with open(storage_path, 'w') as f:
        if args.key in my_dict:
            my_dict[args.key].append(args.val)
        else:
            my_dict[args.key] = [args.val]
        json.dump(my_dict, f)
