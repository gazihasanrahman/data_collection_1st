from sqlalchemy import Column, DECIMAL, Date, DateTime, Float, ForeignKey, LargeBinary, String, Text, Time, text, JSON, Boolean, Numeric, Integer, Double
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, MEDIUMBLOB, MEDIUMTEXT, SMALLINT, TEXT, TIME, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from database.sql import Base, Mixin


###############################################################################################


class MapMeeting(Base, Mixin):
    __tablename__ = 'map_meeting'
    id = Column(INTEGER(11), primary_key=True)
    gmax_estimated = Column(TINYINT(4), nullable=False, server_default=text('0'))
    gmax_meeting_sharecode = Column(String(20, 'utf8_bin'))
    pa_secondary_meeting_id = Column(BIGINT(20))
    bf_event_id = Column(INTEGER(11))
    pa_meeting_id = Column(INTEGER(11))
    bha_unique_fixture_id = Column(INTEGER(11))
    xbnet_fixture_id = Column(INTEGER(8))
    sis_meeting_code = Column(String(8))
    map_course_code = Column(String(4, 'utf8_bin'))
    date = Column(Date)
    notes = Column(Text(collation='utf8_bin'))
    tracked = Column(TINYINT(1), server_default=text('1'))
    map_race = relationship("MapRace", back_populates = "map_meeting", uselist = True)


class MapRace(Base, Mixin):
    __tablename__ = 'map_race'
    id = Column(INTEGER(11), primary_key=True)
    tracked = Column(TINYINT(1), nullable=False, server_default=text('1'))
    map_meeting_id = Column(INTEGER(11), ForeignKey('map_meeting.id'))
    gmax_sharecode = Column(String(20, 'utf8_bin'))
    pa_race_id = Column(INTEGER(11))
    bha_unique_race_id = Column(BIGINT(20))
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


class MapRunner(Base, Mixin):
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
    bha_runner_id = Column(BIGINT(20))
    bha_horse_id = Column(INTEGER(11))
    bf_horse_id = Column(INTEGER(11))
    tpd_prices_id = Column(INTEGER(11))
    runner_number = Column(String(8, 'utf8_bin'))
    notes_internal = Column(Text(collation='utf8_bin'))
    map_race = relationship("MapRace", back_populates = "map_runner", uselist = False)


class MapCourse(Base, Mixin):
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


class MapRaceMetadata(Base, Mixin):
    __tablename__ = 'map_race_metadata'
    id = Column(INTEGER(11), primary_key=True)
    number_race_type_observations = Column(SMALLINT(6))


###############################################################################################




class TsdCourseMap(Base, Mixin):
    __tablename__ = 'tsd_course_map'
    gmax_code = Column(VARCHAR(3), primary_key=True)
    active = Column(TINYINT(1))
    betfair = Column(TINYINT(1))
    country = Column(VARCHAR(24))
    course = Column(VARCHAR(24))
    code = Column(VARCHAR(10))
    country_code = Column(VARCHAR(3))
    rmg = Column(TINYINT(1))


class TsdCountry(Base, Mixin):
    __tablename__ = 'tsd_country'
    country_id = Column(SMALLINT(6), primary_key=True)
    gmax_country_code = Column(String(8, 'utf8_bin'), nullable=False)


class TsdRacecourse(Base, Mixin):
    __tablename__ = 'tsd_racecourse'
    racecourse_id = Column(SMALLINT(6))
    gmax_racecourse_id = Column(String(4, 'utf8_bin'))
    gmax_racecourse_name = Column(VARCHAR(64))
    gmax_additional_label = Column(String(16, 'utf8_bin'))
    country_id = Column(SMALLINT(6))
    ExternalVenueID = Column(String(50), primary_key=True)
    created_at = Column(DateTime(True))
    updated_at = Column(DateTime(True))
    CountyLogoLeft = Column(Boolean)
    SortOrderLowest = Column(Boolean)
    TimeZone = Column(String(255))
    DefaultKit = Column(String(20))
    ClubCode = Column(String(50))
    ClubName = Column(String(500))
    ClubAbbr = Column(String(50))
    VenueName = Column(String(500))
    VenueAbbr = Column(String(50))
    VenueCountry = Column(String(50))
    VenueState = Column(String(50))
    VenueCategory = Column(String(50))
    TrackName = Column(String(50))
    TrackCode = Column(String(50))
    CodeType = Column(String(50))
    OriginLongitude = Column(Numeric)
    OriginLatitude = Column(Numeric)
    OriginOrientiation = Column(Numeric)
    Surface = Column(String(50))
    RacingDirection = Column(String(50))
    TrackCircumference = Column(Integer)
    HomeStraightLength = Column(Integer)
    TrackWidth = Column(Integer)
    Discontinous = Column(Boolean)
    Enabled = Column(Boolean)
    TimingProvider = Column(Text)
    Topic = Column(Text)
    ChickletFolder = Column(String(100))
    SilkFolder = Column(String(100))
    StartlistEmailDL = Column(String(255))
    RaceReportsEmailDL = Column(String(255))
    EODEmailDL = Column(String(255))
    SectionlTimingProvider = Column(Text)
    TabName = Column(Text)
    tpd_course_id = Column(String(4))
    tsd_racetype = relationship('TsdRacetype', back_populates='racecourse')


