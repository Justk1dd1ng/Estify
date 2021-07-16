import boto3
import pandas as pd

from io import BytesIO

from bucket.files import BucketObject


class S3Bucket:

    def __init__(self, bucket_name: str):

        self.name = bucket_name
        self.resource = boto3.resource('s3')
        self.s3 = boto3.client('s3')
        self.bucket = self.resource.Bucket(self.name)

    def list_all_objects(self):

        return [BucketObject(content) for content in self.s3.list_objects(Bucket=self.name).get('Contents')]


