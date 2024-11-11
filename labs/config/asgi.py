"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware

from labs.api import codemonkey_endpoints, github_endpoints
from labs.config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def get_application() -> FastAPI:
    app = FastAPI(title="Labs", debug=settings.DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(codemonkey_endpoints.router)
    app.include_router(github_endpoints.router)
    app.mount("/django", WSGIMiddleware(get_wsgi_application()))

    return app


application = get_application()
