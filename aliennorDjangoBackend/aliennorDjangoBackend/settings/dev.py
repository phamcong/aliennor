from .common import *

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

SECRET_KEY = 'sqqh)7k)(q1jl7t(1^em(_1c*!2_tf(d66s79vhn_*qd21gx&_'
DEBUG = True
ALLOWED_HOSTS = ['*']

AWS_ACCESS_KEY_ID = 'AKIAIJCP62T7XKHJXPXA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'plf-aliennor'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}

CORS_ORIGIN_WHITELIST = (
    'localhost:4200'
)

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)