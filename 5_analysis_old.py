import json
import glob
import pandas as pd
from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from typing import List, Optional, Union, Dict, Any
from models_pd import Fixture, Race, Entry
import models_pd as etl


def parse_fixture(data: Dict[str, Any]) -> etl.Fixture:
    fixture = etl.Fixture(
        fixture_id=data.get('header',{}).get('id'),
        fixture_date=data.get('header',{}).get('date'),
        firstposttime=data.get('header',{}).get('firstposttime'),
        racecount=data.get('header',{}).get('racecount'),
        temperature_fahrenheit=data.get('header',{}).get('temperature',{}).get('fahrenheit'),
        temperature_celsius=data.get('header',{}).get('temperature',{}).get('celsius'),
        track=etl.Track(
            track_id=data.get('track',{}).get('id')
        ),
        races=[
            etl.Race(
                race_id=race.get('id'),
                race_number=race.get('number'),
                race_name=race.get('name'),
                runnercount=race.get('runnercount'),
                posttime=race.get('posttime'),
                estimatedPosttime=race.get('estimatedPosttime'),
                offTime=race.get('offTime'),
                weather=race.get('weather'),
                going=race.get('going'),
                status=race.get('status'),
                tracksurface=race.get('tracksurface',{}).get('value'),
                overround=race.get('overround'),
                overround_selection=race.get('overround_selection'),
                comment=race.get('comment'),

                statusHistory=[
                    etl.StatusHistory(
                        status=status.get('status'),
                        timestamp=status.get('timestamp')
                    )
                    for status in race.get('statusHistory', [])
                ],

                entries=[
                    etl.Entry(
                        entry_id=entry.get('id'),
                        programNumber=entry.get('programNumber'),
                        startNumber=entry.get('startNumber'),
                        startPosition=entry.get('startPosition'),
                        coupledIndicator=entry.get('coupledIndicator'),
                        decoupledNumber=entry.get('decoupledNumber'),
                        horse_id=entry.get('horse_id'),
                        horse_name=entry.get('name'),
                        status_id=entry.get('status'),
                        weight=entry.get('weight',{}).get('value'),
                        weight_unit=entry.get('weight',{}).get('unit'),
                        jockey_id=entry.get('jockey',{}).get('id'),
                        jockey_name=entry.get('jockey',{}).get('name'),
                        position=entry.get('finalPosition',{}).get('position'),
                        deadHeat=entry.get('finalPosition',{}).get('deadHeat'),
                        disqualified=entry.get('finalPosition',{}).get('disqualified'),
                        amendedPosition=entry.get('finalPosition',{}).get('amendedPosition'),
                        starting_price_nominator=entry.get('startingPrice',{}).get('nominator'),
                        starting_price_denominator=entry.get('startingPrice',{}).get('denominator'),
                        runnerTip=entry.get('runnerTip'),
                        price_history=[
                            etl.PriceHistory(
                                timestamp=price.get('timestamp'),
                                numerator=price.get('nominator'),
                                denominator=price.get('denominator'),
                                market=price.get('market')
                            )
                            for price in entry.get('showPrices', [])
                        ]
                    )
                    for entry in race.get('entries', [])
                ]
            )
            for race in data.get('races', [])
        ]
    )
    return fixture

if __name__ == '__main__':

    file = 'downloads/1752138913921.json'
    # file = 'downloads/sample_fofixtures_1.json'

    with open(file, 'r') as f:
        result = json.load(f)

    fixture_data: List[Dict[str, Any]] = result.get('fixtures', [])
    data = fixture_data[0]

    fixture = parse_fixture(data)

    print(fixture.model_dump())
