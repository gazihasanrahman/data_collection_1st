import traceback
from database.general import session_scope, FirstFixture, FirstRace, FirstEntry
from utils.logger import logger_1st


def upload_fixture_from_push(fixture: dict, overwrite: bool = False):
    '''
    upload fixture data received from push method, which 1st pushed to our endpoint.
    '''
    try:
        with session_scope() as session:
            existing_fixture = session.query(FirstFixture).filter(FirstFixture.fixture_id == fixture['fixture_id']).first()
            if existing_fixture:
                if overwrite:
                    existing_fixture.fixture_date = fixture.get('fixture_date')
                    existing_fixture.first_post_time = fixture.get('first_post_time')
                    existing_fixture.race_count = fixture.get('race_count')
                    existing_fixture.temperature_fahrenheit = fixture.get('temperature_fahrenheit')
                    existing_fixture.temperature_celsius = fixture.get('temperature_celsius')
                    existing_fixture.track_id = fixture.get('track_id')
                    existing_fixture.tpd_meeting_id = fixture.get('tpd_meeting_id')
            else:
                new_fixture = FirstFixture(
                    fixture_id = fixture.get('fixture_id'),
                    fixture_date = fixture.get('fixture_date'),
                    first_post_time = fixture.get('first_post_time'),
                    race_count = fixture.get('race_count'),
                    temperature_fahrenheit = fixture.get('temperature_fahrenheit'),
                    temperature_celsius = fixture.get('temperature_celsius'),
                    track_id = fixture.get('track_id'),
                    tpd_meeting_id = fixture.get('tpd_meeting_id'),
                )
                session.add(new_fixture)

        races = fixture.get('race_data', [])
        for race in races:
            with session_scope() as session:
                existing_race = session.query(FirstRace).filter(FirstRace.race_id == race['race_id']).first()
                if existing_race:
                    if overwrite:
                        existing_race.fixture_id = race.get('fixture_id')
                        existing_race.race_number = race.get('race_number')
                        existing_race.runner_count = race.get('runner_count')
                        existing_race.post_time = race.get('post_time')
                        existing_race.estimated_post_time = race.get('estimated_post_time')
                        existing_race.off_time = race.get('off_time')
                        existing_race.weather = race.get('weather')
                        existing_race.going = race.get('going')
                        existing_race.race_name = race.get('race_name')
                        existing_race.race_status = race.get('race_status')
                        existing_race.overround = race.get('overround')
                        existing_race.overround_selection = race.get('overround_selection')
                        existing_race.race_result = race.get('race_result')
                        existing_race.surface_id = race.get('surface_id')
                        existing_race.tpd_race_id = race.get('tpd_race_id')
                else:
                    new_race = FirstRace(
                        race_id = race.get('race_id'),
                        fixture_id = race.get('fixture_id'),
                        race_number = race.get('race_number'),
                        runner_count = race.get('runner_count'),
                        post_time = race.get('post_time'),
                        estimated_post_time = race.get('estimated_post_time'),
                        off_time = race.get('off_time'),
                        weather = race.get('weather'),
                        going = race.get('going'),
                        race_name = race.get('race_name'),
                        race_status = race.get('race_status'),
                        overround = race.get('overround'),
                        overround_selection = race.get('overround_selection'),
                        race_result = race.get('race_result'),
                        surface_id = race.get('surface_id'),
                        tpd_race_id = race.get('tpd_race_id'),
                    )
                    session.add(new_race)
            
            

            entries = race.get('entry_data', [])
            for entry in entries:
                with session_scope() as session:
                    existing_entry = session.query(FirstEntry).filter(FirstEntry.entry_id == entry['entry_id']).first()
                    if existing_entry:
                        if overwrite:
                            existing_entry.race_id = entry.get('race_id')
                            existing_entry.start_number = entry.get('start_number')
                            existing_entry.program_number = entry.get('program_number')
                            existing_entry.start_position = entry.get('start_position')
                            existing_entry.coupled_indicator = entry.get('coupled_indicator')
                            existing_entry.decoupled_number = entry.get('decoupled_number')
                            existing_entry.horse_id = entry.get('horse_id')
                            existing_entry.entry_status = entry.get('entry_status')
                            existing_entry.weight = entry.get('weight')
                            existing_entry.weight_unit = entry.get('weight_unit')
                            existing_entry.jockey_id = entry.get('jockey_id')
                            existing_entry.starting_price_nominator = entry.get('starting_price_nominator')
                            existing_entry.starting_price_denominator = entry.get('starting_price_denominator')
                            existing_entry.fav_pos = entry.get('fav_pos')
                            existing_entry.fav_joint = entry.get('fav_joint')
                            existing_entry.final_position = entry.get('final_position')
                            existing_entry.dead_heat = entry.get('dead_heat')
                            existing_entry.disqualified = entry.get('disqualified')
                            existing_entry.amended_position = entry.get('amended_position')
                            existing_entry.tpd_runner_id = entry.get('tpd_runner_id')
                    else:
                        new_entry = FirstEntry(
                            entry_id = entry.get('entry_id'),
                            race_id = entry.get('race_id'),
                            start_number = entry.get('start_number'),
                            program_number = entry.get('program_number'),
                            start_position = entry.get('start_position'),
                            coupled_indicator = entry.get('coupled_indicator'),
                            decoupled_number = entry.get('decoupled_number'),
                            horse_id = entry.get('horse_id'),
                            entry_status = entry.get('entry_status'),
                            weight = entry.get('weight'),
                            weight_unit = entry.get('weight_unit'),
                            jockey_id = entry.get('jockey_id'),
                            starting_price_nominator = entry.get('starting_price_nominator'),
                            starting_price_denominator = entry.get('starting_price_denominator'),
                            fav_pos = entry.get('fav_pos'),
                            fav_joint = entry.get('fav_joint'),
                            final_position = entry.get('final_position'),
                            dead_heat = entry.get('dead_heat'),
                            disqualified = entry.get('disqualified'),
                            amended_position = entry.get('amended_position'),
                            tpd_runner_id = entry.get('tpd_runner_id'),
                        )
                        session.add(new_entry)
            
            logger_1st.info(f'uploaded: race_id - {race.get("race_id")}')

        return True
    except Exception as e:
        logger_1st.error(f'upload_fixture_from_push(): fixture_id: {fixture.get("fixture_id")}')
        logger_1st.error(traceback.format_exc())
        return False
    