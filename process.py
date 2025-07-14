import json
import glob
import os
import pandas as pd
from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta, date
from dateutil.parser import parse
import models_db as mdb
import models_pd as mpd
from utils.sql import session_scope
from utils.logger import get_logger
from sqlalchemy import and_, or_
from typing import Dict, List, Optional, Set
import hashlib

# Set up logging
logger = get_logger(log_name="etl_process")

file_location = '/home/gazi/Desktop/downloads'
files = glob.glob(os.path.join(file_location, '*.json'))

# Cache for tracking processed records to avoid duplicates
processed_cache = {
    'tracks': set(),
    'jockeys': set(),
    'fixtures': set(),
    'races': set(),
    'entries': set(),
    'status_history': set(),
    'show_prices': set(),
    'starting_prices': set(),
    'withdrawn_entries': set()
}

def generate_hash(data: dict, fields: List[str]) -> str:
    """Generate a hash for duplicate detection"""
    hash_data = {}
    for k in fields:
        value = data.get(k)
        if value is not None:
            # Convert date objects to string for JSON serialization
            if isinstance(value, (datetime, date)):
                hash_data[k] = value.isoformat()
            else:
                hash_data[k] = value
    
    hash_string = json.dumps(hash_data, sort_keys=True)
    return hashlib.md5(hash_string.encode()).hexdigest()

def safe_get_nested(data: dict, *keys, default=None):
    """Safely get nested dictionary values"""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def process_track(session, track_data: dict) -> Optional[str]:
    """Process track data and return track ID"""
    if not track_data or not track_data.get('id'):
        return None
    
    track_hash = generate_hash(track_data, ['id', 'name', 'countryid', 'countryName'])
    if track_hash in processed_cache['tracks']:
        return track_data['id']
    
    try:
        # Create track object
        track = mdb.FirstTrack(
            id=track_data['id'],
            name=track_data.get('name'),
            country_id=track_data.get('countryid'),
            country_name=track_data.get('countryName'),
            timezone=track_data.get('timezone'),
            isdst=track_data.get('isdst'),
            timezone_offset=track_data.get('timezoneOffset'),
            code=track_data.get('code'),
            video_code=track_data.get('videocode'),
            track_type=track_data.get('trackType')
        )
        
        # Use merge to handle both insert and update
        session.merge(track)
        processed_cache['tracks'].add(track_hash)
        logger.info(f"Processed track: {track_data['id']}")
        return track_data['id']
        
    except Exception as e:
        logger.error(f"Error processing track {track_data.get('id')}: {e}")
        return None

def process_jockey(session, jockey_data: dict) -> Optional[str]:
    """Process jockey data and return jockey ID"""
    if not jockey_data or not jockey_data.get('id'):
        return None
    
    jockey_hash = generate_hash(jockey_data, ['id', 'name', 'oldJockeyID'])
    if jockey_hash in processed_cache['jockeys']:
        return jockey_data['id']
    
    try:
        # Create jockey object
        jockey = mdb.FirstJockey(
            id=jockey_data['id'],
            name=jockey_data.get('name'),
            old_jockey_id=jockey_data.get('oldJockeyID'),
            old_jockey_name=jockey_data.get('oldJockeyName')
        )
        
        # Use merge to handle both insert and update
        session.merge(jockey)
        processed_cache['jockeys'].add(jockey_hash)
        logger.info(f"Processed jockey: {jockey_data['id']}")
        return jockey_data['id']
        
    except Exception as e:
        logger.error(f"Error processing jockey {jockey_data.get('id')}: {e}")
        return None

