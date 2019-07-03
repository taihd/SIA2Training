import boto3
import logging
from botocore.exceptions import ClientError
import botocore


# s3 = boto3.resource("s3",aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY )
# for bucket in s3.buckets.all():
#     print('Existing buckets: ')
#     print(bucket.name)
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
        # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(bucket, key, filename):
    """Download a file to a local computer
        :param file_name: File to download
        :param bucket: Bucket to download
        :return: True if file was downloaded, else False"""
    s3 = boto3.client('s3')
    try:
        s3.download_file(Bucket=bucket, Key=key, Filename=filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object is not exist.")
        else:
            raise
        return False
    return True


download_file(bucket="group2training", key="dog.jpg", filename="local_dog.jpg")