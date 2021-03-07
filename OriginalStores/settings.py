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
DEBUG = True



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

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
     'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vcnityonline_test',
        'USER' : 'postgres',
        'PASSWORD' : 'aviral',
        'HOST': 'localhost',  
        'PORT':'5432',
    }
}

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
GS_PROJECT_ID = 'vicinity-solutions'
# GS_BUCKET_NAME = 'vicinity-stores'
GS_BUCKET_NAME = 'vicinity-solutions.appspot.com'
MEDIA_ROOT = "media/"
UPLOAD_ROOT = 'media/uploads/'
MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)

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
EMAIL_PORT = 587
EMAIL_HOST_USER = 'vcreative14@gmailcom'
EMAIL_HOST_PASSWORD = 'Sona@1960'
EMAIL_USE_TLS = True

ALLOWED_HOSTS = ['vcnityonline.herokuapp.com','www.vcnity.online', '127.0.0.1', 'vcnity.online']
                    
