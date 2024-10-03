#!/usr/bin/env python

import sys
import json

if len(sys.argv) < 2:
    print('Usage: env2json.py [--no-prefix] <env_file1> [env_file2] ...')
    sys.exit(1)

noprefix = False
if sys.argv[1] == '--no-prefix':
    noprefix = True

important = 0
fragments = []
for arg in sys.argv[2 if noprefix else 1:]:
    prefix = ''
    with open(arg, 'r') as f:
        prefix = f.name.split('/')[-1].split('.')
        prefix = prefix[0] + '_' if len(prefix) > 1 and not noprefix else ''
        
        for line in f:
            if line.startswith('#'):
                continue
            
            line = line.strip()
            if not line:
                continue
           
            data, comment = line.split('#', 1) if '#' in line else (line, '')
            key, value = line.split('=', 1) if '=' in line else (line, None)
            if value is None or value == '' or value == 'null':
                value = None
            
            m = {"name": key, "label": prefix.upper() + key}
            if value is not None:
                m["default"] = value.strip()
            
            if comment.strip() == '!important':
                fragments.insert(important, m)
                important += 1
            else:
                fragments.append(m)
            
        

jdata = json.dumps(fragments, skipkeys=True, indent=2)
print(jdata)