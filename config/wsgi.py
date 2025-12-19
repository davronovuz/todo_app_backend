import os

from django.core.wsgi import get_wsgi_application

# BU YERNI HAM O'ZGARTIRING:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

application = get_wsgi_application()