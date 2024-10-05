#
#
# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# import boto3
#
# app = FastAPI()
#
# # MinIO Configuration
# MINIO_URL = 'http://localhost:9000'  # MinIO server URL
# ACCESS_KEY = '2bBitdd9CyvAVprqIE3S'   # Replace with your MinIO access key
# SECRET_KEY = 'ArbdnbzHIeuo7OrR3Phni07NcUznLehj349Uxf03'  # Replace with your MinIO secret key
# DEFAULT_BUCKET_NAME = 'uploadimage'  # Replace with your default bucket name
#
# # Create MinIO S3 client
# s3_client = boto3.client('s3',
#     endpoint_url=MINIO_URL,
#     aws_access_key_id=ACCESS_KEY,
#     aws_secret_access_key=SECRET_KEY,
# )
#
# class PresignedURLRequest(BaseModel):
#     file_name: str
#     file_type: str
#
# class MoveFileRequest(BaseModel):
#     source_bucket: str
#     destination_bucket: str
#     file_name: str
#
# @app.post('/generate-presigned-url')
# async def generate_presigned_url(request: PresignedURLRequest):
#     """Generate a presigned URL for uploading a file to MinIO."""
#     try:
#         response = s3_client.generate_presigned_url('put_object',
#             Params={'Bucket': DEFAULT_BUCKET_NAME,
#                     'Key': request.file_name,
#                     'ContentType': request.file_type},
#             ExpiresIn=60)  # URL valid for 60 seconds
#         return {'url': response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# @app.post('/upload-file/{file_name}')
# async def upload_file(file_name: str, file: UploadFile = File(...)):
#     """Upload a file to MinIO after validating size."""
#     MAX_SIZE_MB = 1
#     max_size_bytes = MAX_SIZE_MB * 1024 * 1024
#
#     # Check file size
#     contents = await file.read()
#     if len(contents) > max_size_bytes:
#         raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_SIZE_MB} MB.")
#
#     try:
#         # Upload the file to MinIO
#         s3_client.upload_fileobj(file.file, DEFAULT_BUCKET_NAME, file_name)
#         return {"message": "File uploaded successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# @app.post('/move-file')
# async def move_file(request: MoveFileRequest):
#     """Move a file from one bucket to another."""
#     try:
#         # Copy the object to the destination bucket
#         s3_client.copy_object(
#             Bucket=request.destination_bucket,
#             CopySource={'Bucket': request.source_bucket, 'Key': request.file_name},
#             Key=request.file_name,
#         )
#
#         # Delete the object from the source bucket
#         s3_client.delete_object(Bucket=request.source_bucket, Key=request.file_name)
#
#         return {"message": "File moved successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# # Mount static files to serve the HTML page
# app.mount("/static", StaticFiles(directory="static"), name="static")
#
# @app.get("/", response_class=HTMLResponse)
# async def read_html():
#     with open("static/upload.html") as f:  # Ensure the HTML file is in the 'static' folder
#         return f.read()


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, conint
# import boto3
#
# app = FastAPI()
#
# # MinIO Configuration
# MINIO_URL = 'http://localhost:9000'
# ACCESS_KEY = '2bBitdd9CyvAVprqIE3S'
# SECRET_KEY = 'ArbdnbzHIeuo7OrR3Phni07NcUznLehj349Uxf03'
# DEFAULT_BUCKET_NAME = 'uploadimage'
#
# # Create MinIO S3 client
# s3_client = boto3.client('s3',
#     endpoint_url=MINIO_URL,
#     aws_access_key_id=ACCESS_KEY,
#     aws_secret_access_key=SECRET_KEY,
# )
#
# class PresignedURLRequest(BaseModel):
#     file_name: str
#     file_type: str
#     file_size: conint(le=1024 * 1024)  # Limit to 1 MB (1024 * 1024 bytes)
#
# @app.post('/generate-presigned-url')
# async def generate_presigned_url(request: PresignedURLRequest):
#     """Generate a presigned URL for uploading a file to MinIO."""
#     if request.file_size > 1024 * 1024:  # Check if file size exceeds 1 MB
#         raise HTTPException(status_code=400, detail="File size must be 1 MB or less.")
#
#     try:
#         response = s3_client.generate_presigned_url('put_object',
#             Params={'Bucket': DEFAULT_BUCKET_NAME,
#                     'Key': request.file_name,
#                     'ContentType': request.file_type},
#             ExpiresIn=60)  # URL valid for 60 seconds
#         return {'url': response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# from pydantic import BaseModel
# import boto3
# from fastapi import FastAPI, HTTPException
#
# app = FastAPI()
#
# # MinIO Configuration
# MINIO_URL = 'http://localhost:9000'
# ACCESS_KEY = '2bBitdd9CyvAVprqIE3S'
# SECRET_KEY = 'ArbdnbzHIeuo7OrR3Phni07NcUznLehj349Uxf03'
# DEFAULT_BUCKET_NAME = 'uploadimage'
#
# # Create MinIO S3 client
# s3_client = boto3.client('s3',
#                          endpoint_url=MINIO_URL,
#                          aws_access_key_id=ACCESS_KEY,
#                          aws_secret_access_key=SECRET_KEY,
#                          )
#
#
# class PresignedURLRequest(BaseModel):
#     file_name: str
#     file_type: str
#
#
# @app.post('/generate-presigned-url')
# async def generate_presigned_url(request: PresignedURLRequest):
#     """Generate a presigned URL for uploading a file to MinIO."""
#
#     # Define the maximum file size in bytes
#     MAX_FILE_SIZE = 1024 * 1024  # 1 MB
#
#     try:
#         # Generate a presigned URL
#         response = s3_client.generate_presigned_url('put_object',
#                                                     Params={
#                                                         'Bucket': DEFAULT_BUCKET_NAME,
#                                                         'Key': request.file_name,
#                                                         'ContentType': request.file_type,
#                                                     },
#                                                     ExpiresIn=60,  # URL valid for 60 seconds
#                                                     HttpMethod='PUT'
#                                                     )
#
#         # Return the URL along with a warning about the file size limit
#         return {
#             'url': response,
#             'message': f'Please upload a file of size 1 MB or less. Any files larger than this will be rejected.'
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from pydantic import BaseModel, constr
import boto3

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# MinIO Configuration
MINIO_URL = 'http://localhost:9000'
ACCESS_KEY = '2bBitdd9CyvAVprqIE3S'
SECRET_KEY = 'ArbdnbzHIeuo7OrR3Phni07NcUznLehj349Uxf03'
DEFAULT_BUCKET_NAME = 'uploadimage'

