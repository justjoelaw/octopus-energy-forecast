from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Used to manage static files for the web server"""
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    """Used to store & serve dynamic media files with no access expiration"""
    location = 'media/public'
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    """
    Used to store & serve dynamic media files using access keys
	and short-lived expirations to ensure more privacy control
    """
    location = 'media/private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False