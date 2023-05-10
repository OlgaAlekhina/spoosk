from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1f(irs+z-&_w@j!^a6#q_xweqv3g)dlw&jmcwvg2v#t8&k6$k!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spoosk',
        'USER': 'adminkate',
        'PASSWORD': 'adminkate',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_IMAGE_URL = 'static/image'
STATIC_IMAGE_ROOT = os.path.join(BASE_DIR, 'image')
