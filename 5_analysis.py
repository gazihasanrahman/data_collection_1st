import json
import glob
import pandas as pd
from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from typing import List, Optional, Union, Dict, Any
from models_pd import Fixture, Race, Entry


file = 'downloads/1752138913921.json'
# file = 'downloads/sample_fofixtures_1.json'

with open(file, 'r') as f:
    result = json.load(f)

fixture_data = result.get('fixtures', [])


for data in fixture_data:
    fixture = Fixture(**data)
    print(f"Fixture: {fixture.header.date}")
    for race in fixture.races:
        print(f"Race: {race.number}")
        for entry in race.entries:
            print(f"Horse: {entry.name} - Final Position:{entry.finalPosition.position} - status:{entry.status} - starting price:{entry.starting_price}")



