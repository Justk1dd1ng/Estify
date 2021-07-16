import boto3
import pandas as pd

from typing import List

from bucket.files import BucketObject


class FlatsSource:
    BUCKET_PATH = 's3://flats/'
    BUCKET_NAME = 'flats'

    def __init__(self, source_name):
        self.name = source_name
        self.path = f'{self.BUCKET_PATH}{source_name}/'
        self.s3 = boto3.client('s3')

    def get_dataframe_from_csv(self, file_name: str) -> pd.DataFrame:
        if '.csv' in file_name:
            path = f'{self.path}{file_name}'
        else:
            path = f'{self.path}{file_name}.csv'

        return pd.read_csv(path)

    @property
    def objects_list(self) -> List[BucketObject]:
        full_list = [BucketObject(content) for content in self.s3.list_objects(Bucket=self.BUCKET_NAME).get('Contents')]

        return [obj for obj in full_list if self.name in obj.key]

    def _get_last_csv_object(self):

        return max([obj for obj in self.objects_list], key=lambda obj: obj.last_modified)

    def process_all_csv_into_source_df(self):
        for obj in self.objects_list:
            pass



