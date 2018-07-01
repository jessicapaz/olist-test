from .base import *


DEBUG = env.bool('DJANGO_DEBUG', default=False)

DATABASES = {
    'default': env.db()
}