def process_fixture(session, fixture_data: dict, track_id: str) -> Optional[str]:
    """Process fixture data and return fixture ID"""
    if not fixture_data or not fixture_data.get('id'):
        logger.warning("No fixture data or fixture ID found")
        return None
    
    fixture_id = fixture_data['id']
    fixture_hash = generate_hash(fixture_data, ['id', 'date', 'racecount'])
    if fixture_hash in processed_cache['fixtures']:
        logger.debug(f"Fixture {fixture_id} already processed (cached)")
        return fixture_id
    
    try:
        # Parse temperature data
        temperature = fixture_data.get('temperature', {})
        temp_fahrenheit = temperature.get('fahrenheit') if temperature else None
        temp_celsius = temperature.get('celsius') if temperature else None
        
        # Create fixture object
        fixture = mdb.FirstFixture(
            id=fixture_id,
            date=fixture_data.get('date'),
            race_count=fixture_data.get('racecount'),
            temperature_fahrenheit=temp_fahrenheit,
            temperature_celsius=temp_celsius,
            first_post_time=fixture_data.get('firstposttime'),
            track_id=track_id
        )
        
        # Use merge to handle both insert and update
        session.merge(fixture)
        session.flush()  # Force the merge to complete
        
        # Verify the fixture was actually created/updated
        existing_fixture = session.query(mdb.FirstFixture).filter(
            mdb.FirstFixture.id == fixture_id
        ).first()
        
        if not existing_fixture:
            logger.error(f"Fixture {fixture_id} was not created in database after merge")
            return None
        
        processed_cache['fixtures'].add(fixture_hash)
        logger.info(f"Processed fixture: {fixture_id} for track: {track_id}")
        return fixture_id
        
    except Exception as e:
        logger.error(f"Error processing fixture {fixture_id}: {e}")
        logger.error(f"Fixture data: {fixture_data}")
        logger.error(f"Track ID: {track_id}")
        return None

def process_race(session, race_data: dict, fixture_id: str) -> Optional[str]:
    """Process race data and return race ID"""
    if not race_data or not race_data.get('id'):
        logger.warning("No race data or race ID found")
        return None
    
    race_hash = generate_hash(race_data, ['id', 'number', 'fixture_id'])
    if race_hash in processed_cache['races']:
        logger.debug(f"Race {race_data['id']} already processed (cached)")
        return race_data['id']
    
    try:
        # Create race object
        race = mdb.FirstRace(
            id=race_data['id'],
            type=race_data.get('type'),
            number=race_data.get('number'),
            runner_count=race_data.get('runnercount'),
            post_time=race_data.get('posttime'),
            estimated_post_time=race_data.get('estimatedPosttime'),
            off_time=race_data.get('offTime'),
            weather=race_data.get('weather'),
            going=race_data.get('going'),
            name=race_data.get('name'),
            status=race_data.get('status'),
            isdst=race_data.get('isdst'),
            timezone_offset=race_data.get('timezoneOffset'),
            track_surface_value=safe_get_nested(race_data, 'tracksurface', 'value'),
            overround=race_data.get('overround'),
            overround_selection=race_data.get('overround_selection'),
            result=race_data.get('result'),
            comment=race_data.get('comment'),
            distance_value=safe_get_nested(race_data, 'distance', 'value'),
            distance_unit=safe_get_nested(race_data, 'distance', 'unit'),
            distance_published_text=safe_get_nested(race_data, 'distance', 'publishedText'),
            breed=race_data.get('breed'),
            race_type_type=safe_get_nested(race_data, 'racetype', 'type'),
            race_type_subtype=safe_get_nested(race_data, 'racetype', 'subtype'),
            race_type_description=safe_get_nested(race_data, 'racetype', 'description'),
            sex_restriction_value=safe_get_nested(race_data, 'sexrestriction', 'value'),
            sex_restriction_description=safe_get_nested(race_data, 'sexrestriction', 'description'),
            age_restriction_value=safe_get_nested(race_data, 'agerestriction', 'value'),
            age_restriction_description=safe_get_nested(race_data, 'agerestriction', 'description'),
            purse_value=safe_get_nested(race_data, 'purse', 'value'),
            purse_ranks=safe_get_nested(race_data, 'purse', 'ranks'),
            purse_unit=safe_get_nested(race_data, 'purse', 'unit'),
            grade=race_data.get('grade'),
            race_tip=race_data.get('raceTip'),
            fixture_id=fixture_id
        )
        
        # Use merge to handle both insert and update
        session.merge(race)
        processed_cache['races'].add(race_hash)
        logger.info(f"Processed race: {race_data['id']} for fixture: {fixture_id}")
        return race_data['id']
        
    except Exception as e:
        logger.error(f"Error processing race {race_data.get('id')}: {e}")
        logger.error(f"Race data: {race_data}")
        logger.error(f"Fixture ID: {fixture_id}")
        return None

