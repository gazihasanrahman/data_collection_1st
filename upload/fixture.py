import traceback
from database.general import session_scope, FirstFixture, FirstRace, FirstEntry
from utils.logger import logger_1st



def upload_fixture_data(fixture: dict, overwrite: bool = False):
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
                        existing_race.track_type = race.get('track_type')
                        existing_race.race_number = race.get('race_number')
                        existing_race.runner_count = race.get('runner_count')
                        existing_race.post_time = race.get('post_time')
                        existing_race.estimated_post_time = race.get('estimated_post_time')
                        existing_race.race_status = race.get('race_status')
                        existing_race.isdst = race.get('isdst')
                        existing_race.timezone_offset = race.get('timezone_offset')
                        existing_race.weather = race.get('weather')
                        existing_race.going = race.get('going')
                        existing_race.surface_id = race.get('surface_id')
                        existing_race.grade = race.get('grade')
                        existing_race.distance = race.get('distance')
                        existing_race.distance_unit = race.get('distance_unit')
                        existing_race.distance_text = race.get('distance_text')
                        existing_race.race_breed = race.get('race_breed')
                        existing_race.racetype_id = race.get('racetype_id')
                        existing_race.racetype_subtype = race.get('racetype_subtype')
                        existing_race.sex_restriction_id = race.get('sex_restriction_id')
                        existing_race.age_restriction_id = race.get('age_restriction_id')
                        existing_race.purse = race.get('purse')
                        existing_race.purse_ranks = race.get('purse_ranks')
                        existing_race.purse_unit = race.get('purse_unit')
                        existing_race.race_name = race.get('race_name')
                        existing_race.race_comment = race.get('race_comment')
                        existing_race.race_tip = race.get('race_tip')
                        existing_race.tpd_race_id = race.get('tpd_race_id')
                else:
                    new_race = FirstRace(
                        race_id = race.get('race_id'),
                        fixture_id = race.get('fixture_id'),
                        track_type = race.get('track_type'),
                        race_number = race.get('race_number'),
                        runner_count = race.get('runner_count'),
                        post_time = race.get('post_time'),
                        estimated_post_time = race.get('estimated_post_time'),
                        race_status = race.get('race_status'),
                        isdst = race.get('isdst'),
                        timezone_offset = race.get('timezone_offset'),
                        weather = race.get('weather'),
                        going = race.get('going'),
                        surface_id = race.get('surface_id'),
                        grade = race.get('grade'),
                        distance = race.get('distance'),
                        distance_unit = race.get('distance_unit'),
                        distance_text = race.get('distance_text'),
                        race_breed = race.get('race_breed'),
                        racetype_id = race.get('racetype_id'),
                        racetype_subtype = race.get('racetype_subtype'),
                        sex_restriction_id = race.get('sex_restriction_id'),
                        age_restriction_id = race.get('age_restriction_id'),
                        purse = race.get('purse'),
                        purse_ranks = race.get('purse_ranks'),
                        purse_unit = race.get('purse_unit'),
                        race_name = race.get('race_name'),
                        race_comment = race.get('race_comment'),
                        race_tip = race.get('race_tip'),
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
                        existing_entry.scratch_indicator = entry.get('scratch_indicator')
                        existing_entry.age = entry.get('age')
                        existing_entry.weight = entry.get('weight')
                        existing_entry.weight_unit = entry.get('weight_unit')
                        existing_entry.horse_id = entry.get('horse_id')
                        existing_entry.jockey_id = entry.get('jockey_id')
                        existing_entry.trainer_id = entry.get('trainer_id')
                        existing_entry.owner_id = entry.get('owner_id')
                        existing_entry.breeder_name = entry.get('breeder_name')
                        existing_entry.runner_tip = entry.get('runner_tip')
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
                        scratch_indicator = entry.get('scratch_indicator'),
                        age = entry.get('age'),
                        weight = entry.get('weight'),
                        weight_unit = entry.get('weight_unit'),
                        horse_id = entry.get('horse_id'),
                        jockey_id = entry.get('jockey_id'),
                        trainer_id = entry.get('trainer_id'),
                        owner_id = entry.get('owner_id'),
                        breeder_name = entry.get('breeder_name'),
                        runner_tip = entry.get('runner_tip'),
                        tpd_runner_id = entry.get('tpd_runner_id'),
                    )
                    session.add(new_entry)

        return True
    except Exception as e:
        logger_1st.error(f'upload_fixture_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    




