import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'your_key'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Absolute path for 'collectstatic' command
abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = abs_path + "/static"
STATIC_URL = "/static/"

# Permanent storage of static files
if not DEBUG:
    STATIC_ROOT='/var/www/pbspy/static/'
    STATIC_URL = 'http://localhost/pbspy/static/'

    # Ugly workaround. Do not set STATICFILES_DIRS for 'collectstatic'
    import sys
    mode = "undefined"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    if not mode == "collectstatic":
        STATICFILES_DIRS = [
            "/var/www/pbspy/static",
        ]

# Look into django docs for setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
SOUTH_DATABASE_ADAPTERS = {
    'default': "south.db.sqlite3"
}
