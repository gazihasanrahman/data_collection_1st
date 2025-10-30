from datetime import datetime, date
import hashlib
from utils.logger import logger_1st
import traceback
from database.general import session_scope, FirstTrack, FirstFixture, FirstRace, FirstEntry, MapCourse, MapMeeting, MapRace, MapRunner


def get_price_id(entry_id: int, timestamp: datetime, sha_length: int = 16) -> str:
    return hashlib.sha256(f'{entry_id}{timestamp}'.encode()).hexdigest()[:sha_length]


def get_race_status_id(race_id: int, timestamp: datetime, sha_length: int = 16) -> str:
    return hashlib.sha256(f'{race_id}{timestamp}'.encode()).hexdigest()[:sha_length]


def manually_map_all_tpd_ids():
    unmapped_fixture_ids = get_unmapped_fixture_ids()
    logger_1st.info(f'unmapped_fixture_ids: {unmapped_fixture_ids}')
    if unmapped_fixture_ids:
        for fixture_id in unmapped_fixture_ids:
            manually_map_tpd_meeting_id(fixture_id)

    unmapped_race_ids = get_unmapped_race_ids()
    logger_1st.info(f'unmapped_race_ids: {unmapped_race_ids}')
    if unmapped_race_ids:
        for race_id in unmapped_race_ids:
            manually_map_tpd_race_id(race_id)

    unmapped_entry_ids = get_unmapped_entry_ids()
    logger_1st.info(f'unmapped_entry_ids: {unmapped_entry_ids}')
    if unmapped_entry_ids:
        for entry_id in unmapped_entry_ids:
            manually_map_tpd_runner_id(entry_id)


def get_unmapped_fixture_ids():
    list_of_fixture_ids = []
    with session_scope() as session:
        unmapped_fixtures = session.query(FirstFixture).filter(FirstFixture.tpd_meeting_id == None).all()
        if unmapped_fixtures:
            for fixture in unmapped_fixtures:
                list_of_fixture_ids.append(fixture.fixture_id)
    return list_of_fixture_ids

def get_unmapped_race_ids():
    list_of_race_ids = []   
    with session_scope() as session:
        unmapped_races = session.query(FirstRace).filter(FirstRace.tpd_race_id == None).all()
        if unmapped_races:
            for race in unmapped_races:
                list_of_race_ids.append(race.race_id)
    return list_of_race_ids

def get_unmapped_entry_ids():
    list_of_entry_ids = []
    with session_scope() as session:
        unmapped_entries = session.query(FirstEntry).filter(FirstEntry.tpd_runner_id == None).all()
        if unmapped_entries:
            for entry in unmapped_entries:
                list_of_entry_ids.append(entry.entry_id)
    return list_of_entry_ids


def manually_map_tpd_meeting_id(first_fixture_id :str) -> int:
    try:
        if first_fixture_id is None:
            logger_1st.error(f'manually_map_tpd_meeting_id(): first_fixture_id is None')
            return None
        with session_scope() as session:
            existing_fixture = session.query(FirstFixture).filter(FirstFixture.fixture_id == first_fixture_id).first()
            if existing_fixture:
                track_id = existing_fixture.track_id
                fixture_date = existing_fixture.fixture_date
            else:
                logger_1st.error(f'manually_map_tpd_meeting_id(): no tpd_meeting_id for first_fixture_id: {first_fixture_id}')
                return None

        tpd_meeting_id = get_tpd_meeting_id(track_id = track_id, fixture_date = fixture_date)
        if not tpd_meeting_id:
            return None

        with session_scope() as session:
            existing_fixture = session.query(FirstFixture).filter(FirstFixture.fixture_id == first_fixture_id).first()
            if existing_fixture:
                existing_fixture.tpd_meeting_id = tpd_meeting_id
                session.commit()
                logger_1st.info(f'manually mapped tpd_meeting_id: {tpd_meeting_id} for first_fixture_id: {first_fixture_id}')
    except Exception as e:
        logger_1st.error(f'manually_map_tpd_meeting_id(): first_fixture_id: {first_fixture_id}')
        logger_1st.error(traceback.format_exc())


def manually_map_tpd_race_id(first_race_id :str) -> int:
    try:
        if first_race_id is None:
            logger_1st.error(f'manually_map_tpd_race_id(): first_race_id is None')
            return None
        with session_scope() as session:
            existing_race = session.query(
                FirstFixture.tpd_meeting_id,
                FirstRace.race_number,
                FirstRace.post_time
            ).outerjoin(
                FirstRace, FirstFixture.fixture_id == FirstRace.fixture_id).filter(
                    FirstRace.race_id == first_race_id).first()
            if existing_race:
                tpd_meeting_id =  existing_race.tpd_meeting_id
                race_number = existing_race.race_number
                post_time = existing_race.post_time
            else:
                logger_1st.error(f'manually_map_tpd_race_id(): no tpd_meeting_id for first_race_id: {first_race_id}')
                return None

        tpd_race_id = get_tpd_race_id(tpd_meeting_id = tpd_meeting_id, race_number = race_number, post_time = post_time)
        if not tpd_race_id:
            return None
        
        with session_scope() as session:
            existing_race = session.query(FirstRace).filter(FirstRace.race_id == first_race_id).first()
            if existing_race:
                existing_race.tpd_race_id = tpd_race_id
                session.commit()
                logger_1st.info(f'manually mapped tpd_race_id: {tpd_race_id} for first_race_id: {first_race_id}')
    except Exception as e:
        logger_1st.error(f'manually_map_tpd_race_id(): first_race_id: {first_race_id}')
        logger_1st.error(traceback.format_exc())


