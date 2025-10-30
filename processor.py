import json
import time
import boto3
import config
import schedule
import threading
import traceback
from first import FirstAPI
from datetime import date, timedelta
from database.s3 import upload_to_s3
from process.fixture_push import process_fixture_from_push
from process.fixture_pull import process_fixture_from_pull
from upload.fixture_push import upload_fixture_from_push
from upload.price_history import bulk_insert_price_history_data
from upload.race_status_history import bulk_insert_race_status_history_data
from upload.fixture_pull import upload_fixture_from_pull
from upload.horse import bulk_insert_horse_data
from upload.jockey import bulk_insert_jockey_data
from upload.trainer import bulk_insert_trainer_data
from upload.owner import bulk_insert_owner_data
from process.helper import manually_map_all_tpd_ids
from utils.logger import logger_1st

sqs_client = boto3.client('sqs')


def process_sqs_messages():
    try:
        while True:
            response = sqs_client.receive_message(QueueUrl=config.SQS_QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=20)
            if 'Messages' in response:
                for message in response['Messages']:

                    try:
                        data = json.loads(message['Body'])
                        fixture_data = process_fixture_from_push(data)
                        fixtures = fixture_data['fixtures']
                        race_status_history_dict = fixture_data['race_status_history_dict']
                        price_history_dict = fixture_data['price_history_dict']

                        for fixture in fixtures:
                            upload_fixture_from_push(fixture, overwrite=True)

                        bulk_insert_race_status_history_data(race_status_history_dict)
                        bulk_insert_price_history_data(price_history_dict)
                        upload_to_s3(file_content=json.dumps(data), s3_subdir='1st/processed')
                        sqs_client.delete_message(QueueUrl=config.SQS_QUEUE_URL, ReceiptHandle=message['ReceiptHandle'])

                    except Exception as e:
                        logger_1st.error(f'process_sqs_messages(): {e}')
                        logger_1st.error(traceback.format_exc())
                        upload_to_s3(file_content=message['Body'], s3_subdir='1st/unprocessed')
                        continue

    except KeyboardInterrupt:
        logger_1st.info('Keyboard interrupt detected. Exiting...')
    except Exception as e:
        logger_1st.error(f'process_sqs_messages(): {e}')
        logger_1st.error(traceback.format_exc())
        

def manual_data_collection():
    first_api = FirstAPI()
    list_of_days = [date.today() - timedelta(days=1),
                    date.today(),
                    date.today() + timedelta(days=1),
                    date.today() + timedelta(days=2),]  
    for meeting_date in list_of_days:
        try:
            fixture_data = first_api.get_fofixtures(date=meeting_date)
            if not fixture_data:
                logger_1st.error(f'No fixture data for {meeting_date}')
                return False
            fixture_result = process_fixture_from_pull(fixture_data)
            fixtures = fixture_result['fixtures']
            horse_dict = fixture_result['horse_dict']
            jockey_dict = fixture_result['jockey_dict']
            trainer_dict = fixture_result['trainer_dict']
            owner_dict = fixture_result['owner_dict']
            logger_1st.info(f'Uploading fixture: {len(fixtures)}')
            for fixture in fixtures:
                upload_fixture_from_pull(fixture, overwrite=True)
            bulk_insert_jockey_data(jockey_dict)
            bulk_insert_trainer_data(trainer_dict)
            bulk_insert_owner_data(owner_dict)
            bulk_insert_horse_data(horse_dict)
            upload_to_s3(file_content=json.dumps(fixture_data), s3_subdir='1st/processed')
            logger_1st.info(f'Processing {meeting_date} | items: {len(fixture_data)}')
        except Exception as e:
            logger_1st.error(f'Error processing {meeting_date}: {e}')
            logger_1st.error(traceback.format_exc())
            upload_to_s3(file_content=json.dumps(fixture_data), s3_subdir='1st/unprocessed')
            

def schedule_jobs():
    schedule.every(1).day.at('02:30').do(manual_data_collection)
    schedule.every(1).hour.do(manually_map_all_tpd_ids)
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_concurrent_tasks():
    sqs_thread = threading.Thread(target=process_sqs_messages, daemon=True)
    schedule_thread = threading.Thread(target=schedule_jobs, daemon=True)
    sqs_thread.start()
    schedule_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger_1st.info('Keyboard interrupt detected. Shutting down...')


if __name__ == "__main__":
    run_concurrent_tasks()

