import json
import time
import os
import requests
import boto3
import config
import schedule
import threading
from utils.logger import logger_1st

sqs_client = boto3.client('sqs')


def download_data(data):
    file_name = str(int(time.time() * 1000)) + '.json'
    with open(os.path.join('downloads', file_name), 'w') as f:
        json.dump(data, f)


def process_sqs_messages():
    while True:
        try:
            response = sqs_client.receive_message(QueueUrl=config.SQS_QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=20)
            if 'Messages' in response:
                for message in response['Messages']:
                    data = json.loads(message['Body'])
                    download_data(data)
                    time.sleep(.001)
                    sqs_client.delete_message(QueueUrl=config.SQS_QUEUE_URL, ReceiptHandle=message['ReceiptHandle'])
        
        except KeyboardInterrupt:
            logger_1st.info('Keyboard interrupt detected. Exiting...')
            break
        except Exception as e:
            logger_1st.error(f'Error in 1st processing: {e}')
            
    # try:
    #     response = sqs_client.receive_message(QueueUrl=config.SQS_QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=20)
    #     if 'Messages' in response:
    #         message = response['Messages'][0]
    #         data = json.loads(message['Body'])
    #         download_data(data)
    #         time.sleep(.001)
    #         sqs_client.delete_message(QueueUrl=config.SQS_QUEUE_URL, ReceiptHandle=message['ReceiptHandle'])
    # except KeyboardInterrupt:
    #     logger_1st.info('Keyboard interrupt detected. Exiting...')
    # except Exception as e:
    #     logger_1st.error(f'Error in 1st processing: {e}')
    #     time.sleep(5)


def manual_data_collection():
    raise NotImplementedError('Manual data collection is not implemented')


def schedule_jobs():
    schedule.every(30).minutes.do(manual_data_collection)
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_concurrent_tasks():
    """Run both SQS processing and scheduled jobs concurrently"""
    # Create threads for each task
    sqs_thread = threading.Thread(target=process_sqs_messages, daemon=True)
    schedule_thread = threading.Thread(target=schedule_jobs, daemon=True)
    
    # Start both threads
    sqs_thread.start()
    schedule_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger_1st.info('Keyboard interrupt detected. Shutting down...')


if __name__ == "__main__":
    process_sqs_messages()

