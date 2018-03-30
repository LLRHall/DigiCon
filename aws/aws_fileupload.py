from boto3.s3.transfer import S3Transfer
import boto3
import os
#have all the variables populated which are required below

AWS_ACCESS_KEY_ID = 'AKIAJONJ4JMC5ZSSNAAQ'
AWS_SECRET_ACCESS_KEY = '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'

def file_upload(filename, UPLOAD_FOLDER):
    bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
    TEST_FILE = os.path.join(UPLOAD_FOLDER, filename)

    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.Bucket(bucket_name).upload_file(TEST_FILE, TEST_FILE)

