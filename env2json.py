#!/usr/bin/env python

import sys
import json

if len(sys.argv) < 2:
    print('Usage: env2json.py [--no-prefix] <env_file1> [env_file2] ...')
    sys.exit(1)

noprefix = False
if sys.argv[1] == '--no-prefix':
    noprefix = True

fragments = []
for arg in sys.argv[2 if noprefix else 1:]:
    prefix = ''
    edata = {}
    with open(arg, 'r') as f:
        prefix = f.name.split('/')[-1].split('.')
        prefix = prefix[0] + '_' if len(prefix) > 1 and not noprefix else ''
        
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip()
            if not line:
                continue
            key, value = line.split('=', 1)
            if value is None or value == '' or value == 'null':
                value = None
            edata[key] = value

    for x in edata:
        fragments.append({
            "name": x,
            "label": prefix.upper() + x,
        })
        if edata[x] is not None:
            fragments[-1]["default"] = edata[x]

jdata = json.dumps(fragments, skipkeys=True, indent=2)
print(jdata)