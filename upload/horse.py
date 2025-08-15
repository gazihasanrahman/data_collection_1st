import traceback
import time
from database.general import session_scope, FirstHorse
from first import FirstAPI
from process.horse import process_horse_data
from utils.logger import logger_1st



def upload_horse_data(horse: dict, overwrite: bool = False):
    '''
    upload horse data received from pull method, which we pull from 1st's API.
    '''
    if not horse:
        return False
    
    try:
        with session_scope() as session:
            existing_horse = session.query(FirstHorse).filter(FirstHorse.horse_id == horse['horse_id']).first()
            if existing_horse:
                if overwrite:
                    existing_horse.external_id = horse.get('external_id')
                    existing_horse.horse_name = horse.get('horse_name')
                    existing_horse.gender = horse.get('gender')
                    existing_horse.breed = horse.get('breed')
                    existing_horse.foaling_date = horse.get('foaling_date')
                    existing_horse.foaling_country = horse.get('foaling_country')
                    existing_horse.color = horse.get('color')
                    existing_horse.breeder = horse.get('breeder')
                    existing_horse.horse_id_sire = horse.get('horse_id_sire')
                    existing_horse.horse_id_dam = horse.get('horse_id_dam')
                    existing_horse.horse_id_sire_dam = horse.get('horse_id_sire_dam')
                    existing_horse.horse_id_sire_sire = horse.get('horse_id_sire_sire')
                    existing_horse.horse_id_dam_sire = horse.get('horse_id_dam_sire')
                    existing_horse.horse_id_dam_dam = horse.get('horse_id_dam_dam')
            else:
                new_horse = FirstHorse(
                    horse_id = horse.get('horse_id'),
                    external_id = horse.get('external_id'),
                    horse_name = horse.get('horse_name'),
                    gender = horse.get('gender'),
                    breed = horse.get('breed'),
                    foaling_date = horse.get('foaling_date'),
                    foaling_country = horse.get('foaling_country'),
                    color = horse.get('color'),
                    breeder = horse.get('breeder'),
                    horse_id_sire = horse.get('horse_id_sire'),
                    horse_id_dam = horse.get('horse_id_dam'),
                    horse_id_sire_dam = horse.get('horse_id_sire_dam'),
                    horse_id_sire_sire = horse.get('horse_id_sire_sire'),
                    horse_id_dam_sire = horse.get('horse_id_dam_sire'),
                    horse_id_dam_dam = horse.get('horse_id_dam_dam'),
                )
                session.add(new_horse)
        return True
    except Exception as e:
        logger_1st.error(f'upload_horse_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    

def bulk_insert_horse_data(horse_dict: dict):
    '''
    bulk insert horse data received from pull method, which we pull from 1st's API.
    '''
    if not horse_dict:
        return False
    
    try:
        horse_id_list = list(horse_dict.keys())
        if not horse_id_list:
            return False
        
        with session_scope() as session:
            existing_horse_id_list = session.query(FirstHorse.horse_id).all()
            existing_horse_id_list = [horse_id[0] for horse_id in existing_horse_id_list]
            new_horse_id_list = [horse_id for horse_id in horse_id_list if horse_id not in existing_horse_id_list]

        first_api = FirstAPI()
        horse_data_to_insert = []
        for horse_id in new_horse_id_list:
            horse_data = first_api.get_horses(horse_id)
            horse_data_processed = process_horse_data(horse_data)
            time.sleep(5)
            if not horse_data_processed:
                continue
            horse_data_to_insert.append(horse_data_processed)

        if not horse_data_to_insert:
            return False

        with session_scope() as session:
            session.bulk_insert_mappings(FirstHorse, horse_data_to_insert)
            session.commit()
        return True
    
    except Exception as e:
        logger_1st.error(f'bulk_insert_horse_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    
    