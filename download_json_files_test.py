import os
import unittest

import boto3
import botocore
from moto import mock_s3

MY_BUCKET = "my_bucket"
MY_PREFIX = "mock_folder"

@mock_s3
class TestDownloadJsonFiles(unittest.TestCase):
    def setUp(self):
        client = boto3.client(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
            )
        try:
            s3 = boto3.resource(
                "s3",
                region_name="eu-west-1",
                aws_access_key_id="fake_access_key",
                aws_secret_access_key="fake_secret_key",
                )
            s3.meta.client.head_bucket(Bucket=MY_BUCKET)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = "{bucket} should not exist.".format(bucket=MY_BUCKET)
            raise EnvironmentError(err)

        client.create_bucket(Bucket=MY_BUCKET)
        current_dir = os.path.dirname(__file__)
        fixtures_dir = os.path.join(current_dir, "fixtures")
        # _upload_fixtures(MY_BUCKET, fixtures_dir)

    def tearDown(self):
        s3 = boto3.resource(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
            )
        bucket = s3.Bucket(MY_BUCKET)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def _upload_fixtures(bucket: str, fixtures_dir: str) -> None:
        client = boto3.client("s3")
        fixtures_paths = [
            os.path.join(path,  filename)
            for path, _, files in os.walk(fixtures_dir)
            for filename in files
        ]
        for path in fixtures_paths:
            key = os.path.relpath(path, fixtures_dir)
            client.upload_file(Filename=path, Bucket=bucket, Key=key)