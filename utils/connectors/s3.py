import boto3
import os


MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT_URL", "http://localhost:9000")
ACCESS_KEY = os.environ.get("MINIO_ENDPOINT_URL", "root")
SECRET_KEY = os.environ.get("MINIO_ENDPOINT_URL", "root12345")
BUCKET_NAME = os.environ.get("MINIO_ENDPOINT_URL", "mobile-apps")

# Подключение к MinIO через boto3
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)
