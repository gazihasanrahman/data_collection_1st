import os
import contextlib
from sqlalchemy import create_engine, func, Column, DECIMAL, Date, DateTime, Float, ForeignKey, LargeBinary, String, Text, Time, text, JSON, Boolean, Numeric, Integer, Double
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.engine.base import Engine
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, MEDIUMBLOB, MEDIUMTEXT, SMALLINT, TEXT, TIME, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from utils.logger import logger_database_errors
import traceback


HOST = os.environ.get("MARIADB_HOST", "")
USER = os.environ.get("MARIADB_USER", "")
PASS = os.environ.get("MARIADB_PASS", "")
mariadb_engine = create_engine(
    url=f"mysql+pymysql://{USER}:{PASS}@{HOST}:{3306}/general",
    pool_pre_ping=True,
    pool_size=24,
    max_overflow=24,
)

@contextlib.contextmanager
def session_scope(engine: Engine = mariadb_engine, raise_error: bool = False):
    """Provide a transactional scope around a series of operations."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger_database_errors.error(e)
        logger_database_errors.error(traceback.format_exc())
        if raise_error:
            raise
    finally:
        session.close()


Base = declarative_base()

class MapCourse(Base):
    __tablename__ = 'map_course'
    code = Column(String(4, 'utf8_unicode_ci'), primary_key=True)
    short_name = Column(String(64, 'utf8_unicode_ci'), nullable=False)
    full_name = Column(String(64, 'utf8_unicode_ci'), nullable=False)
    country_code = Column(String(3, 'utf8_unicode_ci'), nullable=False)
    xbnet = Column(TINYINT(1), nullable=False, server_default=text('0'))
    stride = Column(TINYINT(1), nullable=False, server_default=text('0'))
    timezone = Column(String(64, 'utf8_unicode_ci'))
    bha_course_key = Column(SMALLINT(6))
    tpd_racecourse_owner_id = Column(SMALLINT(6))
    tpd_broadcaster_id = Column(SMALLINT(6))
    inrunning_model_owner_id = Column(TINYINT(3))
    tier = Column(INTEGER(11))
    mclloyd_priority = Column(INTEGER(11))


class MapMeeting(Base):
    __tablename__ = 'map_meeting'
    id = Column(INTEGER(11), primary_key=True)
    gmax_estimated = Column(TINYINT(4), nullable=False, server_default=text('0'))
    gmax_meeting_sharecode = Column(String(20, 'utf8_bin'))
    pa_secondary_meeting_id = Column(BIGINT(20))
    bf_event_id = Column(INTEGER(11))
    pa_meeting_id = Column(INTEGER(11))
    xbnet_fixture_id = Column(INTEGER(8))
    sis_meeting_code = Column(String(8))
    map_course_code = Column(String(4, 'utf8_bin'))
    date = Column(Date)
    notes = Column(Text(collation='utf8_bin'))
    tracked = Column(TINYINT(1), server_default=text('1'))
    map_race = relationship("MapRace", back_populates = "map_meeting", uselist = True)


class MapRace(Base):
    __tablename__ = 'map_race'
    id = Column(INTEGER(11), primary_key=True)
    tracked = Column(TINYINT(1), nullable=False, server_default=text('1'))
    map_meeting_id = Column(INTEGER(11), ForeignKey('map_meeting.id'))
    gmax_sharecode = Column(String(20, 'utf8_bin'))
    pa_race_id = Column(INTEGER(11))
    sis_race_id = Column(Integer)
    bf_market_id_win = Column(String(16, 'utf8_bin'))
    bf_market_id_2tbp = Column(String(16, 'utf8_bin'))
    bf_market_id_3tbp = Column(String(16, 'utf8_bin'))
    bf_market_id_4tbp = Column(String(16, 'utf8_bin'))
    bf_market_id_place = Column(String(16, 'utf8_bin'))
    bf_market_id_ew = Column(String(16, 'utf8_bin'))
    post_time = Column(DATETIME(fsp=6))
    race_number = Column(SMALLINT(6))
    tpd_pars_id = Column(INTEGER(11))
    tpd_pars_estimated = Column(TINYINT(1))
    notes = Column(Text(collation='utf8_bin'))
    notes_internal = Column(Text(collation='utf8_bin'))
    issues = Column(Text(collation='utf8_bin'), server_default=text("''"))
    issues_resolved = Column(INTEGER(11))
    tpd_issues_npt = Column(INTEGER(11))
    map_meeting = relationship("MapMeeting", back_populates = "map_race", uselist = False)
    map_runner = relationship("MapRunner", back_populates = "map_race", uselist = True)


class MapRunner(Base):
    __tablename__ = 'map_runner'
    id = Column(INTEGER(11), primary_key=True)
    map_race_id = Column(INTEGER(11), ForeignKey('map_race.id'))
    gmax_runner_sharecode = Column(String(20, 'utf8_bin'))
    tpd_runner_id = Column(INTEGER(11))
    sis_runner_id = Column(Integer)
    bf_runner_id_win = Column(INTEGER(11))
    bf_runner_id_2tbp = Column(INTEGER(11))
    bf_runner_id_3tbp = Column(INTEGER(11))
    bf_runner_id_4tbp = Column(INTEGER(11))
    bf_runner_id_place = Column(INTEGER(11))
    bf_runner_id_ew = Column(INTEGER(11))
    pa_horse_id = Column(INTEGER(11))
    bf_horse_id = Column(INTEGER(11))
    tpd_prices_id = Column(INTEGER(11))
    runner_number = Column(String(8, 'utf8_bin'))
    notes_internal = Column(Text(collation='utf8_bin'))
    map_race = relationship("MapRace", back_populates = "map_runner", uselist = False)


class FirstTrack(Base):
    __tablename__ = 'first_track'
    track_id = Column(VARCHAR(8), primary_key=True)
    track_name = Column(VARCHAR(64))
    country_id = Column(VARCHAR(4))
    country_name = Column(VARCHAR(4))
    timezone = Column(VARCHAR(32))
    isdst = Column(Boolean)
    timezone_offset = Column(Integer)
    code = Column(VARCHAR(6))
    video_code = Column(VARCHAR(16))
    track_type_id = Column(VARCHAR(8))
    tpd_course_id = Column(VARCHAR(3))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstTrackType(Base):
    __tablename__ = 'first_track_type'
    track_type_id = Column(VARCHAR(8), primary_key=True)
    track_type = Column(VARCHAR(128))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstFixture(Base):
    __tablename__ = 'first_fixture'
    fixture_id = Column(VARCHAR(8), primary_key=True)
    track_id = Column(VARCHAR(8))
    fixture_date = Column(Date)
    first_post_time = Column(DateTime)
    race_count = Column(Integer)
    temperature_fahrenheit = Column(Integer)
    temperature_celsius = Column(Float)
    tpd_meeting_id = Column(Integer)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstRace(Base):
    __tablename__ = 'first_race'
    race_id = Column(VARCHAR(8), primary_key=True)
    fixture_id = Column(VARCHAR(8))
    track_type = Column(VARCHAR(16))
    race_number = Column(Integer)
    runner_count = Column(Integer)
    post_time = Column(DateTime)
    estimated_post_time = Column(DateTime)
    off_time = Column(DateTime)
    race_status = Column(VARCHAR(128))
    race_result = Column(Text)
    isdst = Column(Boolean)
    timezone_offset = Column(Integer)
    weather = Column(VARCHAR(64))
    going = Column(VARCHAR(64))
    surface_id = Column(VARCHAR(8))
    grade = Column(VARCHAR(64))
    distance = Column(Integer)
    distance_unit = Column(VARCHAR(16))
    distance_text = Column(VARCHAR(64))
    race_breed = Column(VARCHAR(64))
    racetype_id = Column(VARCHAR(8))
    racetype_subtype = Column(VARCHAR(64))
    sex_restriction_id = Column(VARCHAR(8))
    age_restriction_id = Column(VARCHAR(8))
    purse = Column(Integer)
    purse_ranks = Column(VARCHAR(255))
    purse_unit = Column(VARCHAR(16))
    overround = Column(Float)
    overround_selection = Column(VARCHAR(64))
    race_name = Column(VARCHAR(255))
    race_comment = Column(Text)
    race_tip = Column(Text)
    tpd_race_id = Column(Integer)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstRacetype(Base):
    __tablename__ = 'first_racetype'
    racetype_id = Column(VARCHAR(8), primary_key=True)
    racetype = Column(VARCHAR(64))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstSurface(Base):
    __tablename__ = 'first_surface'
    surface_id = Column(VARCHAR(8), primary_key=True)
    surface = Column(VARCHAR(64))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstSexRestriction(Base):
    __tablename__ = 'first_sex_restriction'
    sex_restriction_id = Column(VARCHAR(8), primary_key=True)
    sex_restriction = Column(VARCHAR(128))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstAgeRestriction(Base):
    __tablename__ = 'first_age_restriction'
    age_restriction_id = Column(VARCHAR(8), primary_key=True)
    age_restriction = Column(VARCHAR(128))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstEntry(Base):
    __tablename__ = 'first_entry'
    entry_id = Column(VARCHAR(16), primary_key=True)
    race_id = Column(VARCHAR(8))
    start_number = Column(VARCHAR(4))
    program_number = Column(VARCHAR(4))
    start_position = Column(VARCHAR(4))
    coupled_indicator = Column(Integer)
    decoupled_number = Column(VARCHAR(4))
    scratch_indicator = Column(VARCHAR(4))
    age = Column(Integer)
    weight = Column(Integer)
    weight_unit = Column(VARCHAR(4))
    horse_id = Column(VARCHAR(8))
    jockey_id = Column(VARCHAR(8))
    trainer_id = Column(VARCHAR(8))
    owner_id = Column(VARCHAR(8))
    breeder_name = Column(Text)
    entry_status = Column(VARCHAR(16))
    starting_price_nominator = Column(VARCHAR(4))
    starting_price_denominator = Column(VARCHAR(4))
    fav_pos = Column(VARCHAR(4))
    fav_joint = Column(VARCHAR(4))
    final_position = Column(Integer)
    dead_heat = Column(VARCHAR(16))
    disqualified = Column(Boolean)
    amended_position = Column(VARCHAR(50))
    runner_tip = Column(Text)
    tpd_runner_id = Column(Integer)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstPriceHistory(Base):
    __tablename__ = 'first_price_history'
    price_id = Column(VARCHAR(16), primary_key=True)
    entry_id = Column(VARCHAR(16))
    timestamp = Column(DateTime)
    numerator = Column(VARCHAR(4))
    denominator = Column(VARCHAR(4))
    market = Column(VARCHAR(4))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstRaceStatusHistory(Base):
    __tablename__ = 'first_race_status_history'
    race_status_id = Column(VARCHAR(16), primary_key=True)
    race_id = Column(VARCHAR(8))
    status = Column(VARCHAR(16))
    timestamp = Column(DateTime)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    

class FirstHorse(Base):
    __tablename__ = 'first_horse'
    horse_id = Column(VARCHAR(8), primary_key=True)
    external_id = Column(VARCHAR(16))
    horse_name = Column(VARCHAR(128))
    gender = Column(VARCHAR(64))
    breed = Column(VARCHAR(64))
    foaling_date = Column(Date)
    foaling_country = Column(VARCHAR(8))
    color = Column(VARCHAR(128))
    breeder = Column(Text)
    horse_id_sire = Column(VARCHAR(8))
    horse_id_dam = Column(VARCHAR(8))
    horse_id_sire_dam = Column(VARCHAR(8))
    horse_id_sire_sire = Column(VARCHAR(8))
    horse_id_dam_sire = Column(VARCHAR(8))
    horse_id_dam_dam = Column(VARCHAR(8))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    

class FirstJockey(Base):
    __tablename__ = 'first_jockey'
    jockey_id = Column(VARCHAR(8), primary_key=True)
    jockey_name = Column(VARCHAR(128))
    old_jockey_id = Column(VARCHAR(8))
    old_jockey_name = Column(VARCHAR(128))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstTrainer(Base):
    __tablename__ = 'first_trainer'
    trainer_id = Column(VARCHAR(8), primary_key=True)
    trainer_name = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class FirstOwner(Base):
    __tablename__ = 'first_owner'
    owner_id = Column(VARCHAR(8), primary_key=True)
    owner_name = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

