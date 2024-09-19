from fastapi import FastAPI
import uvicorn

from labs.api import codemonkey_endpoints, github_endpoints


app = FastAPI()


app.include_router(codemonkey_endpoints.router)
app.include_router(github_endpoints.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
