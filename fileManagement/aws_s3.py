import datetime
import io
import logging
import uuid
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings

logger = logging.getLogger('mylogger')

def upload_csv_to_s3(file, file_name_s3):
    """Create the file name and convet to bytesIO before uploading to S3"""
    logger.info(f"Uploading the file '{file_name_s3}'")
    file_ready = get_ready_the_file(file)
    save_csv_to_s3(file_ready, file_name_s3)

def get_ready_the_file(file):
    """Convert to ByesIO otherwise will be empty when downloading"""
    file_to_upload = io.BytesIO()
    for chunk in file:
        # Cleanup junk
        if str(chunk).startswith("b'---------") or str(chunk).startswith("b'Content-"):
            continue
        if chunk:
            file_to_upload.write(chunk)
    file_to_upload.seek(0)
    return file_to_upload

def save_csv_to_s3(file, file_name):
    """Method using Boto3 to upload the csv file."""
    prefix = datetime.datetime.now().strftime('%d-%m-%Y')
    try:
        get_s3_creds(boto3.client).upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            f"{prefix}/{str(file_name)}.csv",
        )
        logger.info("Upload Successful")
        return True
    except NoCredentialsError:
        logger.info("Credentials not available")
        return False

def get_s3_creds(boto3_action):
    return boto3_action(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
    )