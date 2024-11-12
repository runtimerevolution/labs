from ninja import NinjaAPI

from api.codemonkey_endpoints import router as codemonkey_router
from api.github_endpoints import router as github_router

ninja_api = NinjaAPI()

ninja_api.add_router("", codemonkey_router)
ninja_api.add_router("", github_router)
