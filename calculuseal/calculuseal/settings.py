"""
Django settings for calculuseal project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import logging


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-s3yt2k^ghv5$cj7xa0hdfzb_$(#*t9vbtgv@sd()e-pdcuiz4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# debug friendly
# running locally with `LOCALAAAA=1 ./manage runserver`
LOCAL = os.environ.get('LOCALAAAA')

# logging debug message, blue
if DEBUG:
    logging.basicConfig(level='DEBUG', format='\x1b[34m[%(levelname)s]\x1b[0m \x1b[32mfile=%(pathname)s;\x1b[0m %(message)s')

ALLOWED_HOSTS = ['*']

if LOCAL:
    SERVER_NAME = '4f742b98.ngrok.io'
else:
    SERVER_NAME = 'calculuseal.herokuapp.com'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webhook',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'calculuseal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'calculuseal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if LOCAL:
    # local DB for testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        # 'default': {
        #     'ENGINE': 'django.db.backends.postgresql',
        #     'NAME': 'test',
        #     'USER': 'soyccan',
        #     'PASSWORD': 'soyccan',
        #     'HOST': 'localhost',
        #     'PORT': '5432',
        # }
    }

else:
    # heroku's remote DB
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'd39abpadunahq1',
            'USER': 'nsapksktmaxkwr',
            'PASSWORD': '7cea9969461d6a1fcf3802ec089ca74bcd1fda7e9084ad7d103f029699b74f6f',
            'HOST': 'ec2-54-243-212-227.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'static/'

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
