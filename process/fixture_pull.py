import traceback
from dateutil.parser import parse
from process.helper import get_tpd_meeting_id, get_tpd_race_id, get_tpd_runner_id
from utils.logger import logger_1st



def process_fixture_from_pull(data: dict) -> dict:
    '''
    process fixture data received from pull method, which we pull from 1st's API.
    '''
    horse_dict = {}
    jockey_dict = {}
    trainer_dict = {}
    owner_dict = {}
    fixture_data = []
    try:
        fixtures = data.get('fixtures', [])
        for fixture in fixtures:
            fixture_header = fixture.get('header', {})
            fixture_id = fixture_header.get('id')
            fixture_date_string = fixture_header.get('date')
            fixture_date = parse(fixture_date_string).date() if fixture_date_string else None
            fixture_first_post_time_string = fixture_header.get('firstposttime')
            fixture_first_post_time = parse(fixture_first_post_time_string) if fixture_first_post_time_string else None
            fixture_race_count = fixture_header.get('racecount')
            fixture_temperature_fahrenheit = fixture_header.get('temperature', {}).get('fahrenheit')
            fixture_temperature_celsius = fixture_header.get('temperature', {}).get('celsius')
            track_id = fixture.get('track', {}).get('id')
            tpd_meeting_id = get_tpd_meeting_id(track_id, fixture_date)

            race_data = []
            races = fixture.get('races', [])
            for race in races:
                race_id = race.get('id')
                track_type = race.get('type') # NOTE: NEW
                race_number_string = race.get('number')
                race_number = int(race_number_string) if race_number_string else None
                race_runner_count = race.get('runnercount')
                race_post_time_string = race.get('posttime')
                race_post_time = parse(race_post_time_string) if race_post_time_string else None
                race_estimated_post_time_string = race.get('estimatedposttime')
                race_estimated_post_time = parse(race_estimated_post_time_string) if race_estimated_post_time_string else None
                race_status = race.get('status')
                isdst = race.get('isdst')
                timezone_offset = race.get('timezoneOffset')
                race_weather = race.get('weather')
                race_going = race.get('going')
                race_name = race.get('name')
                race_comment = race.get('comment')
                race_distance_string = race.get('distance', {}).get('value')
                race_distance = int(race_distance_string) if race_distance_string else None
                race_distance_unit = race.get('distance', {}).get('unit')
                race_distance_text = race.get('distance', {}).get('publishedText')
                race_breed = race.get('breed')
                racetype_id = race.get('racetype', {}).get('type')
                racetype_subtype = race.get('racetype', {}).get('subtype')
                track_surface_id = race.get('tracksurface', {}).get('value')
                sex_restriction_id = race.get('sexrestriction', {}).get('value')
                age_restriction_id = race.get('agerestriction', {}).get('value')
                purse_string = race.get('purse', {}).get('value')
                purse = int(purse_string) if purse_string else None
                purse_ranks = race.get('purse', {}).get('ranks')
                purse_unit = race.get('purse', {}).get('unit')
                race_grade = race.get('grade')
                race_tip = race.get('raceTip')
                tpd_race_id = get_tpd_race_id(tpd_meeting_id, race_number, race_post_time)

                entry_data = []
                entries = race.get('entries', [])
                for entry in entries:
                    entry_id = entry.get('id')
                    start_number = entry.get('startNumber')
                    program_number = entry.get('programNumber')
                    start_position = entry.get('startPosition')
                    coupled_indicator = entry.get('coupledIndicator')
                    decoupled_number = entry.get('decoupledNumber')
                    scratch_indicator = entry.get('scratchIndicator')
                    entry_age = entry.get('age')
                    entry_weight_string = entry.get('weight', {}).get('value')
                    entry_weight = int(entry_weight_string) if entry_weight_string else None
                    entry_weight_unit = entry.get('weight', {}).get('unit')
                    horse_id = entry.get('horse_id')
                    jockey_id = entry.get('jockey', {}).get('id')
                    trainer_id = entry.get('trainer', {}).get('id')
                    owner_id = entry.get('owner', {}).get('id')
                    breeder_name = entry.get('breeder')
                    runner_tip = entry.get('runnerTip')
                    tpd_runner_id = get_tpd_runner_id(tpd_race_id, program_number)

                    # Only add to horse_dict if horse_id is valid
                    if is_valid_id(horse_id):
                        horse_dict[horse_id] = {
                            'horse_id': horse_id,
                        }

                    # Only add to jockey_dict if jockey_id is valid
                    if is_valid_id(jockey_id):
                        jockey_dict[jockey_id] = {
                            'jockey_id': jockey_id,
                            'jockey_name': entry.get('jockey', {}).get('name'),
                            'old_jockey_id': entry.get('jockey', {}).get('oldJockeyID'),
                            'old_jockey_name': entry.get('jockey', {}).get('oldJockeyName'),
                        }

                    # Only add to trainer_dict if trainer_id is valid
                    if is_valid_id(trainer_id):
                        trainer_dict[trainer_id] = {
                            'trainer_id': trainer_id,
                            'trainer_name': entry.get('trainer', {}).get('name'),
                        }

                    # Only add to owner_dict if owner_id is valid
                    if is_valid_id(owner_id):
                        owner_dict[owner_id] = {
                            'owner_id': owner_id,
                            'owner_name': entry.get('owner', {}).get('name'),
                        }

                    entry_data.append({
                        'entry_id': entry_id,
                        'race_id': race_id,
                        'start_number': start_number,
                        'program_number': program_number,
                        'start_position': start_position,
                        'coupled_indicator': coupled_indicator,
                        'decoupled_number': decoupled_number,
                        'scratch_indicator': scratch_indicator,
                        'age': entry_age,
                        'weight': entry_weight,
                        'weight_unit': entry_weight_unit,
                        'horse_id': horse_id,
                        'jockey_id': jockey_id,
                        'trainer_id': trainer_id,
                        'owner_id': owner_id,
                        'breeder_name': breeder_name,
                        'runner_tip': runner_tip,
                        'tpd_runner_id': tpd_runner_id,
                    })

                race_data.append({
                    'race_id': race_id,
                    'fixture_id': fixture_id,
                    'track_type': track_type,
                    'race_number': race_number,
                    'runner_count': race_runner_count,
                    'post_time': race_post_time,
                    'estimated_post_time': race_estimated_post_time,
                    'race_status': race_status,
                    'isdst': isdst,
                    'timezone_offset': timezone_offset,
                    'weather': race_weather,
                    'going': race_going,
                    'surface_id': track_surface_id,
                    'grade': race_grade,
                    'distance': race_distance,
                    'distance_unit': race_distance_unit,
                    'distance_text': race_distance_text,
                    'race_breed': race_breed,
                    'racetype_id': racetype_id,
                    'racetype_subtype': racetype_subtype,
                    'sex_restriction_id': sex_restriction_id,
                    'age_restriction_id': age_restriction_id,
                    'purse': purse,
                    'purse_ranks': purse_ranks,
                    'purse_unit': purse_unit,
                    'race_name': race_name,
                    'race_comment': race_comment,
                    'race_tip': race_tip,
                    'tpd_race_id': tpd_race_id,
                    'entry_data': entry_data,
                })

            fixture_data.append({
                'fixture_id': fixture_id,
                'fixture_date': fixture_date,
                'first_post_time': fixture_first_post_time,
                'race_count': fixture_race_count,
                'temperature_fahrenheit': fixture_temperature_fahrenheit,
                'temperature_celsius': fixture_temperature_celsius,
                'track_id': track_id,
                'tpd_meeting_id': tpd_meeting_id,
                'race_data': race_data,
            })

    except Exception as e:
        logger_1st.error(f'process_fixture_from_pull(): {e}')
        logger_1st.error(traceback.format_exc())

    return {
        'fixtures': fixture_data,
        'horse_dict': horse_dict,
        'jockey_dict': jockey_dict,
        'trainer_dict': trainer_dict,
        'owner_dict': owner_dict,
    }


def is_valid_id(id_value):
    try:
        if id_value is None:
            return False
        if id_value == 0:
            return False
        if isinstance(id_value, str):
            if not id_value.strip():
                return False
        return True
    except Exception as e:
        logger_1st.error(f'is_valid_id(): {e}')
        logger_1st.error(traceback.format_exc())
        return False



