import boto3
import pandas as pd

from typing import List, Union

from db.cloud.aws.s3handler.bucket.files import BucketObject
from db.cloud.aws.s3handler.utils import put_df_into_s3_as_csv


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

    def get_objects_list(self) -> List[BucketObject]:
        full_list = [BucketObject(content) for content in self.s3.list_objects(Bucket=self.BUCKET_NAME).get('Contents')]

        return [obj for obj in full_list if f'{self.name}/' in obj.key]

    def get_last_csv_objects(self, num_objects: int = 1) -> Union[BucketObject, List[BucketObject]]:
        if num_objects > 1:
            return sorted(
                [obj for obj in self.get_objects_list()],
                key=lambda obj: obj.last_modified,
                reverse=True
            )[:num_objects]

        return max([obj for obj in self.get_objects_list()], key=lambda obj: obj.last_modified)

    def process_all_csv_into_source_df(self):
        df = pd.DataFrame()
        for num, obj in enumerate(self.get_objects_list()):
            if obj.name:
                df = df.append(self.get_dataframe_from_csv(obj.name), ignore_index=True)

        return df

    def update_cache(self):
        crawled, cached = [self.get_dataframe_from_csv(obj.name) for obj in self.get_last_csv_objects(2)]
        df: pd.DataFrame = crawled.append(cached, ignore_index=True)
        df.sort_values('id', ascending=False, inplace=True)
        df = df[:20]
        put_df_into_s3_as_csv(
            df=df,
            bucket_name='flats',
            key_name=f'{self.name}/cached.csv'
        )