class TsdMeeting(Base, Mixin):
    __tablename__ = 'tsd_meeting'
    gmax_meeting_sharecode = Column(String(16, 'utf8_bin'))
    estimated = Column(TINYINT(4))
    local_meeting_start_date = Column(Date)
    gmax_course_code = Column(String(2, 'utf8_bin'))
    timestamp_added_from_gmax = Column(DATETIME(fsp=6))
    ExternalEventID = Column(String(50), primary_key=True)
    ExternalVenueID = Column(String(50), primary_key=True)
    created_at = Column(DateTime(True))
    updated_at = Column(DateTime(True))
    VenueName = Column(String(50))
    MeetingCategory = Column(String(50))
    MeetingDate = Column(Date)
    MeetingType = Column(String(50))
    NumberRaces = Column(Integer)
    DayNight = Column(String(50))
    TabStatus = Column(Boolean)
    Penetromer = Column(Numeric)
    Irrigation = Column(String(50))
    KitID = Column(Text)
    IsTagSet = Column(Boolean)
    BarrierTag = Column(Text)
    EventName = Column(Text)
    Rail = Column(Text)
    RailStart = Column(Text)
    RailEnd = Column(Text)
    Remainder = Column(Text)
    Transition = Column(Text)
    EntireCourseRail = Column(Text)
    tpd_meeting_id = Column(INTEGER(11))


class TsdRace(Base, Mixin):
    __tablename__ = 'tsd_race'
    sharecode = Column(String(20, 'utf8_bin'))
    gmax_meeting_sharecode = Column(String(16))
    race_number = Column(SMALLINT(6))
    post_time = Column(DATETIME(fsp=6))
    off_time = Column(DATETIME(fsp=6))
    official_win_time = Column(Float)
    gmax_live_win_time = Column(Float)
    estimated = Column(TINYINT(1))
    published = Column(TINYINT(1))
    timestamp_modified = Column(DateTime)
    racetype_id = Column(INTEGER(11))
    runner_sectionals_populated = Column(SMALLINT(6))
    tpd_runner_sectionals_populated = Column(SMALLINT(6))
    gmax_merged_runner_sectionals_populated = Column(SMALLINT(6))
    live_recording_available = Column(TINYINT(1))
    gmax_notes = Column(Text(collation='utf8_bin'))
    ExternalRaceID = Column(String(50), primary_key=True)
    created_at = Column(DateTime(True))
    updated_at = Column(DateTime(True))
    ExternalVenueID = Column(String(50))
    ExternalEventID = Column(String(50))
    RaceName = Column(String(1024))
    RaceNumber = Column(Integer)
    RaceClass = Column(String(50))
    ScheduledDate = Column(Date)
    ScheduledTime = Column(Time)
    StartTime = Column(Time)
    FinishTime = Column(Time)
    MileRate = Column(Time)
    RaceLength = Column(String(50))
    DistanceApprox = Column(Boolean)
    TrackID = Column(Integer)
    EQTraCeTrack = Column(String(50))
    RaceType = Column(String(50))
    SizeField = Column(Integer)
    RailPosition = Column(String(80))
    SplitRail = Column(Boolean)
    TrackCondition = Column(String(50))
    Weather = Column(String(1024))
    Rainfall = Column(String(50))
    WindDirection = Column(String(50))
    WindDirectionDeg = Column(Numeric)
    WindSpeed = Column(Numeric)
    SoilMoisture = Column(Numeric)
    SizeField = Column(Integer)
    TrackType = Column(Text)
    Prize = Column(Double)
    Section0 = Column(Time())
    Section1 = Column(Time())
    Section2 = Column(Time())
    Section3 = Column(Time())
    Section4 = Column(Time())
    Section5 = Column(Time())
    Section6 = Column(Time())
    Section7 = Column(Time())
    Section8 = Column(Time())
    Section9 = Column(Time())
    Section10 = Column(Time())
    Section11 = Column(Time())
    Section12 = Column(Time())
    Section13 = Column(Time())
    Section14 = Column(Time())
    Section15 = Column(Time())
    Section16 = Column(Time())
    Section17 = Column(Time())
    Section18 = Column(Time())
    Section19 = Column(Time())
    Section20 = Column(Time())
    RaceState = Column(String(100))
    class_def = Column(String(100))
    tpd_RaceClass = Column(Integer)
    tpd_race_id = Column(INTEGER(11))
    betmakers_race_id = Column(String(48))



