import os

SECRET_KEY = 'your_key'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Absolute path for 'collectstatic' command
abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = abs_path + "/static"
STATIC_URL = "/static/"

# Permanent storage of static files
STATICFILES_DIRS = [
        "/var/www/pbspy/static",
        ]

# Look into django docs for setup
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
            }
        }