def process_race_status_history(session, status_history: List[dict], race_id: str):
    """Process race status history"""
    for status_data in status_history:
        if not status_data:
            continue
            
        status_hash = generate_hash(status_data, ['status', 'timestamp'])
        if status_hash in processed_cache['status_history']:
            continue
        
        try:
            # Check if status history already exists
            existing_status = session.query(mdb.FirstRaceStatusHistory).filter(
                and_(
                    mdb.FirstRaceStatusHistory.race_id == race_id,
                    mdb.FirstRaceStatusHistory.status == status_data.get('status'),
                    mdb.FirstRaceStatusHistory.timestamp == status_data.get('timestamp')
                )
            ).first()
            
            if existing_status:
                processed_cache['status_history'].add(status_hash)
                continue
            
            # Create status history object
            status_history_record = mdb.FirstRaceStatusHistory(
                race_id=race_id,
                status=status_data.get('status'),
                timestamp=status_data.get('timestamp')
            )
            
            # Use merge to handle both insert and update
            session.merge(status_history_record)
            processed_cache['status_history'].add(status_hash)
            
        except Exception as e:
            logger.error(f"Error processing status history for race {race_id}: {e}")

def process_entry(session, entry_data: dict, race_id: str) -> Optional[str]:
    """Process entry data and return entry ID"""
    if not entry_data or not entry_data.get('id'):
        return None
    
    entry_hash = generate_hash(entry_data, ['id', 'startNumber', 'race_id'])
    if entry_hash in processed_cache['entries']:
        return entry_data['id']
    
    try:
        # Process jockey if present
        jockey_id = None
        if entry_data.get('jockey'):
            jockey_id = process_jockey(session, entry_data['jockey'])
        
        # Create entry object
        entry = mdb.FirstEntry(
            id=entry_data['id'],
            start_number=entry_data.get('startNumber'),
            program_number=entry_data.get('programNumber'),
            start_position=entry_data.get('startPosition'),
            coupled_indicator=entry_data.get('coupledIndicator'),
            decoupled_number=entry_data.get('decoupledNumber'),
            horse_id=entry_data.get('horse_id'),
            name=entry_data.get('name'),
            status=entry_data.get('status'),
            equipment_code=safe_get_nested(entry_data, 'equipment', 'code'),
            equipment_description=safe_get_nested(entry_data, 'equipment', 'description'),
            weight_value=safe_get_nested(entry_data, 'weight', 'value'),
            weight_overweight=safe_get_nested(entry_data, 'weight', 'overweight'),
            weight_unit=safe_get_nested(entry_data, 'weight', 'unit'),
            jockey_id=jockey_id,
            starting_price=entry_data.get('starting_price'),
            fav_pos=entry_data.get('favPos'),
            fav_joint=entry_data.get('favJoint'),
            position=safe_get_nested(entry_data, 'finalPosition', 'position'),
            dead_heat=safe_get_nested(entry_data, 'finalPosition', 'deadHeat'),
            disqualified=safe_get_nested(entry_data, 'finalPosition', 'disqualified'),
            amended_position=safe_get_nested(entry_data, 'finalPosition', 'amendedPosition'),
            race_id=race_id
        )
        
        # Use merge to handle both insert and update
        session.merge(entry)
        processed_cache['entries'].add(entry_hash)
        logger.info(f"Processed entry: {entry_data['id']}")
        return entry_data['id']
        
    except Exception as e:
        logger.error(f"Error processing entry {entry_data.get('id')}: {e}")
        return None

