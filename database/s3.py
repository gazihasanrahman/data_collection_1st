import os
import json
import traceback
import boto3
from datetime import datetime, timezone
from utils.logger import logger_1st

s3 = boto3.client('s3', config=boto3.session.Config(
    connect_timeout=30,
    read_timeout=30,
    retries={'max_attempts': 3}
))

def upload_to_s3(file_content: str, s3_subdir: str, bucket_name: str = 'tpd-archive', file_name: str = None):
    try:
        if not file_name:
            current_time = datetime.now(timezone.utc)
            file_name = f'{current_time.strftime("%Y%m%d-%H%M%S")}-{int(current_time.microsecond / 1000):03d}.json'
        s3.put_object(Bucket=bucket_name, Key=f'{s3_subdir}/{file_name}', Body=file_content)
        logger_1st.info(f'archived: {file_name}')
    except Exception as e:
        logger_1st.error(f'upload_to_s3(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    return True





