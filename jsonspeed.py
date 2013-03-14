import sys
import time
import os

def usage():
    print "Usage: env/bin/python jsonspeed.py <directory-with-json-files>"

try:
    import ujson
    import simplejson
except ImportError, e:
    usage()
    sys.exit(1)

import json
from collections import defaultdict

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
        try:
            result = test(sys.argv[1], module)
        except IndexError, e:
            usage()
            sys.exit(1)
        end = time.time()
        dur = end-start
        print module, result['byte'], result['file'], dur, result['byte']/dur

if __name__ == '__main__':
    main()
