import traceback
from database.general import session_scope, FirstTrainer
from utils.logger import logger_1st


def upload_trainer_data(trainer: dict, overwrite: bool = False):
    '''
    upload trainer data received from pull method, which we pull from 1st's API.
    '''
    if not trainer:
        return False
    
    try:
        with session_scope() as session:
            existing_trainer = session.query(FirstTrainer).filter(FirstTrainer.trainer_id == trainer['trainer_id']).first()
            if existing_trainer:
                if overwrite:
                    existing_trainer.trainer_name = trainer.get('trainer_name')
            else:
                new_trainer = FirstTrainer(
                    trainer_id = trainer.get('trainer_id'),
                    trainer_name = trainer.get('trainer_name'),
                )
                session.add(new_trainer)
        return True
    except Exception as e:
        logger_1st.error(f'upload_trainer_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False


def bulk_insert_trainer_data(trainer_dict: dict):
    '''
    bulk insert trainer data received from pull method, which we pull from 1st's API.
    '''
    if not trainer_dict:
        return False
    
    try:
        trainer_id_list = list(trainer_dict.keys())
        if not trainer_id_list:
            return False
            
        with session_scope() as session:
            existing_trainer_id_list = session.query(FirstTrainer.trainer_id).all()
            existing_trainer_id_list = [trainer_id[0] for trainer_id in existing_trainer_id_list]
            new_trainer_id_list = [trainer_id for trainer_id in trainer_id_list if trainer_id not in existing_trainer_id_list]
            
        trainer_data_to_insert = [trainer_dict[trainer_id] for trainer_id in new_trainer_id_list]
        if not trainer_data_to_insert:
            return False
            
        with session_scope() as session:
            session.bulk_insert_mappings(FirstTrainer, trainer_data_to_insert)
            session.commit()
        return True
    
    except Exception as e:
        logger_1st.error(f'bulk_insert_trainer_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    
    