class TsdRunner(Base, Mixin):
    __tablename__ = 'tsd_runner'
    runner_sharecode = Column(String(20, 'utf8_bin'))
    race_sharecode = Column(String(20))
    primary_tracker_id = Column(INTEGER(11), nullable = True)
    secondary_tracker_id = Column(INTEGER(11), nullable = True)
    radio_percentage = Column(Float)
    finish_line_error = Column(Float)
    estimated_splits = Column(SMALLINT(6))
    finish_time = Column(Float)
    EntrantsID = Column(String(50), primary_key=True)
    ExternalEventID = Column(String(50), primary_key=True)
    ExternalVenueID = Column(String(50), primary_key=True)
    ExternalRaceID = Column(String(50), primary_key=True)
    ExternalAnimalID = Column(String(50), primary_key=True)
    ExternalJockeyID = Column(String(50))
    ExternalTrainerID = Column(String(50))
    created_at = Column(DateTime(True))
    updated_at = Column(DateTime(True))
    ExternalSilkID = Column(String(50))
    RacingColour1 = Column(String(500))
    RacingColour2 = Column(String(500))
    RacingColour3 = Column(String(500))
    HasJockey = Column(Boolean)
    StartNumber = Column(Integer)
    BallotSequence = Column(String(50))
    BarrierNumber = Column(String(50))
    HandicapWeight = Column(Numeric)
    HandicapRating = Column(Numeric)
    WeightPenalty = Column(Numeric)
    Handicap = Column(String(500))
    Gear = Column(String(500))
    RaceState = Column(String(50))
    IsLateScratching = Column(Boolean)
    ReasonScratching = Column(String(500))
    OfficialFinishTime = Column(Time)
    FinishRank = Column(Integer)
    MarginNumeric = Column(Numeric)
    Margin = Column(String(500))
    DistanceTravelled = Column(String(50))
    MileRate = Column(String(50))
    TopSpeed = Column(Numeric)
    DeviceID = Column(Integer)
    RaceSubState = Column(String)
    LastMile = Column(String(100))
    LastMileDistance = Column(Numeric)
    TopSpeedSection = Column(String(50))
    FastestSection = Column(String(50))
    DistanceMargin = Column(String(50))
    tpd_runner_id = Column(INTEGER(11))


class TsdAnimal(Base, Mixin):
    __tablename__ = 'tsd_animal'
    ExternalAnimalID = Column(String(50), primary_key=True)
    created_at = Column(DateTime(True))
    updated_at = Column(DateTime(True))
    AnimalName = Column(String(1024))
    Colour = Column(String(500))
    Sex = Column(String(50))
    Age = Column(Integer)
    FoalDate = Column(Date)
    OfficalAnimalOwners = Column(String(1024))
    ExternalSireID = Column(String(500))
    ExternalDamID = Column(String(500))
    ExternalSireofDamID = Column(String(500))
    Breeder = Column(String(500))


class TsdJockey(Base, Mixin):
    __tablename__ = 'tsd_jockey'
    ExternalJockeyID = Column(String(50), primary_key=True)
    Apprentice = Column(String(50))
    JockeyName = Column(String)
    Gender = Column(String(50))
    JockeyLocation = Column(String(50))
    JockeyState = Column(String(50))
    Postcode = Column(String(50))
    Country = Column(String(50))
    RidingWeight = Column(Numeric)
    created_at = Column(DateTime(True))
    updated_at = Column(DateTime(True))


class TsdTrainer(Base, Mixin):
    __tablename__ = 'tsd_trainer'
    ExternalTrainerID = Column(String(50), primary_key=True)
    TrainerName = Column(String(50))
    Gender = Column(String(50))
    TrainerLocation = Column(String(50))
    TrainerState = Column(String(50))
    Postcode = Column(String(50))
    Country = Column(String(50))
    created_at = Column(DateTime(True))
    updated_at = Column(DateTime(True))


class TsdObstacle(Base, Mixin):
    __tablename__ = 'tsd_obstacle'
    obstacle_id = Column(Integer, primary_key=True)
    obstacle = Column(String(32))
    tsd_racetype = relationship('TsdRacetype', back_populates='obstacle')


class TsdSurface(Base, Mixin):
    __tablename__ = 'tsd_surface'
    surface_id = Column(Integer, primary_key=True)
    surface = Column(String(32))
    tsd_racetype = relationship('TsdRacetype', back_populates='surface')


