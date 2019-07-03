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
        test1.upload_file('mountain.jpg','group2training','mountain_test.jpg')


    def tearDown(self):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket('group2training')
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def test_exist(self):
        s3 = boto3.client("s3")
        test1.upload_file('test.jpg', 'group2training', "test_img")
        keys = []
        resp = s3.list_objects_v2(Bucket='group2training')
        for obj in resp['Contents']:
            keys.append(obj['Key'])
        self.assertTrue('test_img' in keys)

    def test_download_exist(self):
        s3 = boto3.client('s3')
        test1.download_file('group2training', 'mountain_test.jpg', 'downloaded_mountain.jpg')
        current_file = os.listdir()
        # print(current_file)
        self.assertTrue('downloaded_mountain.jpg' in current_file)
