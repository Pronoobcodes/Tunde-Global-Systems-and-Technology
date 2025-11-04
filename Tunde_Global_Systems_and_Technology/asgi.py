"""
ASGI config for Tunde_Global_Systems_and_Technology project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tunde_Global_Systems_and_Technology.settings')

application = get_asgi_application()
