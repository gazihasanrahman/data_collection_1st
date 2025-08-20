import traceback
from database.general import session_scope, FirstRaceStatusHistory
from utils.logger import logger_1st


def upload_race_status_history_data(race_status_history: dict, overwrite: bool = False):
    '''
    upload race status history data received from pull method, which we pull from 1st's API.
    '''
    if not race_status_history:
        return False
    
    try:
        with session_scope() as session:
            existing_race_status_history = session.query(FirstRaceStatusHistory).filter(FirstRaceStatusHistory.race_status_id == race_status_history['race_status_id']).first()
            if existing_race_status_history:
                if overwrite:
                    existing_race_status_history.race_id = race_status_history.get('race_id')
                    existing_race_status_history.status = race_status_history.get('status')
                    existing_race_status_history.timestamp = race_status_history.get('timestamp')
            else:
                new_race_status_history = FirstRaceStatusHistory(
                    race_status_id = race_status_history.get('race_status_id'),
                    race_id = race_status_history.get('race_id'),
                    status = race_status_history.get('status'),
                    timestamp = race_status_history.get('timestamp'),
                )
                session.add(new_race_status_history)
        return True
    
    except Exception as e:
        logger_1st.error(f'upload_race_status_history_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    

def bulk_insert_race_status_history_data(race_status_history_dict: dict):
    '''
    bulk insert race status history data received from pull method, which we pull from 1st's API.
    '''
    if not race_status_history_dict:
        return False
    
    try:
        race_status_history_id_list = list(race_status_history_dict.keys())
        if not race_status_history_id_list:
            return False
        
        with session_scope() as session:
            existing_race_status_history_id_list = session.query(FirstRaceStatusHistory.race_status_id).all()
            existing_race_status_history_id_list = [race_status_history_id[0] for race_status_history_id in existing_race_status_history_id_list]
            new_race_status_history_id_list = [race_status_history_id for race_status_history_id in race_status_history_id_list if race_status_history_id not in existing_race_status_history_id_list]

        race_status_history_data_to_insert = [race_status_history_dict[race_status_history_id] for race_status_history_id in new_race_status_history_id_list]
        if not race_status_history_data_to_insert:
            return False
        
        with session_scope() as session:
            session.bulk_insert_mappings(FirstRaceStatusHistory, race_status_history_data_to_insert)
            session.commit()
        return True
    
    except Exception as e:
        logger_1st.error(f'bulk_insert_race_status_history_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    