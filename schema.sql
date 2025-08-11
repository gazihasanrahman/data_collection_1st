-- SQL Schema for Horse Racing Data Collection
-- Based on Pydantic models from models.py

-- Track table
CREATE TABLE first_track (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    country_id VARCHAR(255),
    country_name VARCHAR(255),
    timezone VARCHAR(255),
    isdst BOOLEAN,
    timezone_offset INTEGER,
    code VARCHAR(255),
    video_code VARCHAR(255),
    track_type VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Jockey table
CREATE TABLE first_jockey (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    old_jockey_id VARCHAR(255),
    old_jockey_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Fixture table
CREATE TABLE first_fixture (
    id VARCHAR(255) PRIMARY KEY,
    date DATE,
    race_count INTEGER,
    temperature_fahrenheit DECIMAL(5,2),
    temperature_celsius DECIMAL(5,2),
    first_post_time TIMESTAMP,
    track_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (track_id) REFERENCES first_track(id)
);

-- Race table
CREATE TABLE first_race (
    id VARCHAR(255) PRIMARY KEY,
    type VARCHAR(255),
    number VARCHAR(50),
    runner_count INTEGER,
    post_time TIMESTAMP,
    estimated_post_time TIMESTAMP,
    off_time TIMESTAMP,
    weather VARCHAR(255),
    going VARCHAR(255),
    name VARCHAR(255),
    status VARCHAR(255),
    isdst BOOLEAN,
    timezone_offset INTEGER,
    track_surface_value VARCHAR(255),
    overround VARCHAR(255),
    overround_selection VARCHAR(255),
    result TEXT,
    comment TEXT,
    distance_value VARCHAR(255),
    distance_unit VARCHAR(255),
    distance_published_text VARCHAR(255),
    breed VARCHAR(255),
    race_type_type VARCHAR(255),
    race_type_subtype VARCHAR(255),
    race_type_description VARCHAR(255),
    sex_restriction_value VARCHAR(255),
    sex_restriction_description VARCHAR(255),
    age_restriction_value VARCHAR(255),
    age_restriction_description VARCHAR(255),
    purse_value VARCHAR(255),
    purse_ranks VARCHAR(255),
    purse_unit VARCHAR(255),
    grade VARCHAR(255),
    race_tip VARCHAR(255),
    fixture_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (fixture_id) REFERENCES first_fixture(id)
);

-- Race status history table
CREATE TABLE first_race_status_history (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    race_id VARCHAR(255),
    status VARCHAR(255),
    timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (race_id) REFERENCES first_race(id)
);

-- Entry table
CREATE TABLE first_entry (
    id VARCHAR(255) PRIMARY KEY,
    start_number VARCHAR(50),
    program_number VARCHAR(50),
    start_position VARCHAR(50),
    coupled_indicator INTEGER,
    decoupled_number VARCHAR(50),
    horse_id VARCHAR(255),
    name VARCHAR(255),
    status INTEGER,
    equipment_code VARCHAR(50),
    equipment_description VARCHAR(255),
    weight_value VARCHAR(50),
    weight_overweight VARCHAR(50),
    weight_unit VARCHAR(50),
    jockey_id VARCHAR(255),
    starting_price DECIMAL(10,2),
    fav_pos VARCHAR(50),
    fav_joint VARCHAR(50),
    position VARCHAR(50),
    dead_heat VARCHAR(50),
    disqualified BOOLEAN DEFAULT FALSE,
    amended_position VARCHAR(50),
    race_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (race_id) REFERENCES first_race(id),
    FOREIGN KEY (jockey_id) REFERENCES first_jockey(id)
);

-- Entry show prices table
CREATE TABLE first_entry_show_price (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    entry_id VARCHAR(255),
    timestamp TIMESTAMP,
    numerator VARCHAR(50),
    denominator VARCHAR(50),
    price DECIMAL(10,2),
    market VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (entry_id) REFERENCES first_entry(id)
);

-- Entry starting price table
CREATE TABLE first_entry_starting_price (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    entry_id VARCHAR(255),
    nominator VARCHAR(50),
    denominator VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (entry_id) REFERENCES first_entry(id)
);

-- Entry withdrawn table
CREATE TABLE first_entry_withdrawn (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    entry_id VARCHAR(255),
    market INTEGER,
    timestamp TIMESTAMP,
    denominator VARCHAR(50),
    numerator VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (entry_id) REFERENCES first_entry(id)
);

-- Horse table
CREATE TABLE first_horse (
    horse_id VARCHAR(255) PRIMARY KEY,
    external_id VARCHAR(255),
    name VARCHAR(255),
    gender VARCHAR(255),
    breed VARCHAR(255),
    foaling_date DATE,
    foaling_country VARCHAR(255),
    color VARCHAR(255),
    breeder VARCHAR(255),
    horse_id_sire VARCHAR(255),
    horse_id_dam VARCHAR(255),
    horse_id_sire_dam VARCHAR(255),
    horse_id_sire_sire VARCHAR(255),
    horse_id_dam_sire VARCHAR(255),
    horse_id_dam_dam VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- Indexes for better performance
CREATE INDEX idx_first_fixture_date ON first_fixture(date);
CREATE INDEX idx_first_fixture_track_id ON first_fixture(track_id);
CREATE INDEX idx_first_race_fixture_id ON first_race(fixture_id);
CREATE INDEX idx_first_race_number ON first_race(number);
CREATE INDEX idx_first_entry_race_id ON first_entry(race_id);
CREATE INDEX idx_first_entry_jockey_id ON first_entry(jockey_id);
CREATE INDEX idx_first_entry_show_price_entry_id ON first_entry_show_price(entry_id);
CREATE INDEX idx_first_entry_starting_price_entry_id ON first_entry_starting_price(entry_id);
CREATE INDEX idx_first_entry_withdrawn_entry_id ON first_entry_withdrawn(entry_id);
CREATE INDEX idx_first_race_status_history_race_id ON first_race_status_history(race_id);
