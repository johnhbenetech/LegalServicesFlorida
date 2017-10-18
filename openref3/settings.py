import os

import sys

sys.dont_write_bytecode = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SRC_ROOT = os.path.abspath(__file__)
for i in range(2):
    SRC_ROOT = os.path.dirname(SRC_ROOT)

STATIC_ROOT = os.path.join(SRC_ROOT, 'static_serve')

STATICFILES_DIRS = (
    os.path.join(SRC_ROOT, 'static'),
)

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(SRC_ROOT, 'media')

MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'liststyle',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #3rd-party
    'django_tables2',
    'reversion',
    'django_admin_listfilter_dropdown',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'django_filters',
    'widget_tweaks',
    'bootstrap3',
    'select2',
    'nested_admin',
    'kronos',
    #app
    'homepage',
    'service',
    'apitoken',
    'languages',
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

ROOT_URLCONF = 'openref3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SRC_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'openref3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': os.environ.get('DJANGO_DATABASE_NAME'),
    #    'USER': os.environ.get('DJANGO_DATABASE_USER'),
    #    'PASSWORD' : os.environ.get('DJANGO_DATABASE_PASSWORD'),
    #    'HOST': os.environ.get('DJANGO_DATABASE_HOST'),
    #    'PORT': os.environ.get('DJANGO_DATABASE_PORT'),
    #
    #}
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #    'NAME': os.environ.get('RDS_DB_NAME'),
    #    'USER': os.environ.get('RDS_USERNAME'),
    #    'PASSWORD': os.environ.get('RDS_PASSWORD'),
    #    'HOST': os.environ.get('RDS_HOSTNAME'),
    #    'PORT': os.environ.get('RDS_PORT'),
    #}
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'openref',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_INPUT_FORMATS = ('%H:%M',)
DATE_INPUT_FORMATS = ('%Y-%m-%d',)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/service/update'


SWAGGER_SETTINGS = {
    'JSON_EDITOR': True,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