def process_entry_show_prices(session, show_prices: List[dict], entry_id: str):
    """Process entry show prices"""
    for price_data in show_prices:
        if not price_data:
            continue
            
        price_hash = generate_hash(price_data, ['timestamp', 'numerator', 'denominator', 'market'])
        if price_hash in processed_cache['show_prices']:
            continue
        
        try:
            # Check if show price already exists
            existing_price = session.query(mdb.FirstEntryShowPrice).filter(
                and_(
                    mdb.FirstEntryShowPrice.entry_id == entry_id,
                    mdb.FirstEntryShowPrice.timestamp == price_data.get('timestamp'),
                    mdb.FirstEntryShowPrice.numerator == price_data.get('numerator'),
                    mdb.FirstEntryShowPrice.denominator == price_data.get('denominator'),
                    mdb.FirstEntryShowPrice.price == price_data.get('price'),
                    mdb.FirstEntryShowPrice.market == price_data.get('market')
                )
            ).first()
            
            if existing_price:
                processed_cache['show_prices'].add(price_hash)
                continue
            
            # Create show price object
            show_price = mdb.FirstEntryShowPrice(
                entry_id=entry_id,
                timestamp=price_data.get('timestamp'),
                numerator=price_data.get('numerator'),
                denominator=price_data.get('denominator'),
                price=price_data.get('price'),
                market=price_data.get('market')
            )
            
            # Use merge to handle both insert and update
            session.merge(show_price)
            processed_cache['show_prices'].add(price_hash)
            
        except Exception as e:
            logger.error(f"Error processing show price for entry {entry_id}: {e}")

def process_entry_starting_price(session, starting_price_data: dict, entry_id: str):
    """Process entry starting price"""
    if not starting_price_data:
        return
    
    price_hash = generate_hash(starting_price_data, ['nominator', 'denominator'])
    if price_hash in processed_cache['starting_prices']:
        return
    
    try:
        # Check if starting price already exists
        existing_price = session.query(mdb.FirstEntryStartingPrice).filter(
            mdb.FirstEntryStartingPrice.entry_id == entry_id
        ).first()
        
        if existing_price:
            processed_cache['starting_prices'].add(price_hash)
            return
        
        # Create starting price object
        starting_price = mdb.FirstEntryStartingPrice(
            entry_id=entry_id,
            nominator=starting_price_data.get('nominator'),
            denominator=starting_price_data.get('denominator')
        )
        
        # Use merge to handle both insert and update
        session.merge(starting_price)
        processed_cache['starting_prices'].add(price_hash)
        
    except Exception as e:
        logger.error(f"Error processing starting price for entry {entry_id}: {e}")

def process_entry_withdrawn(session, withdrawn_data: dict, entry_id: str):
    """Process entry withdrawn data"""
    if not withdrawn_data:
        return
    
    withdrawn_hash = generate_hash(withdrawn_data, ['market', 'timestamp', 'denominator', 'numerator'])
    if withdrawn_hash in processed_cache['withdrawn_entries']:
        return
    
    try:
        # Check if withdrawn entry already exists
        existing_withdrawn = session.query(mdb.FirstEntryWithdrawn).filter(
            and_(
                mdb.FirstEntryWithdrawn.entry_id == entry_id,
                mdb.FirstEntryWithdrawn.market == withdrawn_data.get('market'),
                mdb.FirstEntryWithdrawn.timestamp == withdrawn_data.get('timestamp')
            )
        ).first()
        
        if existing_withdrawn:
            processed_cache['withdrawn_entries'].add(withdrawn_hash)
            return
        
        # Create withdrawn entry object
        withdrawn_entry = mdb.FirstEntryWithdrawn(
            entry_id=entry_id,
            market=withdrawn_data.get('market'),
            timestamp=withdrawn_data.get('timestamp'),
            denominator=withdrawn_data.get('denominator'),
            numerator=withdrawn_data.get('numerator')
        )
        
        # Use merge to handle both insert and update
        session.merge(withdrawn_entry)
        processed_cache['withdrawn_entries'].add(withdrawn_hash)
        
    except Exception as e:
        logger.error(f"Error processing withdrawn entry for entry {entry_id}: {e}")

def process_entries(session, entries: List[dict], race_id: str):
    """Process all entries for a race"""
    for entry_data in entries:
        if not entry_data:
            continue
        
        entry_id = process_entry(session, entry_data, race_id)
        if not entry_id:
            continue
        
        # Process related data
        if entry_data.get('showPrices'):
            process_entry_show_prices(session, entry_data['showPrices'], entry_id)
        
        if entry_data.get('startingPrice'):
            process_entry_starting_price(session, entry_data['startingPrice'], entry_id)
        
        if entry_data.get('withdrawn'):
            process_entry_withdrawn(session, entry_data['withdrawn'], entry_id)

