import json
import glob
import pandas as pd
from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from typing import List, Optional, Union, Dict, Any
from x_models_pd import Fixture, Race, Entry
import x_models_pd as etl


class FixtureDataTransformer:
    """Transforms raw JSON data to match Pydantic model structure."""
    
    @staticmethod
    def transform_fixture(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw fixture data to match our Pydantic model structure."""
        header = data.get('header', {})
        track_data = data.get('track', {})
        
        return {
            'fixture_id': header.get('id'),
            'fixture_date': header.get('date'),
            'firstposttime': header.get('firstposttime'),
            'racecount': header.get('racecount'),
            'temperature_fahrenheit': header.get('temperature', {}).get('fahrenheit'),
            'temperature_celsius': header.get('temperature', {}).get('celsius'),
            'track': FixtureDataTransformer.transform_track(track_data),
            'races': [FixtureDataTransformer.transform_race(race) for race in data.get('races', [])]
        }
    
    @staticmethod
    def transform_track(track_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform track data."""
        return {
            'track_id': track_data.get('id'),
            'track_name': track_data.get('name'),
            'countryid': track_data.get('countryid'),
            'countryName': track_data.get('countryName'),
            'timezone': track_data.get('timezone'),
            'code': track_data.get('code'),
            'trackType': track_data.get('trackType')
        }
    
    @staticmethod
    def transform_race(race_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform race data."""
        return {
            'race_id': race_data.get('id'),
            'race_number': race_data.get('number'),
            'race_name': race_data.get('name'),
            'runnercount': race_data.get('runnercount'),
            'posttime': race_data.get('posttime'),
            'estimatedPosttime': race_data.get('estimatedPosttime'),
            'offTime': race_data.get('offTime'),
            'weather': race_data.get('weather'),
            'going': race_data.get('going'),
            'status': race_data.get('status'),
            'tracksurface': race_data.get('tracksurface', {}).get('value'),
            'overround': race_data.get('overround'),
            'overround_selection': race_data.get('overround_selection'),
            'comment': race_data.get('comment'),
            'distance': race_data.get('distance', {}).get('value'),
            'distance_unit': race_data.get('distance', {}).get('unit'),
            'distance_text': race_data.get('distance', {}).get('publishedText'),
            'breed': race_data.get('breed'),
            'racetype_type': race_data.get('racetype', {}).get('type'),
            'racetype_subtype': race_data.get('racetype', {}).get('subtype'),
            'racetype_description': race_data.get('racetype', {}).get('description'),
            'agerestriction': race_data.get('agerestriction', {}).get('value'),
            'agerestriction_description': race_data.get('agerestriction', {}).get('description'),
            'purse': race_data.get('purse', {}).get('value'),
            'purse_unit': race_data.get('purse', {}).get('unit'),
            'grade': race_data.get('grade'),
            'raceTip': race_data.get('raceTip'),
            'statusHistory': [FixtureDataTransformer.transform_status_history(status) 
                            for status in race_data.get('statusHistory', [])],
            'entries': [FixtureDataTransformer.transform_entry(entry) 
                       for entry in race_data.get('entries', [])]
        }
    
    @staticmethod
    def transform_status_history(status_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform status history data."""
        return {
            'status': status_data.get('status'),
            'timestamp': status_data.get('timestamp')
        }
    
    @staticmethod
    def transform_entry(entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform entry data."""
        horse_data = entry_data.get('horse', {})
        jockey_data = entry_data.get('jockey', {})
        owner_data = entry_data.get('owner', {})
        trainer_data = entry_data.get('trainer', {})
        final_position = entry_data.get('finalPosition', {})
        starting_price = entry_data.get('startingPrice', {})
        weight_data = entry_data.get('weight', {})
        
        return {
            'entry_id': entry_data.get('id'),
            'programNumber': entry_data.get('programNumber'),
            'startNumber': entry_data.get('startNumber'),
            'startPosition': entry_data.get('startPosition'),
            'coupledIndicator': entry_data.get('coupledIndicator'),
            'decoupledNumber': entry_data.get('decoupledNumber'),
            'horse_id': horse_data.get('id'),
            'age': horse_data.get('age'),
            'saddleclothcolor': horse_data.get('saddleclothcolor'),
            'status_id': entry_data.get('status'),
            'weight': weight_data.get('value'),
            'weight_unit': weight_data.get('unit'),
            'breeder': horse_data.get('breeder'),
            'owner_id': owner_data.get('id'),
            'owner_name': owner_data.get('name'),
            'trainer_id': trainer_data.get('id'),
            'trainer_name': trainer_data.get('name'),
            'jockey_id': jockey_data.get('id'),
            'jockey_name': jockey_data.get('name'),
            'position': final_position.get('position'),
            'deadHeat': final_position.get('deadHeat'),
            'disqualified': final_position.get('disqualified'),
            'amendedPosition': final_position.get('amendedPosition'),
            'starting_price_nominator': starting_price.get('nominator'),
            'starting_price_denominator': starting_price.get('denominator'),
            'runnerTip': entry_data.get('runnerTip'),
            'price_history': [FixtureDataTransformer.transform_price_history(price) 
                             for price in entry_data.get('showPrices', [])]
        }
    
    @staticmethod
    def transform_price_history(price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform price history data."""
        return {
            'timestamp': price_data.get('timestamp'),
            'numerator': price_data.get('nominator'),
            'denominator': price_data.get('denominator'),
            'market': price_data.get('market')
        }


def parse_fixture(data: Dict[str, Any]) -> etl.Fixture:
    """Parse fixture data using Pydantic's model_validate for better validation and error handling."""
    try:
        # Transform the data structure to match our Pydantic models
        transformed_data = FixtureDataTransformer.transform_fixture(data)
        
        # Use Pydantic's model_validate for automatic validation and type conversion
        return etl.Fixture.model_validate(transformed_data)
    
    except Exception as e:
        print(f"Error parsing fixture: {e}")
        raise


# Alternative approach using direct model_validate (if data structure matches exactly)
def parse_fixture_direct(data: Dict[str, Any]) -> etl.Fixture:
    """Alternative approach if your JSON structure matches your Pydantic models exactly."""
    try:
        return etl.Fixture.model_validate(data)
    except Exception as e:
        print(f"Error with direct validation: {e}")
        # Fall back to manual parsing
        return parse_fixture(data)


if __name__ == '__main__':

    file = 'downloads/1752138913921.json'
    # file = 'downloads/sample_fofixtures_1.json'

    with open(file, 'r') as f:
        result = json.load(f)

    fixture_data: List[Dict[str, Any]] = result.get('fixtures', [])
    data = fixture_data[0]

    fixture = parse_fixture(data)

    print(fixture.model_dump())



