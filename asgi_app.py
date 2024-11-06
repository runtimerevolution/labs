import os

import django
from django.core.asgi import get_asgi_application
from fastapi import FastAPI

from labs.api import codemonkey_endpoints, github_endpoints

# Set the DJANGO_SETTINGS_MODULE environment variable to point to your Django project's settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize Django settings
django.setup()

# Load Django ASGI application
django_app = get_asgi_application()

# Create FastAPI app
fastapi_app = FastAPI()

# include codemonkey and github into fastapi
fastapi_app.include_router(codemonkey_endpoints.router)
fastapi_app.include_router(github_endpoints.router)


# ASGI application to route to Django or FastAPI
async def app(scope, receive, send):
    if scope["type"] == "http" and scope["path"].startswith("/admin"):
        await django_app(scope, receive, send)
    else:
        await fastapi_app(scope, receive, send)
