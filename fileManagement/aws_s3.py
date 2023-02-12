import datetime
import io
import logging
import uuid
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings

def proccess_csv_to_s3(file, row_count):
    """"""
    id = uuid.uuid4()
    now=datetime.datetime.now()
    file_name_s3 = f"{id}_{row_count}_{now.strftime('%d-%m-%Y')}"
    logging.info(f"Uploading the file '{file_name_s3}'")
    save_csv_to_s3(file, file_name_s3)

def save_csv_to_s3(file, file_name):
    """Need to transform the files to BytesIO for S3"""
    prefix = f"/"
    file_aws = io.BytesIO()
    for chunk in file:
        file_aws.write(bytes([chunk]))
    file_aws.seek(0)
    try:
        get_s3_creds(boto3.client).upload_fileobj(
            file_aws,
            settings.AWS_STORAGE_BUCKET_NAME,
            f"{prefix}/{str(file_name)}",
        )
        logging.info("Upload Successful")
        return True
    except NoCredentialsError:
        logging.info("Credentials not available")
        return False

def get_s3_creds(boto3_action):
    return boto3_action(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
    )