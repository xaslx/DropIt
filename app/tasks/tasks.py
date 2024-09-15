from app.utils.S3 import s3_client




async def delete_file_from_s3(filename: str):
    await s3_client.delete_file(object_name=filename)
