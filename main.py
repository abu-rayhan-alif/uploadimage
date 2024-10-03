#
# from fastapi import FastAPI, UploadFile
# import boto3
#
#
# app = FastAPI()
#
# # Configure the  MinIO client
# s3_client = boto3.client(
#     's3',
#     endpoint_url='http://localhost:9000',
#     aws_access_key_id='2bBitdd9CyvAVprqIE3S',
#     aws_secret_access_key='ArbdnbzHIeuo7OrR3Phni07NcUznLehj349Uxf03',
# )
#
#
#
#
# BUCKET_NAME = 'uploadimage'
#
# @app.post('/upload')
# async def upload(file: UploadFile | None = None):
#         s3_client.upload_fileobj(file.file, BUCKET_NAME, file.filename)
#         return {"filename": file.filename, "message": "File uploaded successfully"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from botocore.exceptions import NoCredentialsError, ClientError
import logging
import boto3

app = FastAPI()

# MinIO Configuration
MINIO_URL = 'http://localhost:9000'  # MinIO server URL
ACCESS_KEY = '2bBitdd9CyvAVprqIE3S'        # Replace with your MinIO access key
SECRET_KEY = 'ArbdnbzHIeuo7OrR3Phni07NcUznLehj349Uxf03'        # Replace with your MinIO secret key
BUCKET_NAME = 'uploadimage'           # Replace with your bucket name

# Create MinIO S3 client
s3_client = boto3.client('s3',
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

class PresignedURLRequest(BaseModel):
    file_name: str
    file_type: str

@app.post('/generate-presigned-url')
async def generate_presigned_url(request: PresignedURLRequest):
    """Generate a presigned URL for uploading a file to MinIO."""
    try:
        response = s3_client.generate_presigned_url('put_object',
            Params={'Bucket': BUCKET_NAME,
                    'Key': request.file_name,
                    'ContentType': request.file_type},
            ExpiresIn=60)  # URL valid for 60 seconds

        return {'url': response}
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail='Credentials not available')
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))



