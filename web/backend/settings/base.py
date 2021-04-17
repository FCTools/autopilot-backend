# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import os

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..")

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',

    'bot_manager',
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRONTAB_USER = os.getenv('CRONTAB_USER')
REDIS_SET_COMMAND = os.getenv('REDIS_SET_COMMAND')

SUPPORTED_TRACKERS = ['Binom']

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"

STATIC_URL = "/static/"

# internal autopilot codes for actions
PLAY_CAMPAIGN = 1
STOP_CAMPAIGN = 2
EXCLUDE_ZONE = 3
INCLUDE_ZONE = 4

SUPPORTED_ACTIONS = [PLAY_CAMPAIGN, STOP_CAMPAIGN, EXCLUDE_ZONE, INCLUDE_ZONE]

# bot statuses
ENABLED = 'enabled'
DISABLED = 'disabled'

SUPPORTED_TRAFFIC_SOURCES = ['Propeller Ads', 'Evadav', 'MGID']

# tracker (binom) codes for filtering statistics by time
TODAY = 1
YESTERDAY = 2
THIS_WEEK = 11
LAST_2_DAYS = 13
LAST_3_DAYS = 14
LAST_7_DAYS = 3
LAST_14_DAYS = 4
THIS_MONTH = 5
LAST_MONTH = 6
THIS_YEAR = 7
ALL_TIME = 9

SUPPORTED_PERIODS = [TODAY, YESTERDAY, THIS_WEEK, LAST_2_DAYS, LAST_3_DAYS, LAST_7_DAYS,
                     LAST_14_DAYS, THIS_MONTH, LAST_MONTH, THIS_YEAR, ALL_TIME]

# bot types
PLAY_STOP_CAMPAIGN = 1  # this bots check whole campaign and play or stop it
INCLUDE_EXCLUDE_ZONE = 2  # this bots check campaign zones and include/exclude these zones

CPU_COUNT = 6
