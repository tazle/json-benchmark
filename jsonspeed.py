import ujson
import json
import simplejson
from collections import defaultdict
import sys
import time
import os

def test(directory, jsonmodule):
    counts = defaultdict(lambda: 0)
    for fname in os.listdir(directory):
        if fname.endswith('.json'):
            counts['file'] += 1
            path = os.path.join(directory, fname)
            f = file(path, 'rb')
            rawdata = f.read()
            f.close()
            counts['byte'] += len(rawdata)
            data = jsonmodule.loads(rawdata)
            for k in data:
                if k not in ['file', 'byte'] and isinstance(data[k], list):
                    counts[k] += len(data[k])
    return counts

def main():
    for module in [ujson, json, simplejson]:
        start = time.time()
        result = test(sys.argv[1], module)
        end = time.time()
        dur = end-start
        print module, result['byte'], result['file'], dur, result['byte']/dur

if __name__ == '__main__':
    main()
