import traceback
from database.general import session_scope, FirstJockey
from utils.logger import logger_1st


def upload_jockey_data(jockey: dict, overwrite: bool = False):
    '''
    upload jockey data received from pull method, which we pull from 1st's API.
    '''
    if not jockey:
        return False
    
    try:
        with session_scope() as session:
            existing_jockey = session.query(FirstJockey).filter(FirstJockey.jockey_id == jockey['jockey_id']).first()
            if existing_jockey:
                if overwrite:
                    existing_jockey.jockey_name = jockey.get('jockey_name')
                    existing_jockey.old_jockey_id = jockey.get('old_jockey_id')
                    existing_jockey.old_jockey_name = jockey.get('old_jockey_name')
            else:
                new_jockey = FirstJockey(
                    jockey_id = jockey.get('jockey_id'),
                    jockey_name = jockey.get('jockey_name'),
                    old_jockey_id = jockey.get('old_jockey_id'),
                    old_jockey_name = jockey.get('old_jockey_name'),
                )
                session.add(new_jockey)
        return True
    except Exception as e:
        logger_1st.error(f'upload_jockey_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    

def bulk_insert_jockey_data(jockey_dict: dict):
    '''
    bulk insert jockey data received from pull method, which we pull from 1st's API.
    '''
    if not jockey_dict:
        return False
    
    try:
        jockey_id_list = list(jockey_dict.keys())
        if not jockey_id_list:
            return False
        
        with session_scope() as session:
            existing_jockey_id_list = session.query(FirstJockey.jockey_id).all()
            existing_jockey_id_list = [jockey_id[0] for jockey_id in existing_jockey_id_list]
            new_jockey_id_list = [jockey_id for jockey_id in jockey_id_list if jockey_id not in existing_jockey_id_list]
            
        jockey_data_to_insert = [jockey_dict[jockey_id] for jockey_id in new_jockey_id_list]
        if not jockey_data_to_insert:
            return False
            
        with session_scope() as session:
            session.bulk_insert_mappings(FirstJockey, jockey_data_to_insert)
            session.commit()
        return True
    
    except Exception as e:
        logger_1st.error(f'bulk_insert_jockey_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    
    