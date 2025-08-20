CREATE TABLE first_track (
    track_id VARCHAR(8) PRIMARY KEY,
    track_name VARCHAR(64),
    country_id VARCHAR(4),
    country_name VARCHAR(4),
    timezone VARCHAR(32),
    isdst BOOLEAN,
    timezone_offset INTEGER,
    code VARCHAR(6),
    video_code VARCHAR(16),
    track_type_id VARCHAR(8),
    tpd_course_id VARCHAR(3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE first_track_type (
    track_type_id VARCHAR(8) PRIMARY KEY,
    track_type VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE first_fixture (
    fixture_id VARCHAR(8) PRIMARY KEY,
    track_id VARCHAR(8),
    fixture_date DATE,
    first_post_time TIMESTAMP,
    race_count INTEGER,
    temperature_fahrenheit INTEGER,
    temperature_celsius FLOAT,
    tpd_meeting_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_race (
    race_id VARCHAR(8) PRIMARY KEY,
    fixture_id VARCHAR(8),
    track_type VARCHAR(16),
    race_number INTEGER,
    runner_count INTEGER,
    post_time TIMESTAMP,
    estimated_post_time TIMESTAMP,
    off_time TIMESTAMP,
    race_status VARCHAR(128),
    race_result TEXT,
    isdst BOOLEAN,
    timezone_offset INTEGER,
    weather VARCHAR(64),
    going VARCHAR(64),
    surface_id VARCHAR(8),
    grade VARCHAR(64),
    distance INTEGER,
    distance_unit VARCHAR(16),
    distance_text VARCHAR(64),
    race_breed VARCHAR(64),
    racetype_id VARCHAR(8),
    racetype_subtype VARCHAR(64),
    sex_restriction_id VARCHAR(8),
    age_restriction_id VARCHAR(8),
    purse INTEGER,
    purse_ranks VARCHAR(255),
    purse_unit VARCHAR(16),
    overround FLOAT,
    overround_selection VARCHAR(64),
    race_name VARCHAR(255),
    race_comment TEXT,
    race_tip TEXT,
    tpd_race_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_racetype (
    racetype_id VARCHAR(8) PRIMARY KEY,
    racetype VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_surface (
    surface_id VARCHAR(8) PRIMARY KEY,
    surface VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_sex_restriction (
    sex_restriction_id VARCHAR(8) PRIMARY KEY,
    sex_restriction VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_age_restriction (
    age_restriction_id VARCHAR(8) PRIMARY KEY,
    age_restriction VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_entry (
    entry_id VARCHAR(16) PRIMARY KEY,
    race_id VARCHAR(8),
    start_number VARCHAR(4),
    program_number VARCHAR(4),
    start_position VARCHAR(4),
    coupled_indicator INTEGER,
    decoupled_number VARCHAR(4),
    scratch_indicator VARCHAR(4),
    age INTEGER,
    weight INTEGER,
    weight_unit VARCHAR(4),
    horse_id VARCHAR(8),
    jockey_id VARCHAR(8),
    trainer_id VARCHAR(8),
    owner_id VARCHAR(8),
    breeder_name TEXT,
    entry_status VARCHAR(16),
    starting_price_nominator VARCHAR(4),
    starting_price_denominator VARCHAR(4),
    fav_pos VARCHAR(4),
    fav_joint VARCHAR(4),
    final_position INTEGER,
    dead_heat VARCHAR(16),
    disqualified BOOLEAN,
    amended_position VARCHAR(50),
    runner_tip TEXT,
    tpd_runner_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_price_history (
    price_id VARCHAR(16) PRIMARY KEY,
    entry_id VARCHAR(16),
    timestamp TIMESTAMP,
    numerator VARCHAR(4),
    denominator VARCHAR(4),
    market VARCHAR(4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_race_status_history (
    race_status_id VARCHAR(16) PRIMARY KEY,
    race_id VARCHAR(8),
    status VARCHAR(16),
    timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_horse (
    horse_id VARCHAR(8) PRIMARY KEY,
    external_id VARCHAR(16),
    horse_name VARCHAR(128),
    gender VARCHAR(64),
    breed VARCHAR(64),
    foaling_date DATE,
    foaling_country VARCHAR(8),
    color VARCHAR(128),
    breeder TEXT,
    horse_id_sire VARCHAR(8),
    horse_id_dam VARCHAR(8),
    horse_id_sire_dam VARCHAR(8),
    horse_id_sire_sire VARCHAR(8),
    horse_id_dam_sire VARCHAR(8),
    horse_id_dam_dam VARCHAR(8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_jockey (
    jockey_id VARCHAR(8) PRIMARY KEY,
    jockey_name VARCHAR(128),
    old_jockey_id VARCHAR(8),
    old_jockey_name VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_trainer (
    trainer_id VARCHAR(8) PRIMARY KEY,
    trainer_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE first_owner (
    owner_id VARCHAR(8) PRIMARY KEY,
    owner_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

