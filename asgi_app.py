import os
import django
from fastapi import FastAPI
from django.core.asgi import get_asgi_application

# Set the DJANGO_SETTINGS_MODULE environment variable to point to your Django project's settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize Django settings
django.setup()

# Load Django ASGI application
django_app = get_asgi_application()

# Create FastAPI app
fastapi_app = FastAPI()

# Sample FastAPI route
@fastapi_app.get("/fastapi")
async def fastapi_root():
    return {"message": "Hello from FastAPI"}

# ASGI application to route to Django or FastAPI
async def app(scope, receive, send):
    if scope["type"] == "http" and scope["path"].startswith("/d"):
        await django_app(scope, receive, send)
    else:
        await fastapi_app(scope, receive, send)
