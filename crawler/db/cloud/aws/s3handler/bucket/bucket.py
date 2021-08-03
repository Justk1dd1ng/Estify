import boto3
import pandas as pd

from io import BytesIO

from db.cloud.aws.s3handler.bucket.files import BucketObject
from db.cloud.aws.s3handler.bucket.flats_source import FlatsSource
from db.cloud.aws.s3handler.utils import put_df_into_s3_as_csv


class S3Bucket:
    BUCKET_PATH = 's3://flats/'
    SOURCE_DUMPS_PATH = f'{BUCKET_PATH}source_dumps/'

    def __init__(self, bucket_name: str):

        self.name = bucket_name
        self.resource = boto3.resource('s3')
        self.s3 = boto3.client('s3')
        self.bucket = self.resource.Bucket(self.name)

    def list_all_objects(self):

        return [BucketObject(content) for content in self.s3.list_objects(Bucket=self.name).get('Contents')]

    def process_new_data(self, source_name):
        source = FlatsSource(source_name)
        new_data = source.get_dataframe_from_csv(source.get_last_csv_objects().name)
        self.insert_new_data_into_source_dump(source_name, new_data)

        source.update_cache()
        print(f'"{source_name}" cache updated')

    def insert_new_data_into_source_dump(self, source_name: str, new_data: pd.DataFrame):
        source_dump = pd.read_csv(f'{self.SOURCE_DUMPS_PATH}{source_name}.csv')
        updated_dump = source_dump.append(new_data, ignore_index=True)
        put_df_into_s3_as_csv(
            df=updated_dump,
            bucket_name=self.name,
            key_name=f'source_dumps/{source_name}.csv'
        )
        print(f'New data inserted into "{source_name}" source dump')