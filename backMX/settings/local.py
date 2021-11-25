from backMX.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'django',
        'PASSWORD': '0P7Tiw6KQCHJ',
        'HOST': 'db',
        'PORT': '3306',
    }
}

BANXICO_API_TOKEN = '58ff548e6ab78e716e400bafcd33c4843bc1cf9cf91e945d30c09568b57a3096'
BANXICO_URL = f'{BANXICO_BASE_URL}series/{{series}}/datos/{{init_date}}/{{end_date}}?token={BANXICO_API_TOKEN}'
