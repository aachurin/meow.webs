import pytest
from meow.webs import App, test, exceptions


@pytest.fixture(scope="module")
def app() -> test.Client:
    return App()


@pytest.fixture(scope="module")
def client(app) -> test.Client:
    return test.Client(app)


def test_request(client):
    response = client.get("/request/")
    assert response.json() == {
        "method": "GET",
        "url": "http://testserver/request/",
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "host": "testserver",
            "user-agent": "testclient",
        },
        "body": "",
    }


def test_method(client):
    response = client.get("/method/")
    assert response.json() == {"method": "GET"}
    response = client.post("/method/")
    assert response.json() == {"method": "POST"}


def test_scheme(client):
    response = client.get("http://example.com/scheme/")
    assert response.json() == {"scheme": "http"}
    response = client.get("https://example.com/scheme/")
    assert response.json() == {"scheme": "https"}


def test_host(client):
    response = client.get("http://example.com/host/")
    assert response.json() == {"host": "example.com"}


def test_port(client):
    response = client.get("http://example.com/port/")
    assert response.json() == {"port": 80}
    response = client.get("https://example.com/port/")
    assert response.json() == {"port": 443}
    response = client.get("http://example.com:123/port/")
    assert response.json() == {"port": 123}
    response = client.get("https://example.com:123/port/")
    assert response.json() == {"port": 123}


def test_path(client):
    response = client.get("/path/")
    assert response.json() == {"path": "/path/"}


def test_query_string(client):
    response = client.get("/query_string/")
    assert response.json() == {"query_string": ""}
    response = client.get("/query_string/?a=1&a=2&b=3")
    assert response.json() == {"query_string": "a=1&a=2&b=3"}


def test_query_params(client):
    response = client.get("/query_params/")
    assert response.json() == {"query_params": {}}
    response = client.get("/query_params/?a=1&a=2&b=3")
    assert response.json() == {"query_params": {"a": "1", "b": "3"}}


def test_single_query_param(client):
    response = client.get("/page_query_param/")
    assert response.json() == dict(page=None)
    response = client.get("/page_query_param/?page=123")
    assert response.json() == {"page": "123"}
    response = client.get("/page_query_param/?page=123&page=456")
    assert response.json() == {"page": "123"}


def test_url(client):
    response = client.get("http://example.com/url/")
    assert response.json() == {
        "url": "http://example.com/url/",
        "url.components": ["http", "example.com", "/url/", "", "", ""],
    }
    response = client.get("https://example.com/url/")
    assert response.json() == {
        "url": "https://example.com/url/",
        "url.components": ["https", "example.com", "/url/", "", "", ""],
    }
    response = client.get("http://example.com:123/url/")
    assert response.json() == {
        "url": "http://example.com:123/url/",
        "url.components": ["http", "example.com:123", "/url/", "", "", ""],
    }
    response = client.get("https://example.com:123/url/")
    assert response.json() == {
        "url": "https://example.com:123/url/",
        "url.components": ["https", "example.com:123", "/url/", "", "", ""],
    }
    response = client.get("http://example.com/url/?a=1")
    assert response.json() == {
        "url": "http://example.com/url/?a=1",
        "url.components": ["http", "example.com", "/url/", "", "a=1", ""],
    }


def test_body(client):
    response = client.post("/body/", data="content")
    assert response.json() == {"body": "content"}


def test_headers(client):
    response = client.get("http://example.com/headers/")
    assert response.json() == {
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "host": "example.com",
            "user-agent": "testclient",
        }
    }
    response = client.get(
        "http://example.com/headers/", headers={"X-Example-Header": "example"}
    )
    assert response.json() == {
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "host": "example.com",
            "user-agent": "testclient",
            "x-example-header": "example",
        }
    }

    response = client.post("http://example.com/headers/", data={"a": 1})
    assert response.json() == {
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "content-length": "3",
            "content-type": "application/x-www-form-urlencoded",
            "host": "example.com",
            "user-agent": "testclient",
        }
    }


def test_accept_header(client):
    response = client.get("/accept_header/")
    assert response.json() == {"accept": "*/*"}


def test_missing_header(client):
    response = client.get("/missing_header/")
    assert response.json() == {"missing": None}


def test_path_params(client):
    response = client.get("/path_params/abc/")
    assert response.json() == {"params": {"example": "abc"}}
    response = client.get("/path_params/a%20b%20c/")
    assert response.json() == {"params": {"example": "a b c"}}
    response = client.get("/path_params/abc/def/")
    assert response.status_code == 404


def test_full_path_params(client):
    response = client.get("/full_path_params/abc/def/")
    assert response.json() == {"params": {"example": "abc/def/"}}


def test_request_data_valid_json(client):
    response = client.post("/request_data/", json={"abc": 123})
    assert response.status_code == 200
    assert response.json() == {"data": {"abc": 123}}


def test_request_data_empty_json(client):
    response = client.post("/request_data/", json=None)
    assert response.status_code == 204


def test_request_data_non_dict_json(client):
    response = client.post("/request_data/", json="test")
    assert response.status_code == 400


