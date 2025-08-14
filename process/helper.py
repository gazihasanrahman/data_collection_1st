from datetime import datetime, date
import hashlib
from utils.logger import logger_1st
import traceback
from database.general import session_scope, FirstTrack, FirstFixture, FirstRace, FirstEntry, MapCourse, MapMeeting, MapRace, MapRunner


def get_price_id(entry_id: int, timestamp: datetime, sha_length: int = 16) -> str:
    return hashlib.sha256(f'{entry_id}{timestamp}'.encode()).hexdigest()[:sha_length]


def get_race_status_id(race_id: int, timestamp: datetime, sha_length: int = 16) -> str:
    return hashlib.sha256(f'{race_id}{timestamp}'.encode()).hexdigest()[:sha_length]


def get_tpd_meeting_id(track_id :str, fixture_date :date) -> int:
    tpd_meeting_id = None
    try:
        track_id = str(track_id).strip()
        track_id = None if track_id == '' else track_id
        if track_id is not None and fixture_date is not None:
            with session_scope() as session:
                result = session.query(FirstTrack.tpd_course_id).filter(FirstTrack.track_id == track_id).first()
                if result:
                    tpd_course_id = result.tpd_course_id
                else:
                    tpd_course_id = None
                    logger_1st.error(f'get_tpd_meeting_id(): track_id: {track_id} not found in first_track table')
            if tpd_course_id is not None:
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
                        tpd_meeting_id = new_meeting.id
            else:
                logger_1st.error(f'get_tpd_meeting_id(): track_id: {track_id} is not mapped')
        else:
            logger_1st.error(f'get_tpd_meeting_id(): track_id: {track_id}, fixture_date: {fixture_date} is not valid')
    except Exception as e:
        logger_1st.error(f'get_tpd_meeting_id(): track_id: {track_id}, fixture_date: {fixture_date}')
        logger_1st.error(traceback.format_exc())
    return tpd_meeting_id


def get_tpd_race_id(tpd_meeting_id :int, race_number :int, post_time :datetime) -> int:
    tpd_race_id = None
    try:
        if tpd_meeting_id is not None and race_number is not None and post_time is not None:
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
                    tpd_race_id = new_race.id
        else:
            logger_1st.error(f'get_tpd_race_id(): tpd_meeting_id: {tpd_meeting_id}, race_number: {race_number}, post_time: {post_time} is not valid')
    except Exception as e:
        logger_1st.error(f'get_tpd_race_id(): tpd_meeting_id: {tpd_meeting_id}, race_number: {race_number}, post_time: {post_time}')
        logger_1st.error(traceback.format_exc())
    return tpd_race_id


def get_tpd_runner_id(tpd_race_id :int, program_number :str) -> int:
    tpd_runner_id = None
    try:
        program_number = str(program_number).strip() if program_number is not None else None
        program_number = None if program_number == '' else program_number
        if tpd_race_id is not None and program_number is not None:
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
                    tpd_runner_id = new_runner.id
        else:
            logger_1st.error(f'get_tpd_runner_id(): tpd_race_id: {tpd_race_id}, program_number: {program_number} is not valid')
    except Exception as e:
        logger_1st.error(f'get_tpd_runner_id(): tpd_race_id: {tpd_race_id}, program_number: {program_number}')
        logger_1st.error(traceback.format_exc())
    return tpd_runner_id



def calculate_price(nominator, denominator) -> tuple[str, float]:
    show_price_fraction = None
    show_price_percentage = None
    def is_valid_number(value):
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            if not value.strip():
                return False
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False
    if is_valid_number(nominator) and is_valid_number(denominator):
        try:
            nom_val = float(nominator)
            den_val = float(denominator)
            if den_val == 0:
                logger_1st.error(f'calculate_price(): Division by zero - denominator: {denominator}')
                return show_price_fraction, show_price_percentage
            show_price_fraction = f'{nominator}/{denominator}'
            show_price_percentage = round((nom_val / den_val) * 100, 2)
        except Exception as e:
            logger_1st.error(f'calculate_price(): nominator: {nominator}, denominator: {denominator}')
            logger_1st.error(traceback.format_exc())
    return show_price_fraction, show_price_percentage




