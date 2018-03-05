from .common import *

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']

# Allow all host hosts/domain names for this site
ALLOWED_HOSTS = ['*']

# we only need the engine name, as heroku takes care of the rest
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': get_env_variable('DATABASE_NAME'),
#         'USER': get_env_variable('DATABASE_USER'),
#         'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
#         'HOST': '',
#         'PORT': '',
#     }
# }

if not DEBUG:
  AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
  AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
  AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
  AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
  STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
  AWS_LOCATION = 'static'
  S3_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
  STATIC_URL = S3_URL
  AWS_LOCATION = 'static'
  MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN


# Parse database configuration from $DATABASE_URL
# import dj_database_url

# DATABASES = { 'default' : dj_database_url.config()}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# try to load local_settings.py if it exists
try:
  from local_settings import *
except Exception as e:
  pass