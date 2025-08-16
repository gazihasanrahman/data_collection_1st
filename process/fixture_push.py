import traceback
from dateutil.parser import parse
from process.helper import (
    get_tpd_meeting_id, 
    get_tpd_race_id, 
    get_tpd_runner_id, 
    get_price_id, 
    get_race_status_id, 
    calculate_price, 
)
from utils.logger import logger_1st

def process_fixture_from_push(data:dict)-> dict:
    '''
    process fixture data received from push method, which 1st pushed to our endpoint.
    '''
    race_status_history_dict = {}
    price_history_dict = {}
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
                race_number_string = race.get('number')
                race_number = int(race_number_string) if race_number_string else None
                race_runner_count = race.get('runnercount')
                race_post_time_string = race.get('posttime')
                race_post_time = parse(race_post_time_string) if race_post_time_string else None
                race_estimated_post_time_string = race.get('estimatedPosttime')
                race_estimated_post_time = parse(race_estimated_post_time_string) if race_estimated_post_time_string else None
                race_off_time_string = race.get('offTime')
                race_off_time = parse(race_off_time_string) if race_off_time_string else None
                race_weather = race.get('weather')
                race_going = race.get('going')
                race_name = race.get('name')
                race_status = race.get('status')
                track_surface_id = race.get('tracksurface', {}).get('value')
                race_overround_string = race.get('overround')
                race_overround = float(race_overround_string) if race_overround_string else None
                race_overround_selection = race.get('overround_selection')
                race_result = race.get('result')
                tpd_race_id = get_tpd_race_id(tpd_meeting_id, race_number, race_post_time)

                race_status_histories = race.get('statusHistory', [])
                for race_status_history in race_status_histories:
                    race_status_history_status = race_status_history.get('status')
                    race_status_history_timestamp_string = race_status_history.get('timestamp')
                    race_status_history_timestamp = parse(race_status_history_timestamp_string) if race_status_history_timestamp_string else None
                    race_status_id = get_race_status_id(race_id, race_status_history_timestamp)
                    race_status_history_dict[race_status_id] = {
                        'race_status_id': race_status_id,
                        'race_id': race_id,
                        'status': race_status_history_status,
                        'timestamp': race_status_history_timestamp,
                    }
                    
                entry_data = []
                entries = race.get('entries', [])
                for entry in entries:
                    entry_id = entry.get('id')
                    start_number = entry.get('startNumber')
                    program_number = entry.get('programNumber')
                    start_position = entry.get('startPosition')
                    coupled_indicator = entry.get('coupledIndicator')
                    decoupled_number = entry.get('decoupledNumber')
                    horse_id = entry.get('horse_id')
                    jockey_id = entry.get('jockey', {}).get('id')
                    entry_status = entry.get('status')
                    entry_weight_string = entry.get('weight', {}).get('value')
                    entry_weight = int(entry_weight_string) if entry_weight_string else None
                    entry_weight_unit = entry.get('weight', {}).get('unit')
                    starting_price_nominator = entry.get('startingPrice', {}).get('nominator')
                    starting_price_denominator = entry.get('startingPrice', {}).get('denominator')
                    starting_price_fraction, starting_price_percentage = calculate_price(starting_price_nominator, starting_price_denominator)
                    entry_fav_pos = entry.get('favPos')
                    entry_fav_joint = entry.get('favJoint')
                    entry_final_position_raw = entry.get('finalPosition', {}).get('position')
                    try:
                        entry_final_position = int(entry_final_position_raw)
                    except (TypeError, ValueError):
                        entry_final_position = None

                    entry_final_dead_heat = entry.get('finalPosition', {}).get('deadHeat')
                    entry_final_disqualified = entry.get('finalPosition', {}).get('disqualified')
                    entry_final_amended_position = entry.get('finalPosition', {}).get('amendedPosition')
                    tpd_runner_id = get_tpd_runner_id(tpd_race_id, program_number)

                    show_prices = entry.get('showPrices', [])
                    for show_price in show_prices:
                        show_price_timestamp = show_price.get('timestamp')
                        show_price_numerator = show_price.get('numerator')
                        show_price_denominator = show_price.get('denominator')
                        show_price_market = show_price.get('market')
                        show_price_fraction, show_price_percentage = calculate_price(show_price_numerator, show_price_denominator)
                        price_id = get_price_id(entry_id, show_price_timestamp)
                        price_history_dict[price_id] = {
                            'price_id': price_id,
                            'entry_id': entry_id,
                            'timestamp': show_price_timestamp,
                            'price_fraction': show_price_fraction,
                            'price_percentage': show_price_percentage,
                            'market': show_price_market,
                        }

                    entry_data.append({
                        'entry_id': entry_id,
                        'race_id': race_id,
                        'start_number': start_number,
                        'program_number': program_number,
                        'start_position': start_position,
                        'coupled_indicator': coupled_indicator,
                        'decoupled_number': decoupled_number,
                        'horse_id': horse_id,
                        'entry_status': entry_status,
                        'weight': entry_weight,
                        'weight_unit': entry_weight_unit,
                        'jockey_id': jockey_id,
                        'starting_price_fraction': starting_price_fraction,
                        'starting_price_percentage': starting_price_percentage,
                        'fav_pos': entry_fav_pos,
                        'fav_joint': entry_fav_joint,
                        'final_position': entry_final_position,
                        'dead_heat': entry_final_dead_heat,
                        'disqualified': entry_final_disqualified,
                        'amended_position': entry_final_amended_position,
                        'tpd_runner_id': tpd_runner_id,
                    })

                race_data.append({
                    'race_id': race_id,
                    'fixture_id': fixture_id,
                    'race_number': race_number,
                    'runner_count': race_runner_count,
                    'post_time': race_post_time,
                    'estimated_post_time': race_estimated_post_time,
                    'off_time': race_off_time,
                    'weather': race_weather,
                    'going': race_going,
                    'race_name': race_name,
                    'race_status': race_status,
                    'overround': race_overround,
                    'overround_selection': race_overround_selection,
                    'race_result': race_result,
                    'surface_id': track_surface_id,
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
        logger_1st.error(f'process_fixture_from_push(): {e}')
        logger_1st.error(traceback.format_exc())

    return {
        'fixtures': fixture_data,
        'race_status_history_dict': race_status_history_dict,
        'price_history_dict': price_history_dict,
    }

