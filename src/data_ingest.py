import os
import json
import logging

import pandas as pd
import pandas as pd
from minio import Minio
from io import BytesIO

from dotenv import load_dotenv  #for testing task
load_dotenv()    

MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
DATA_LATEST_VERSION=os.getenv("DATA_LATEST_VERSION")

def ingest_data():

    if os.listdir("/mlops_pipeline/data/raw")!=0:
        logging.info("start ingest data")
        raw_data = pd.read_parquet("/mlops_pipeline/data/raw/raw_train.parquet")
        df = pd.DataFrame(raw_data)
        csv = df.to_csv(index=False).encode("utf-8")
        client = Minio("host.docker.internal:9000", access_key=MINIO_ROOT_USER, secret_key=MINIO_ROOT_PASSWORD, secure=False)
        print(MINIO_BUCKET_NAME)
        # Make MINIO_BUCKET_NAME if not exist.
        found = client.bucket_exists(MINIO_BUCKET_NAME)
        if not found:
            client.make_bucket(MINIO_BUCKET_NAME)
        else:
            print(f"Bucket '{MINIO_BUCKET_NAME}' already exists!")

        # Put csv data in the bucket
        client.put_object(
            MINIO_BUCKET_NAME, f"data_{DATA_LATEST_VERSION}.csv", data=BytesIO(csv), length=len(csv), content_type="application/csv"
        )

    else:
        raise "Data training is not available"
    


if __name__=="__main__":
    ingest_data()