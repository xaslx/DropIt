from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from config import settings
from logger import logger



class S3Client:
    def __init__(
            self,
            aws_access_key_id: str,
            aws_secret_access_key: str,
            endpoint_url: str,
            region_name: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "endpoint_url": endpoint_url,
            "region_name": region_name
        }
        self.bucket_name = bucket_name
        self.session = get_session()


    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client



    async def upload_file( self, file_path: bytes, file_name: str):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_name,
                    Body=file_path,
                )
        except ClientError:
            logger.error(f'Не удалось загрузить файл в S3 хранилище')
        
        
    async def get_file(self, object_key: str, exp: int = 3600):
        try:
            async with self.get_client() as client:
                presigned_url: str = await client.generate_presigned_url(
                    'get_object', Params={
                        'Bucket': self.bucket_name, 'Key': object_key, 
                        'ResponseContentDisposition': f'attachment; filename="{object_key}"'},
                    ExpiresIn=exp)
                return presigned_url
        except ClientError:
            logger.error(f'Не удалось сгенерировать ссылку для скачивания')

       

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError:
            logger.error(f'Не удалось удалить файл из S3 хранилище')


def create_s3_client():
    s3_client: S3Client = S3Client(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        endpoint_url=settings.endpoint_url,
        bucket_name='dropit',
        region_name='ru-1'
    )
    return s3_client


s3_client: S3Client = create_s3_client()