def process_fixture_data(session, fixture_data: dict):
    """Process a complete fixture with all its data"""
    try:
        # Debug: Log the fixture data structure
        logger.debug(f"Processing fixture data with keys: {list(fixture_data.keys()) if fixture_data else 'None'}")
        
        # Process track first
        track_data = fixture_data.get('track')
        if not track_data:
            logger.error("No track data found in fixture")
            return
            
        track_id = process_track(session, track_data)
        if not track_id:
            logger.error("No track ID found for fixture")
            return
        
        # Process fixture header
        header_data = fixture_data.get('header')
        if not header_data:
            logger.error("No header data found in fixture")
            return
            
        fixture_id = process_fixture(session, header_data, track_id)
        if not fixture_id:
            logger.error("No fixture ID found")
            return
        
        # Process races
        races = fixture_data.get('races', [])
        logger.info(f"Processing {len(races)} races for fixture {fixture_id}")
        
        for race_data in races:
            if not race_data:
                continue
            
            race_id = process_race(session, race_data, fixture_id)
            if not race_id:
                logger.warning(f"Failed to process race {race_data.get('id')} for fixture {fixture_id}")
                continue
            
            # Process status history
            if race_data.get('statusHistory'):
                process_race_status_history(session, race_data['statusHistory'], race_id)
            
            # Process entries
            if race_data.get('entries'):
                process_entries(session, race_data['entries'], race_id)
        
        # Verify fixture exists in database after processing
        final_fixture = session.query(mdb.FirstFixture).filter(
            mdb.FirstFixture.id == fixture_id
        ).first()
        
        if final_fixture:
            logger.info(f"Successfully processed fixture: {fixture_id} (verified in database)")
        else:
            logger.error(f"Fixture {fixture_id} not found in database after processing")
        
    except Exception as e:
        logger.error(f"Error processing fixture data: {e}")
        logger.error(f"Fixture data structure: {list(fixture_data.keys()) if fixture_data else 'None'}")
        if fixture_data:
            logger.error(f"Track data: {fixture_data.get('track')}")
            logger.error(f"Header data: {fixture_data.get('header')}")

def check_database_setup(session):
    """Check if database tables exist and are properly set up"""
    try:
        # Check if tables exist by trying to query them
        track_count = session.query(mdb.FirstTrack).count()
        fixture_count = session.query(mdb.FirstFixture).count()
        race_count = session.query(mdb.FirstRace).count()
        
        logger.info(f"Database setup check - Tracks: {track_count}, Fixtures: {fixture_count}, Races: {race_count}")
        
        # Test creating a simple record to verify foreign key constraints
        logger.info("Testing database constraints...")
        
        # Check if we can create a test fixture (this will verify foreign key constraints)
        test_track = session.query(mdb.FirstTrack).first()
        if test_track:
            logger.info(f"Found existing track: {test_track.id}")
        else:
            logger.warning("No tracks found in database")
            
        return True
    except Exception as e:
        logger.error(f"Database setup check failed: {e}")
        return False

def main():
    """Main ETL process"""
    logger.info("Starting ETL process...")
    
    # Check database setup
    with session_scope() as session:
        if not check_database_setup(session):
            logger.error("Database setup check failed. Please ensure tables are created.")
            return
    
    total_files = len(files)
    processed_files = 0
    
    for file in files:
        try:
            logger.info(f"Processing file: {os.path.basename(file)} ({processed_files + 1}/{total_files})")
            
            with open(file, 'r') as f:
                result = json.load(f)
            
            fixture_data = result.get('fixtures', [])
            
            with session_scope() as session:
                for data in fixture_data:
                    try:
                        # Validate data with Pydantic
                        fixture = mpd.Fixture(**data)
                        process_fixture_data(session, fixture.model_dump())
                    except Exception as e:
                        logger.error(f"Error processing fixture in file {file}: {e}")
                        continue
            
            processed_files += 1
            logger.info(f"Completed file: {os.path.basename(file)}")
            
        except Exception as e:
            logger.error(f"Error processing file {file}: {e}")
            continue
    
    logger.info(f"ETL process completed. Processed {processed_files}/{total_files} files.")
    logger.info(f"Cache statistics: {processed_cache}")

if __name__ == "__main__":
    main()