# Create MinIO S3 client
s3_client = boto3.client('s3',
                         endpoint_url=MINIO_URL,
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY)


class PresignedURLRequest(BaseModel):
    file_name: constr(max_length=255)
    file_type: str


import uuid
from datetime import datetime


@app.post('/generate-presigned-url')
async def generate_presigned_url(request: PresignedURLRequest):
    """Generate a presigned URL for uploading a file to MinIO."""

    # Define the maximum file size in bytes
    MAX_FILE_SIZE = 1024 * 1024  # 1 MB

    try:
        # Create a unique file name by appending a UUID to the original file name
        unique_file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}_{request.file_name}"

        # Generate a presigned URL
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={
                                                        'Bucket': DEFAULT_BUCKET_NAME,
                                                        'Key': unique_file_name,
                                                        'ContentType': request.file_type,
                                                    },
                                                    ExpiresIn=60,
                                                    HttpMethod='PUT'
                                                    )

        # Return the URL along with a warning about the file size limit
        return {
            'url': response,
            'message': 'Please upload a file of size 1 MB or less. Any files larger than this will be rejected.',
            'unique_file_name': unique_file_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class MoveFileRequest(BaseModel):
    source_bucket: str
    destination_bucket: str
    file_name: str
@app.post('/move-file')
async def move_file(request: MoveFileRequest):
    """Move a file from one bucket to another."""
    try:
        # Copy the object to the destination bucket
        s3_client.copy_object(
            Bucket=request.destination_bucket,
            CopySource={'Bucket': request.source_bucket, 'Key': request.file_name},
            Key=request.file_name,
        )

        # Delete the object from the source bucket
        s3_client.delete_object(Bucket=request.source_bucket, Key=request.file_name)

        return {"message": "File moved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files to serve the HTML page
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_html():
    with open("static/upload.html") as f:
        return f.read()