import os
import boto3
from botocore.config import Config

def upload_file_to_r2(file_storage, filename):
    bucket_name = os.getenv("R2_BUCKET_NAME")
    access_key_id = os.getenv("R2_ACCESS_KEY_ID")
    secret_access_key = os.getenv("R2_SECRET_ACCESS_KEY")
    endpoint_url = os.getenv("R2_ENDPOINT_URL")
    public_url = os.getenv("R2_PUBLIC_URL")

    if not all([bucket_name, access_key_id, secret_access_key, endpoint_url, public_url]):
        raise ValueError("缺少必要的 Cloudflare R2 环境变量配置！请检查你的 .env 文件或 Render 环境变量。")

    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=Config(signature_version='s3v4')
    )

    content_type = 'application/octet-stream'
    ext = filename.lower()
    if ext.endswith('.jpg') or ext.endswith('.jpeg'):
        content_type = 'image/jpeg'
    elif ext.endswith('.png'):
        content_type = 'image/png'
    elif ext.endswith('.gif'):
        content_type = 'image/gif'
    elif ext.endswith('.webp'):
        content_type = 'image/webp'

    s3_client.upload_fileobj(
        file_storage,
        bucket_name,
        filename,
        ExtraArgs={
            'ContentType': content_type,
        }
    )

    public_url_clean = public_url.rstrip('/')
    return f"{public_url_clean}/{filename}"