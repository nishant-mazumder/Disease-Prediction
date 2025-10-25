"""
ASGI config for disease_prediction project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disease_prediction.settings')

application = get_asgi_application()
