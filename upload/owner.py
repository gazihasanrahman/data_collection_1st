import traceback
from database.general import session_scope, FirstOwner
from utils.logger import logger_1st


def upload_owner_data(owner: dict, overwrite: bool = False):
    '''
    upload owner data received from pull method, which we pull from 1st's API.
    '''
    if not owner:
        return False
    
    try:
        with session_scope() as session:
            existing_owner = session.query(FirstOwner).filter(FirstOwner.owner_id == owner['owner_id']).first()
            if existing_owner:
                if overwrite:
                    existing_owner.owner_name = owner.get('owner_name')
            else:
                new_owner = FirstOwner(
                    owner_id = owner.get('owner_id'),
                    owner_name = owner.get('owner_name'),
                )
                session.add(new_owner)
        return True
    except Exception as e:
        logger_1st.error(f'upload_owner_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False


def bulk_insert_owner_data(owner_dict: dict):
    '''
    bulk insert owner data received from pull method, which we pull from 1st's API.
    '''
    if not owner_dict:
        return False
    
    try:
        owner_id_list = list(owner_dict.keys())
        if not owner_id_list:
            return False

        with session_scope() as session:
            existing_owner_id_list = session.query(FirstOwner.owner_id).all()
            existing_owner_id_list = [owner_id[0] for owner_id in existing_owner_id_list]
            new_owner_id_list = [owner_id for owner_id in owner_id_list if owner_id not in existing_owner_id_list]
            
        owner_data_to_insert = [owner_dict[owner_id] for owner_id in new_owner_id_list]
        if not owner_data_to_insert:
            return False
        
        with session_scope() as session:
            session.bulk_insert_mappings(FirstOwner, owner_data_to_insert)
            session.commit()
        return True
    
    except Exception as e:
        logger_1st.error(f'bulk_insert_owner_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    

    