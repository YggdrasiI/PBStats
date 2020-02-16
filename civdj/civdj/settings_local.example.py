import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'your_key'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Add new languages here and create with 
# 'python3 manage.py makemessages --locale {your language code}'
# translation file in civdj/pbspy/locale/...
LANGUAGES = (
    ("en", ("English")),
    ("de", ("Deutsch")),
)

# Permanent storage of static files
if not DEBUG:
    # Set STATIC_ROOT permissions such that
    #      manage.py [collectstatic|compilestatic]
    # can write the files.
    STATIC_ROOT = '/var/www/html/pbspy/static/'
    STATIC_URL = 'http://localhost/pbspy/static/'

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
