from moto import mock_s3
import boto3
from unittest import TestCase
import os
import test1


@mock_s3
class Testing(TestCase):
    def setUp(self):
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket='group2training')
        s3.put_object(Bucket=self.bucket_name, Key=self.key, Body=self.value)


    def tearDown(self):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket('group2training')
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def test_exist(self):
        test1.upload_file('test.jpg', 'group2training', "test_img")
        keys = []
        resp = s3.list_objects_v2(Bucket='group2training')
        for obj in resp['Contents']:
            keys.append(obj['Key'])
        self.assertTrue('test_img' in keys)

    def test_download_exist(self):
        s3 = boto3.client('s3',
                          aws_access_key_id="fake_access_key",
                          aws_secret_access_key="fake_secret_key"
                          )
        response = s3.list_objects(Bucket='group2training')
        for o in response['Contents']:
            print(o['Key'])
        # download_file(bucket="group2training", key="group2training/long.txt", filename="local.txt")
        # current_file = os.listdir()
        # print(current_file)
        # self.assertTrue('local_dog.jpg' in current_file)
