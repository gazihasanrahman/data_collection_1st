from sqlalchemy import Column, DECIMAL, Date, DateTime, Float, ForeignKey, LargeBinary, String, Text, Time, text, JSON, Boolean, Numeric, Integer, Double
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, MEDIUMBLOB, MEDIUMTEXT, SMALLINT, TEXT, TIME, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from database.sql import Base, Mixin
from sqlalchemy import func


###############################################################################################


class FirstTrack(Base):
    __tablename__ = 'first_track'
    
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    country_id = Column(String(255))
    country_name = Column(String(255))
    timezone = Column(String(255))
    isdst = Column(Boolean)
    timezone_offset = Column(Integer)
    code = Column(String(255))
    video_code = Column(String(255))
    track_type = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    fixtures = relationship("FirstFixture", back_populates="track")


class FirstJockey(Base):
    __tablename__ = 'first_jockey'
    
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    old_jockey_id = Column(String(255))
    old_jockey_name = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    entries = relationship("FirstEntry", back_populates="jockey")


class FirstFixture(Base):
    __tablename__ = 'first_fixture'
    
    id = Column(String(255), primary_key=True)
    date = Column(Date)
    race_count = Column(Integer)
    temperature_fahrenheit = Column(DECIMAL(5, 2))
    temperature_celsius = Column(DECIMAL(5, 2))
    first_post_time = Column(DateTime)
    track_id = Column(String(255), ForeignKey('first_track.id'))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    track = relationship("FirstTrack", back_populates="fixtures")
    races = relationship("FirstRace", back_populates="fixture")


class FirstRace(Base):
    __tablename__ = 'first_race'
    
    id = Column(String(255), primary_key=True)
    type = Column(String(255))
    number = Column(String(50))
    runner_count = Column(Integer)
    post_time = Column(DateTime)
    estimated_post_time = Column(DateTime)
    off_time = Column(DateTime)
    weather = Column(String(255))
    going = Column(String(255))
    name = Column(String(255))
    status = Column(String(255))
    isdst = Column(Boolean)
    timezone_offset = Column(Integer)
    track_surface_value = Column(String(255))
    overround = Column(String(255))
    overround_selection = Column(String(255))
    result = Column(Text)
    comment = Column(Text)
    distance_value = Column(String(255))
    distance_unit = Column(String(255))
    distance_published_text = Column(String(255))
    breed = Column(String(255))
    race_type_type = Column(String(255))
    race_type_subtype = Column(String(255))
    race_type_description = Column(String(255))
    sex_restriction_value = Column(String(255))
    sex_restriction_description = Column(String(255))
    age_restriction_value = Column(String(255))
    age_restriction_description = Column(String(255))
    purse_value = Column(String(255))
    purse_ranks = Column(String(255))
    purse_unit = Column(String(255))
    grade = Column(String(255))
    race_tip = Column(String(255))
    fixture_id = Column(String(255), ForeignKey('first_fixture.id'))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    fixture = relationship("FirstFixture", back_populates="races")
    entries = relationship("FirstEntry", back_populates="race")
    status_history = relationship("FirstRaceStatusHistory", back_populates="race")


class FirstRaceStatusHistory(Base):
    __tablename__ = 'first_race_status_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(String(255), ForeignKey('first_race.id'))
    status = Column(String(255))
    timestamp = Column(DateTime)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    race = relationship("FirstRace", back_populates="status_history")


class FirstEntry(Base):
    __tablename__ = 'first_entry'
    
    id = Column(String(255), primary_key=True)
    start_number = Column(String(50))
    program_number = Column(String(50))
    start_position = Column(String(50))
    coupled_indicator = Column(Integer)
    decoupled_number = Column(String(50))
    horse_id = Column(String(255))
    name = Column(String(255))
    status = Column(Integer)
    equipment_code = Column(String(50))
    equipment_description = Column(String(255))
    weight_value = Column(String(50))
    weight_overweight = Column(String(50))
    weight_unit = Column(String(50))
    jockey_id = Column(String(255), ForeignKey('first_jockey.id'))
    starting_price = Column(DECIMAL(10, 2))
    fav_pos = Column(String(50))
    fav_joint = Column(String(50))
    position = Column(String(50))
    dead_heat = Column(String(50))
    disqualified = Column(Boolean, default=False)
    amended_position = Column(String(50))
    race_id = Column(String(255), ForeignKey('first_race.id'))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    race = relationship("FirstRace", back_populates="entries")
    jockey = relationship("FirstJockey", back_populates="entries")
    show_prices = relationship("FirstEntryShowPrice", back_populates="entry")
    starting_prices = relationship("FirstEntryStartingPrice", back_populates="entry")
    withdrawn_entries = relationship("FirstEntryWithdrawn", back_populates="entry")


class FirstEntryShowPrice(Base):
    __tablename__ = 'first_entry_show_price'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(String(255), ForeignKey('first_entry.id'))
    timestamp = Column(DateTime)
    numerator = Column(String(50))
    denominator = Column(String(50))
    price = Column(DECIMAL(10, 2))
    market = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    entry = relationship("FirstEntry", back_populates="show_prices")


class FirstEntryStartingPrice(Base):
    __tablename__ = 'first_entry_starting_price'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(String(255), ForeignKey('first_entry.id'))
    nominator = Column(String(50))
    denominator = Column(String(50))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    entry = relationship("FirstEntry", back_populates="starting_prices")


class FirstEntryWithdrawn(Base):
    __tablename__ = 'first_entry_withdrawn'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(String(255), ForeignKey('first_entry.id'))
    market = Column(Integer)
    timestamp = Column(DateTime)
    denominator = Column(String(50))
    numerator = Column(String(50))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    entry = relationship("FirstEntry", back_populates="withdrawn_entries")


class FirstHorse(Base):
    __tablename__ = 'first_horse'
    
    horse_id = Column(String(255), primary_key=True)
    external_id = Column(String(255))
    name = Column(String(255))
    gender = Column(String(255))
    breed = Column(String(255))
    foaling_date = Column(Date)
    foaling_country = Column(String(255))
    color = Column(String(255))
    breeder = Column(String(255))
    horse_id_sire = Column(String(255))
    horse_id_dam = Column(String(255))
    horse_id_sire_dam = Column(String(255))
    horse_id_sire_sire = Column(String(255))
    horse_id_dam_sire = Column(String(255))
    horse_id_dam_dam = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    