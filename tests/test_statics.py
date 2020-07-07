import pytest
from meow.webs import App, test


@pytest.fixture(scope="module")
def app() -> test.Client:
    return App()


@pytest.fixture(scope="module")
def client(app) -> test.Client:
    return test.Client(app)


def test_statics1(client):
    response = client.get("/static/style1.css")
    assert response.content == b"/* statics2/style1.css */\nbody {font-size: 10px}\n"


def test_statics2(client):
    response = client.get("/static/style2.css")
    assert response.content == b"/* statics1/style2.css */\nbody {font-size: 10px}\n"


def test_statics3(client):
    response = client.get("/static/style3.css")
    assert response.content == b"/* statics2/style3.css */\nbody {font-size: 10px}\n"


def test_statics4(client):
    response = client.get("/static/prefix1/style1.css")
    assert response.content == b"/* statics1/style1.css */\nbody {font-size: 10px}\n"


def test_statics5(client):
    response = client.get("/static/prefix2/style1.css")
    assert response.content == b"/* statics2/style1.css */\nbody {font-size: 10px}\n"


def test_statics6(client):
    response = client.get("/static/style4.css")
    assert response.status_code == 404


def test_static_url(app):
    assert app.static_url("style1.css") == "/static/style1.css"
