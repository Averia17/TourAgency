import os

from dotenv import load_dotenv

from tour_agency.settings import BASE_DIR

load_dotenv()

APP_DOMAIN = os.getenv("APP_DOMAIN", default="http://localhost:8000")

FILE_UPLOAD_STORAGE = os.getenv("FILE_UPLOAD_STORAGE", default="local")  # local | s3
FILE_MAX_SIZE = 10485760  # 10 MB
if FILE_UPLOAD_STORAGE == "local":
    MEDIA_ROOT_NAME = "media"
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
    MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"

if FILE_UPLOAD_STORAGE == "s3":
    # Using django-storages
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_S3_SIGNATURE_VERSION = os.getenv("AWS_S3_SIGNATURE_VERSION", default="s3v4")

    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
    AWS_DEFAULT_ACL = os.getenv("AWS_DEFAULT_ACL", default="private")

    AWS_PRESIGNED_EXPIRY = int(os.getenv("AWS_PRESIGNED_EXPIRY", default=10))  # seconds
