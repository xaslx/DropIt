from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from config import settings


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client



    async def upload_file(
            self,
            file_path: bytes,
            file_name: str
    ):
        try:

            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_name,
                    Body=file_path,
                )
        except ClientError:
            raise ClientError

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError:
            raise ClientError


def create_s3_client():
    s3_client: S3Client = S3Client(
        access_key=settings.aws_access_key_id,
        secret_key=settings.aws_secret_access_key,
        endpoint_url=settings.endpoint_url,
        bucket_name='dropit'
    )
    return s3_client