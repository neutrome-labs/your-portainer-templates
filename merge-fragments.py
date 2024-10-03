#!/usr/bin/env python

import json

data = {}
with open('portainer-v2.json') as f:
    data = json.load(f)
    for template in data['templates']:
        fragment_file = template['repository']['stackfile'].replace('docker-compose.yml', 'fragment.json')
        with open(fragment_file) as j:
            jdata = json.load(j)
            template['env'] = jdata

with open('portainer-v2.json', 'w') as f:
    json.dump(data, f, indent=2)