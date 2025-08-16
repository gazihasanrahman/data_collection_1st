import traceback
from database.general import session_scope, FirstPriceHistory
from utils.logger import logger_1st


def upload_price_history_data(price_history: dict, overwrite: bool = False):
    '''
    upload price history data received from pull method, which we pull from 1st's API.
    '''
    if not price_history:
        return False

    try:
        with session_scope() as session:
            existing_price_history = session.query(FirstPriceHistory).filter(FirstPriceHistory.price_id == price_history['price_id']).first()
            if existing_price_history:
                if overwrite:
                    existing_price_history.entry_id = price_history.get('entry_id')
                    existing_price_history.timestamp = price_history.get('timestamp')
                    existing_price_history.price_fraction = price_history.get('price_fraction')
                    existing_price_history.price_percentage = price_history.get('price_percentage')
                    existing_price_history.market = price_history.get('market')
            else:
                new_price_history = FirstPriceHistory(
                    price_id = price_history.get('price_id'),
                    entry_id = price_history.get('entry_id'),
                    timestamp = price_history.get('timestamp'),
                    price_fraction = price_history.get('price_fraction'),
                    price_percentage = price_history.get('price_percentage'),
                    market = price_history.get('market'),
                )
                session.add(new_price_history)
        return True
    
    except Exception as e:
        logger_1st.error(f'upload_price_history_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    

def bulk_insert_price_history_data(price_history_dict: dict):
    '''
    bulk insert price history data received from pull method, which we pull from 1st's API.
    '''
    if not price_history_dict:
        return False
    
    try:
        price_history_id_list = list(price_history_dict.keys())
        if not price_history_id_list:
            return False
        
        with session_scope() as session:
            existing_price_history_id_list = session.query(FirstPriceHistory.price_id).all()
            existing_price_history_id_list = [price_history_id[0] for price_history_id in existing_price_history_id_list]
            new_price_history_id_list = [price_history_id for price_history_id in price_history_id_list if price_history_id not in existing_price_history_id_list]
            
        price_history_data_to_insert = [price_history_dict[price_history_id] for price_history_id in new_price_history_id_list]
        if not price_history_data_to_insert:
            return False
        
        with session_scope() as session:
            session.bulk_insert_mappings(FirstPriceHistory, price_history_data_to_insert)
            session.commit()
        return True
    
    except Exception as e:
        logger_1st.error(f'bulk_insert_price_history_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    