class TsdRacetype(Base, Mixin):
    __tablename__ = 'tsd_racetype'
    racetype_id = Column(Integer, primary_key=True)
    ExternalVenueID = Column(String(50))
    gmax_race_length = Column(Float)
    gmax_racetype_label = Column(String(64))
    surface_id = Column(Integer, ForeignKey('tsd_surface.surface_id'))
    obstacle_id = Column(Integer, ForeignKey('tsd_obstacle.obstacle_id'))
    detail_id = Column(Integer)
    racecourse_id = Column(Integer, ForeignKey('tsd_racecourse.racecourse_id'))
    start_line_id = Column(Integer)
    finish_line_id = Column(Integer)
    has_strange_sectional_gates = Column(Integer, server_default = text('0'))
    RaceLength = Column(String(50))
    RaceType = Column(String(50))
    TrackType = Column(String(20))
    obstacle = relationship('TsdObstacle', back_populates='tsd_racetype')
    racecourse = relationship('TsdRacecourse', back_populates='tsd_racetype')
    surface = relationship('TsdSurface', back_populates='tsd_racetype')



###############################################################################################


class TpdPricingMeeting(Base, Mixin):
    __tablename__ = 'tpd_pricing_meeting'
    gmax_meeting_sharecode = Column(VARCHAR(16), primary_key=True)
    gmax_course_code = Column(VARCHAR(2))
    date = Column(Date)
    racecourse_id = Column(SMALLINT(6))
    

class TpdPricingRace(Base, Mixin):
    __tablename__ = 'tpd_pricing_race'
    pa_race_id = Column(BIGINT(20), primary_key=True, autoincrement=True)
    sharecode = Column(VARCHAR(20))
    gmax_meeting_sharecode = Column(VARCHAR(16))
    race_number = Column(SMALLINT(6))
    post_time = Column(DATETIME(6))
    start_time = Column(DATETIME(6))
    finish_time = Column(DATETIME(6))
    price_count = Column(SMALLINT(6), default=0)
    alert_count = Column(SMALLINT(6), default=0)
    coverage_percent = Column(Float)
    from_pricing_server = Column(Float, default=False)
    comment = Column(Text)


class TpdPrice(Base, Mixin):
    __tablename__ = 'tpd_price'
    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    race_sharecode = Column(VARCHAR(20))
    runner_sharecode = Column(VARCHAR(20))
    pa_runner_number = Column(SMALLINT(6))
    prob = Column(Float)
    book_price = Column(Float)
    timestamp = Column(DateTime)
    suspended = Column(Boolean)
    count = Column(INTEGER(11))
    packet_type_id = Column(SMALLINT(6))
    model_version_id = Column(SMALLINT(6))
    price_id = Column(SMALLINT(6))
    market_type_id = Column(SMALLINT(6))


class TpdPacketType(Base, Mixin):
    __tablename__ = 'tpd_packet_type'
    packet_type_id = Column(SMALLINT(6), primary_key=True, autoincrement=True) 
    packet_type = Column(VARCHAR(32), nullable=False, unique=True)


class TpdPricingModelVersion(Base, Mixin):
    __tablename__ = 'tpd_pricing_model_version'
    version_id = Column(SMALLINT(6), primary_key=True, autoincrement=True)
    version_name = Column(VARCHAR(32))
    description = Column(Text)
    active = Column(Boolean, default=True)
    report_on = Column(Boolean, default=False)


class TpdMarketType(Base, Mixin):
    __tablename__ = 'tpd_market_type'
    market_type_id = Column(SMALLINT(6), primary_key=True, autoincrement=True)
    market_type = Column(VARCHAR(32), nullable=False, unique=True)


class TpdPriceAlertCode(Base, Mixin):
    __tablename__ = 'tpd_price_alert_code'
    code = Column(SMALLINT(6), primary_key=True)
    name = Column(VARCHAR(64))
    description = Column(VARCHAR(256))


class TpdPriceAlert(Base, Mixin):
    __tablename__ = 'tpd_price_alert'
    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    race_sharecode = Column(VARCHAR(20))
    cloth = Column(VARCHAR(2))
    timestamp = Column(DATETIME(6))
    code = Column(INTEGER(11))
    packet_type_id = Column(SMALLINT(6))


class StreamUdpRaceInfo(Base, Mixin):
    __tablename__ = 'stream_udp_race_info'
    sc = Column(VARCHAR(20), primary_key=True)
    start = Column(Float)
    end = Column(Float)
    final_r = Column(Float)
    packet_count = Column(Integer)
    coverage = Column(Float)
    notes = Column(Text)
    okayed = Column(Boolean)
    bf_start = Column(Float)



