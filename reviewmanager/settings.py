#-*- coding: utf-8 -*-
#Obs: Se estiver operando no modo LOCAL modificar o CSS para referenciar os  staticfiles

# Django settings for reviewmanager project.
import os
PROJECT_DIR = os.path.dirname(__file__)
LOCAL = False
PROJECT_NAME = '/reviewmanager'



DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Manuel G. S. Neto', 'academicsgit@users.noreply.github.com'),
)

MANAGERS = ADMINS
if LOCAL:
    DATABASES = {
                 'default': {
                             'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                             'NAME': os.path.join(PROJECT_DIR,'local.db'),                      # Or path to database file if using sqlite3.
                             'USER': '',                      # Not used with sqlite3.
                             'PASSWORD': '',                  # Not used with sqlite3.
                             'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
                             'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
                             }
                 }
else:
    #create database reviewmanager CHARACTER SET utf8 COLLATE utf8_general_ci
    # grant all privileges on reviewmanager.* to review@'localhost' identified by 'cesar@mprof'
    DATABASES = { 
                 'default': {
                             'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                             'NAME': 'reviewmanager',                      # Or path to database file if using sqlite3.
                             'USER': 'root',                      # Not used with sqlite3.
                             'PASSWORD': 'root',                  # Not used with sqlite3.
                             'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
                             'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
                             }
                 }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Fortaleza'

LANGUAGE_CODE = 'pt-br'

DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = ('%d/%m/%Y',)
DATETIME_FORMAT = 'd/m/Y H:i'
DATETIME_INPUT_FORMATS = ('%d/%m/%Y %H:%M', '%d/%m/%Y %H:%M:%S',)

LANGUAGES = (
             ('pt-br', u'Portugues Brasil'),
             ('en', u'Ingles'),
             )

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
if LOCAL:
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = PROJECT_NAME + '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR,'layout')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if LOCAL:
    STATIC_URL = '/static/'
else:
    STATIC_URL = PROJECT_NAME + '/static/'

#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
                    os.path.join(PROJECT_DIR,'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0hgseu@pb#32fh75824rk#vb+vu5)1f0p!4n)t)ic07#!_+ngp'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'reviewmanager.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'reviewmanager.wsgi.application'

TEMPLATE_DIRS = (
                  os.path.join(PROJECT_DIR,'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'review',
    'geraldo',
    'captcha',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

if LOCAL:
    LOGIN_URL = '/login/'
    LOGOUT_URL = '/logout/'
else:
    LOGIN_URL = PROJECT_NAME +'/login/'
    LOGOUT_URL = PROJECT_NAME + '/logout/'
    
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = '/tmp'
SESSION_COOKIE_AGE = 1 * 4 * 60 * 60 #tempo em segundos , 4 horas
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
