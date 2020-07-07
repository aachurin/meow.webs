import pytest
from meow.webs import test, App


@pytest.fixture(scope="module")
def app() -> test.Client:
    return App(settings_module="hook_settings")


@pytest.fixture(scope="module")
def client(app) -> test.Client:
    return test.Client(app)


def test_on_response(client):
    response = client.get("/return_string/")
    assert response.status_code == 200
    assert response.headers["Custom"] == "Ran hooks"
    assert response.headers["AnotherCustom"] == "Ran hooks"


def test_on_error(client):
    with pytest.raises(TypeError) as excinfo:
        client.get("/return_unserializable_json/")
    import hooks

    assert hooks.ERROR_HOOK == 2