def test_request_data_valid_urlencoded(client):
    response = client.post("/request_data/", data={"abc": 123})
    assert response.status_code == 200
    assert response.json() == {"data": {"abc": "123"}}


def test_request_data_empty_urlencoded_body(client):
    response = client.post(
        "/request_data/", headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 204


def test_request_data_unknown_body_type(client):
    response = client.post(
        "/request_data/", data=b"...", headers={"content-type": "unknown"}
    )
    assert response.status_code == 415


def test_request_data_invalid_json(client):
    response = client.post(
        "/request_data/", data=b"...", headers={"content-type": "application/json"}
    )
    assert response.status_code == 400


def test_multipart_request_data(client):
    response = client.post(
        "/request_data/", files={"a": ("b", "123")}, data={"b": "42"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {"a": {"filename": "b", "content": "123"}, "b": "42"}
    }

    response = client.post(
        "/multikey_request_data/", files={"a": ("b", "123")}, data={"b": ["41", "42"]}
    )
    assert response.status_code == 200
    assert response.json() == {"data": [["b", "41"], ["b", "42"]]}


def test_request_text(client):
    response = client.post(
        "/request_data/", data=b"...", headers={"content-type": "text/plain"}
    )
    assert response.status_code == 200
    assert response.content == b"..."


def test_return_string(client):
    response = client.get("/return_string/")
    assert response.text == "<html><body>example content</body></html>"


def test_return_bytes(client):
    response = client.get("/return_bytes/")
    assert response.content == b"..."


def test_return_data(client):
    response = client.get("/return_data/")
    assert response.json() == {
        "str": "content",
        "date": "2020-07-01T12:00:00",
        "time": "12:00:00Z",
        "enum": "X",
        "uuid": "00000000-0000-0000-0000-000000000000",
        "data": {"a": "x", "b": 1.1},
    }


def test_return_response(client):
    response = client.get("/return_response/")
    assert response.json() == {"example": "content"}


def test_return_none(client):
    response = client.get("/return_none/")
    assert response.status_code == 204


def test_return_own_status_code(client):
    response = client.get("/return_own_status_code/")
    assert response.status_code == 999


def test_return_unserializable_json(client):
    with pytest.raises(TypeError) as excinfo:
        client.get("/return_unserializable_json/")
    assert str(excinfo.value).endswith(
        "Object of type 'Dummy' is not JSON serializable."
    )


def test_return_302(client):
    resp = client.get("/return_302/", allow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"] == "/return_string/"


def test_chain_handlers(client):
    response = client.get("/return_wrapped_response/")
    assert response.json() == {"wrapped": "<html><body>example content</body></html>"}


def test_return_bad_response(client):
    with pytest.raises(RuntimeError) as excinfo:
        client.get("/return_bad_response/")
    assert str(excinfo.value) == "MyResponse content must be bytes. Got str."


def test_method_not_allowed(client):
    response = client.post("/return_bad_response/")
    assert response.status_code == 405


def test_included_routes(client):
    response = client.get(
        "/extra/path_params/1/1.1/00000000-0000-0000-0000-000000000000"
    )
    assert response.json() == {
        "p1": 1,
        "p2": 1.1,
        "p3": "00000000-0000-0000-0000-000000000000",
    }


def test_path_params_not_found(client):
    response = client.get("/extra/path_params/1/a/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json() == {"p2": "Must be a number."}


def test_return_default_query_param(client):
    response = client.get("/return_default_query_param/")
    assert response.json() == {"x": 1}


def test_return_required_query_param(client):
    response = client.get("/return_required_query_param/")
    assert response.status_code == 400
    assert response.json() == {"x": "Parameter is required"}


def test_invalid_query_param(client):
    response = client.get("/return_required_query_param/?x=a")
    assert response.status_code == 400
    assert response.json() == {"x": "Must be an integer."}


def test_return_input_data_get(client):
    response = client.get("/return_input_data_get/?x=a&y=1")
    assert response.json() == {"x": "a", "y": 1}
    response = client.get("/return_input_data_get/?x=a&y=a")
    assert response.status_code == 400
    assert response.json() == {"y": "Must be an integer."}


def test_return_input_data_post(client):
    response = client.post("/return_input_data_post/", json={"x": "a", "y": 1})
    assert response.status_code == 200
    assert response.json() == {"x": "a", "y": 1}
    response = client.post("/return_input_data_post/", json={"x": "a", "y": "1"})
    assert response.status_code == 400
    assert response.json() == {"y": "Must be an integer."}
    response = client.post("/return_input_data_post/", data={"x": "a", "y": "1"})
    assert response.status_code == 200
    assert response.json() == {"x": "a", "y": 1}
    response = client.post("/return_input_data_post/", data={"x": "a", "y": "1"})
    assert response.status_code == 200
    assert response.json() == {"x": "a", "y": 1}


def test_reverse_url(app):
    assert app.reverse_url("get_path_params", example="123") == "/path_params/123/"
    with pytest.raises(exceptions.NoReverseMatch):
        assert app.reverse_url("foo") == "/path_params/123/"
