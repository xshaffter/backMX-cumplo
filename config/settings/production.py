import environ

from config.settings.base import *

env = environ.Env(
    DB_HOST=(str, "db"),
    DB_PORT=(str, '3306'),
)

environ.Env.read_env()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}

BANXICO_API_TOKEN = '58ff548e6ab78e716e400bafcd33c4843bc1cf9cf91e945d30c09568b57a3096'
BANXICO_URL = f'{BANXICO_BASE_URL}series/{{series}}/datos/{{init_date}}/{{end_date}}?token={BANXICO_API_TOKEN}'
