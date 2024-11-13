from api.codemonkey_endpoints import router as codemonkey_router
from api.github_endpoints import router as github_router
from ninja import NinjaAPI

ninja_api = NinjaAPI(title="Labs")

ninja_api.add_router("/codemonkey", codemonkey_router)
ninja_api.add_router("/github", github_router)
