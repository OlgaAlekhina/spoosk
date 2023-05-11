# project-site-spoosk

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-1f(irs+z-&_w@j!^a6#q_xweqv3g)dlw&jmcwvg2v#t8&k6$k!'

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

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

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
