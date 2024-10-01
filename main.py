
from fastapi import FastAPI, UploadFile
import boto3


app = FastAPI()

# Configure the  MinIO client
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='2bBitdd9CyvAVprqIE3S',
    aws_secret_access_key='ArbdnbzHIeuo7OrR3Phni07NcUznLehj349Uxf03',
)

BUCKET_NAME = 'uploadimage'

@app.post('/upload')
async def upload(file: UploadFile | None = None):



        s3_client.upload_fileobj(file.file, BUCKET_NAME, file.filename)



        return {"filename": file.filename, "message": "File uploaded successfully"}
