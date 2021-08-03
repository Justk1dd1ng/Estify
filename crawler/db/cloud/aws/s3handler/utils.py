import pandas as pd
import boto3

from io import BytesIO


def put_df_into_s3_as_csv(df: pd.DataFrame, bucket_name: str, key_name: str):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=bucket_name,
        Key=key_name,
        Body=buffer
    )



