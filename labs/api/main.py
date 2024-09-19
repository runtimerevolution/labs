from fastapi import FastAPI

from labs.api import codemonkey_endpoints, github_endpoints


app = FastAPI()


app.include_router(codemonkey_endpoints.router)
app.include_router(github_endpoints.router)
