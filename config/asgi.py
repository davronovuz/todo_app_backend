import os
from django.core.asgi import get_asgi_application

# BU YERNI HAM O'ZGARTIRING:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

application = get_asgi_application()