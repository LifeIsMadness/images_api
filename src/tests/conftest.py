from fastapi import FastAPI
import pytest
from starlette.testclient import TestClient

import routers


def start_application():
    app = FastAPI()
    app.include_router(router=routers.images_router)
    app.include_router(router=routers.groups_router)
    return app


@pytest.fixture
def app():
    return start_application()


@pytest.fixture
def api_client(app):
    return TestClient(app)
