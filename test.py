import json
import time
import traceback
from first import FirstAPI
from datetime import date
from process.fixture_pull import process_fixture_from_pull
from process.fixture_push import process_fixture_from_push
from upload.fixture_pull import upload_fixture_from_pull
from upload.horse import bulk_insert_horse_data
from upload.jockey import bulk_insert_jockey_data
from upload.trainer import bulk_insert_trainer_data
from upload.owner import bulk_insert_owner_data
from database.s3 import upload_to_s3
from utils.logger import logger_1st

if __name__ == '__main__':
    first_api = FirstAPI()

    date_list = [
        date(2025, 8, 15), date(2025, 8, 16), date(2025, 8, 17), date(2025, 8, 18), date(2025, 8, 4), date(2025, 8, 5), 
        date(2025, 8, 6), date(2025, 8, 7), date(2025, 8, 8), date(2025, 8, 9), date(2025, 8, 10), date(2025, 8, 11), 
        date(2025, 8, 12), date(2025, 8, 13), date(2025, 8, 14), date(2025, 8, 19), date(2025, 8, 20), date(2025, 8, 1), 
        date(2025, 8, 2), date(2025, 8, 3),
    ]


    for date in date_list:
        try:
            time.sleep(3)
            fixture_data = first_api.get_fofixtures(date=date)
            if not fixture_data:
                logger_1st.error(f'No fixture data for {date}')
                continue

            fixture_result = process_fixture_from_pull(fixture_data)

            fixtures = fixture_result['fixtures']
            horse_dict = fixture_result['horse_dict']
            jockey_dict = fixture_result['jockey_dict']
            trainer_dict = fixture_result['trainer_dict']
            owner_dict = fixture_result['owner_dict']

            print(f'Uploading fixture: {len(fixtures)}')
            for fixture in fixtures:
                upload_fixture_from_pull(fixture, overwrite=True)

            print(f'Uploading jockey data: {len(jockey_dict)}')
            bulk_insert_jockey_data(jockey_dict)

            print(f'Uploading trainer data: {len(trainer_dict)}')
            bulk_insert_trainer_data(trainer_dict)

            print(f'Uploading owner data: {len(owner_dict)}')
            bulk_insert_owner_data(owner_dict)

            print(f'Uploading horse data: {len(horse_dict)}')
            bulk_insert_horse_data(horse_dict)

            upload_to_s3(file_content=json.dumps(fixture_data), s3_subdir='1st/processed')
            logger_1st.info(f'Processing {date} | items: {len(fixture_data)}')
        except Exception as e:
            logger_1st.error(f'Error processing {date}: {e}')
            logger_1st.error(traceback.format_exc())
            upload_to_s3(file_content=json.dumps(fixture_data), s3_subdir='1st/unprocessed')
            continue






# from datetime import datetime, timezone


# current_time = datetime.now(timezone.utc)
# file_name = f'{current_time.strftime("%Y%m%d-%H%M%S")}-{int(current_time.microsecond / 1000):03d}.json'
# # show 3 digit milliseconds
# print(file_name)



# print(file_name)