def manually_map_tpd_runner_id(first_entry_id :str) -> int:
    try:
        if first_entry_id is None:
            logger_1st.error(f'manually_map_tpd_runner_id(): first_entry_id is None')
            return None
        with session_scope() as session:
            existing_entry = session.query(
                FirstRace.tpd_race_id,
                FirstEntry.program_number
            ).outerjoin(
                FirstRace, FirstEntry.race_id == FirstRace.race_id).filter(
                        FirstEntry.entry_id == first_entry_id).first()
            if existing_entry:
                tpd_race_id = existing_entry.tpd_race_id
                program_number = existing_entry.program_number
            else:
                logger_1st.error(f'manually_map_tpd_runner_id(): no tpd_race_id for first_entry_id: {first_entry_id}')
                return None

        tpd_runner_id = get_tpd_runner_id(tpd_race_id = tpd_race_id, program_number = program_number)
        if not tpd_runner_id:
            return None

        with session_scope() as session:
            existing_entry = session.query(FirstEntry).filter(FirstEntry.entry_id == first_entry_id).first()
            if existing_entry:
                existing_entry.tpd_runner_id = tpd_runner_id
                session.commit()
                logger_1st.info(f'manually mapped tpd_runner_id: {tpd_runner_id} for first_entry_id: {first_entry_id}')
    except Exception as e:
        logger_1st.error(f'manually_map_tpd_runner_id(): first_entry_id: {first_entry_id}')
        logger_1st.error(traceback.format_exc())


def get_tpd_meeting_id(track_id :str, fixture_date :date) -> int:
    track_id = str(track_id).strip()
    track_id = None if track_id == '' else track_id
    if track_id is None or fixture_date is None:
        logger_1st.error(f'get_tpd_meeting_id(): track_id: {track_id}, fixture_date: {fixture_date} is not valid')
        return None

    tpd_meeting_id = None
    try:
        with session_scope() as session:
            result = session.query(FirstTrack.tpd_course_id).filter(FirstTrack.track_id == track_id).first()
            if result:
                tpd_course_id = result.tpd_course_id
            else:
                tpd_course_id = None
                logger_1st.error(f'get_tpd_meeting_id(): track_id: {track_id} not found in first_track table')
        if tpd_course_id is None:
            logger_1st.error(f'get_tpd_meeting_id(): track_id: {track_id} is not mapped')
            return None

        with session_scope() as session:
            existing_meeting = session.query(MapMeeting.id).filter(
                MapMeeting.map_course_code == tpd_course_id, 
                MapMeeting.date == fixture_date).first()
            if existing_meeting:
                tpd_meeting_id = existing_meeting.id
            else:
                new_meeting = MapMeeting(
                    map_course_code = tpd_course_id,
                    date = fixture_date,
                )
                session.add(new_meeting)
                session.flush()
                session.refresh(new_meeting)
                session.commit()
                tpd_meeting_id = new_meeting.id
    except Exception as e:
        logger_1st.error(f'get_tpd_meeting_id(): track_id: {track_id}, fixture_date: {fixture_date}')
        logger_1st.error(traceback.format_exc())
    return tpd_meeting_id


def get_tpd_race_id(tpd_meeting_id :int, race_number :int, post_time :datetime) -> int | None:
    if tpd_meeting_id is None or race_number is None or post_time is None:
        logger_1st.error(f'get_tpd_race_id(): tpd_meeting_id: {tpd_meeting_id}, race_number: {race_number}, post_time: {post_time} is not valid')
        return None
    tpd_race_id = None
    try:
        with session_scope() as session:
            existing_race = session.query(MapRace.id).filter(
                MapRace.map_meeting_id == tpd_meeting_id,
                MapRace.race_number == race_number).first()
            if existing_race:
                tpd_race_id = existing_race.id
            else:
                new_race = MapRace(
                    map_meeting_id = tpd_meeting_id,
                    race_number = race_number,
                    post_time = post_time,
                )
                session.add(new_race)
                session.flush()
                session.refresh(new_race)
                session.commit()
                tpd_race_id = new_race.id
    except Exception as e:
        logger_1st.error(f'get_tpd_race_id(): tpd_meeting_id: {tpd_meeting_id}, race_number: {race_number}, post_time: {post_time}')
        logger_1st.error(traceback.format_exc())
    return tpd_race_id


def get_tpd_runner_id(tpd_race_id :int, program_number :str) -> int:
    program_number = str(program_number).strip() if program_number is not None else None
    program_number = None if program_number == '' else program_number
    if tpd_race_id is None or program_number is None:
        logger_1st.error(f'get_tpd_runner_id(): tpd_race_id: {tpd_race_id}, program_number: {program_number} is not valid')
        return None
    tpd_runner_id = None
    try:
        with session_scope() as session:
            existing_runner = session.query(MapRunner.id).filter(
                MapRunner.map_race_id == tpd_race_id,
                MapRunner.runner_number == program_number).first()
            if existing_runner:
                tpd_runner_id = existing_runner.id
            else:
                new_runner = MapRunner(
                    map_race_id = tpd_race_id,
                    runner_number = program_number,
                )
                session.add(new_runner)
                session.flush()
                session.refresh(new_runner)
                session.commit()
                tpd_runner_id = new_runner.id
    except Exception as e:
        logger_1st.error(f'get_tpd_runner_id(): tpd_race_id: {tpd_race_id}, program_number: {program_number}')
        logger_1st.error(traceback.format_exc())
    return tpd_runner_id





