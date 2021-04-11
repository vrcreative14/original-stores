"""
Django settings for OriginalStores project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^c9#co+_4ff%8)k3t6+a99c+qm=_s26x((wzfp$(%a0(@eg*_b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'stores',
    'products',
    'orders',
    'api',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'frontend',
    'knox',    
    'blogpost',    
]

AUTH_USER_MODEL = 'accounts.User'               #changes the built-in user model to ours 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OriginalStores.urls'
PROJECT_DIR = os.path.dirname(__file__)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {    
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'frontend.context_processors.base',
            ],
        },
    },
]

WSGI_APPLICATION = 'OriginalStores.wsgi.application'

CORS_ORIGIN_WHITELIST = [
    "https://localhost:3000",
    "http://localhost:8100",    
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# if os.getenv('GAE_APPLICATION', None):
if os.getenv('development', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    #  'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'vcnity_online',
    #     'USER' : 'postgres',
    #     'PASSWORD' : 'postgres123',
    #     'HOST': '/cloudsql/vicinity-solutions:asia-south1:vicinity-instance', 
    #     'PORT': '5432',
    # }
    'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': 'ec2-34-203-155-237.compute-1.amazonaws.com',
            'PORT': '5432', 
            'NAME': 'd452dugs2bth6t',
            'USER': 'sefpclnhqedars',
            'PASSWORD': '9612b43a8d72f0d9d8fa307ed5a2cc39e71b2bf11e2740f9cca8d66331f476ec',
        }

}
else:
    # Running locally so connect to either a local MySQL instance or connect to
    # Cloud SQL via the proxy. To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'NAME': 'vcnityonline_test',
            'USER': 'postgres',
            'PASSWORD': 'aviral',
        }
    }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'HOST': 'ec2-34-203-155-237.compute-1.amazonaws.com',
    #         'PORT': '5432', 
    #         'NAME': 'd452dugs2bth6t',
    #         'USER': 'sefpclnhqedars',
    #         'PASSWORD': '9612b43a8d72f0d9d8fa307ed5a2cc39e71b2bf11e2740f9cca8d66331f476ec',
    #     }      
    # }




# if False and DEBUG: 
#         # Running in development, but want to access the Google Cloud SQL instance in production.
#         DATABASES = {
#             'default': {
#                 'ENGINE': 'django.db.backends.postgresql_psycopg2',  
#                 'NAME': 'cloud-database-name',  
#                 'USER': 'dbuser',                      
#                 'PASSWORD': 'dbpass',                  
#                 'HOST': '35.242.xxx.xxx', # Set to IP address 
#                 'PORT': '',  # Set to empty string for default. 
#             }
#         }
#  else if DEBUG:
#   #Sqlite database
#  else:
#      DATABASES = {
#    'default': {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',  
#     'NAME': 'cloud-database-name',  
#     'USER': 'dbuser',                     
#     'PASSWORD': 'dbpass',                  
#     'HOST': '/cloudsql/instancename:zone:dbname', #Use socket                   
#     'PORT': '', # Set to empty string for default.
#         }


import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/





STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [ 
   os.path.join(BASE_DIR, 'static')
]

#MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

from google.oauth2 import service_account
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.path.join(BASE_DIR,'credential.json'))

DEFAULT_FILE_STORAGE = "OriginalStores.gcloud.GoogleCloudMediaFileStorage"
GS_PROJECT_ID = 'vcnity-solutions'
# GS_BUCKET_NAME = 'vicinity-stores'
GS_BUCKET_NAME = 'vcnity-solutions.appspot.com'
MEDIA_ROOT = "media/"
UPLOAD_ROOT = 'media/uploads/'
#MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)
MEDIA_URL = 'https://storage.cloud.google.com/{}/'.format(GS_BUCKET_NAME)
#https://storage.cloud.google.com/vcnity-solutions.appspot.com/jaipur_hawa_mahal.jpg

#STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

REST_FRAMEWORK = {
     'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),   
    # 'DEFAULT_AUTHENTICATION_CLASSES': (        
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    #     'rest_framework.permissions.IsAuthenticated',
    #     #IsAuthenticated
    # ],
    # 'USER_DETAILS_SERIALIZER': 'userapp.serializer.UserDetailsSerializer'
     'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
}   

from datetime import timedelta

REST_KNOX = {
    'USER_SERIALIZER' : 'api.serializers.UserSerializer',
    'TOKEN_TTL' : timedelta(hours=24*7),
}

AUTHENTICATION_BACKENDS = (
    'accounts.backends.PhoneBackend', # our custom authentication backend
    'django.contrib.auth.backends.ModelBackend', # fallback to default authentication backend if first fails 
    )

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST = 'localhost'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'vcnityonline@gmail.com'
EMAIL_HOST_PASSWORD = 'Vcnity@2021'
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True

ALLOWED_HOSTS = [ '127.0.0.1','vcnityonline.herokuapp.com','www.vcnity.online', 'vcnity.online', "vicinity-solutions.et.r.appspot.com","vikreta.vcnity.online"]
                    
