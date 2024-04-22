#!/usr/bin/python3

import requests
import json
from subprocess import run

EVENT = 'carnival'

event_data = json.loads(requests.get(f'https://platform.modfest.net/event/{EVENT}').text)
projects = set()

for _, participant in event_data['participants'].items():
    for project_id in participant['submissions']:
        if project_id not in projects:
            run(['packwiz', 'mr', 'add', project_id])
            projects.add(project_id)