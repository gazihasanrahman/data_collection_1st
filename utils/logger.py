# import os
import logging
import watchtower
import boto3
import json
import time
import config
from botocore.exceptions import ClientError
from functools import wraps, partial

def get_logger(log_name: str, email: bool = False, cloudwatch: bool = config.LOG_CLOUDWATCH, console: bool = config.LOG_CONSOLE, log_group: str = config.LOG_GROUP) -> logging.Logger:
    logger = logging.getLogger(log_name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)
    
    if not (console or cloudwatch):
        logger.addHandler(logging.NullHandler())
        return logger

    standard_formatter = logging.Formatter('%(asctime)s - %(filename)s (%(lineno)d) - %(levelname)s | %(message)s')
    cloudwatch_formatter = logging.Formatter('%(asctime)s - %(filename)s (%(lineno)d) - %(levelname)s | %(message)s')

    if console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(standard_formatter)
        logger.addHandler(ch)
               
    if cloudwatch:
        if not log_group:
            raise ValueError('log_group must be provided for CloudWatch logging')
        cw = watchtower.CloudWdatabase_errorsatchLogHandler(log_group=log_group, stream_name=log_name)
        cw.setFormatter(cloudwatch_formatter)
        logger.addHandler(cw)
    
    if email:
        try:
            ses_handler = SESHandler(
                sender= f'{config.SES_SENDER_NAME} <{config.SES_SENDER_EMAIL}>',
                recipients=config.SES_RECIPIENT_LIST,
                subject_prefix=log_name,
                aws_region=config.AWS_DEFAULT_REGION
            )
            ses_handler.setLevel(logging.INFO)
            ses_handler.setFormatter(standard_formatter)
            logger.addHandler(ses_handler)
        except KeyError as e:
            raise ValueError(f"Environment variables not set. {e}")
        
    return logger


class SESHandler(logging.Handler):
    def __init__(self, sender, recipients, subject_prefix, aws_region):
        super().__init__()
        self.sender = sender
        self.recipients = recipients
        self.subject_prefix = subject_prefix
        self.aws_region = aws_region
        self.ses_client = boto3.client('ses', region_name=self.aws_region)

    def emit(self, record):
        subject = f"{self.subject_prefix}: {record.levelname}"
        body = self.format(record)

        try:
            response = self.ses_client.send_email(
                Source=self.sender,
                Destination={'ToAddresses': self.recipients},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
        except ClientError as e:
            print(f"An error occurred: {e.response['Error']['Message']}")

######################################################################################

# loggers
logger_1st = get_logger(log_name='1st')
logger_database_errors = get_logger(log_name="database_errors")

######################################################################################

def log_to_file(log_data, output_log_file):
    try:
        with open(output_log_file, 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception as e:
        logger_1st.error(f"Error logging to file: {e}")

        
def time_it(func = None, precision: int = 8):
    if func is None:
        return partial(time_it, precision=precision)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        logger_1st.info(f"TIME | {func.__name__}(): {execution_time:.{precision}f} seconds")
        return result
    return wrapper
