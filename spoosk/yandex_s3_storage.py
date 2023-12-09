from storages.backends.s3boto3 import S3Boto3Storage


class ImagesStorage(S3Boto3Storage):
    bucket_name = 'newback'
    file_overwrite = False
    querystring_auth = False