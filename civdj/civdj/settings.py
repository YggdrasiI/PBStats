"""
Django settings for civdj project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admin',
    'polymorphic',
    #    'registration',
    # Deprecated variant, see
    # https://github.com/ubernostrum/django-registration/blob/master/docs/quickstart.rst
    'debug_toolbar',
#    'erroneous',
    'static_precompiler',
    'django_bleach',
    'pbspy',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'pbspy.middleware.timezone.TimezoneMiddleware',
)

ROOT_URLCONF = 'civdj.urls'

WSGI_APPLICATION = 'civdj.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'pbspy', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
#            'debug': False,
            'context_processors': [
#                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
TIME_WITH_SECONDS_FORMAT_STR = "H:i:s"
# Django 1.9 (and 1.8?), formats.time_format() requires string with constant name :un:
# This was fixed in 1.11 (or 1.10)
if django.VERSION == (1, 9):
    TIME_WITH_SECONDS_FORMAT = "TIME_WITH_SECONDS_FORMAT_STR"
else:
    TIME_WITH_SECONDS_FORMAT = TIME_WITH_SECONDS_FORMAT_STR

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TEMPLATE_CONTEXT': True,
}

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = 'game_list'

# For compilation of less files, see
# https://github.com/andreyfedoseev/django-static-precompiler
STATIC_PRECOMPILER_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static')) # Default is STATIC_URL

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'static_precompiler.finders.StaticPrecompilerFinder',
)

# Workaround because StaticPrecompilerFinder does not trigger copy
# of static/COMPILED folder
STATICFILES_DIRS = [
    ("COMPILED", os.path.abspath(os.path.join(BASE_DIR, 'static', 'COMPILED')))
]

# Absolute path for 'collectstatic' command
__abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = __abs_path + "/static"
STATIC_URL = "/static/"


# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = ['li', 'ul', 'img']

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ['src', 'alt']

# Which CSS properties are allowed in 'style' attributes (assuming style is
# an allowed attribute)
BLEACH_ALLOWED_STYLES = []

# Strip unknown tags if True, replace with HTML escaped characters if False
BLEACH_STRIP_TAGS = True

# Strip HTML comments, or leave them in.
BLEACH_STRIP_COMMENTS = True


from civdj.settings_local import *
