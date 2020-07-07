import pytest
from meow.webs import App, test


@pytest.fixture(scope="module")
def client() -> test.Client:
    return test.Client(App())


def test_return_template1(client):
    response = client.get("/return_template/?msg=Hello&tpl=tpl1.html")
    assert response.text == "<html><body>templates1/tpl1:Hello</body></html>"


def test_return_template2(client):
    response = client.get("/return_template/?msg=Hello&tpl=tpl2.html")
    assert response.text == "<html><body>templates1/tpl2:Hello</body></html>"


def test_return_template3(client):
    response = client.get("/return_template/?msg=Hello&tpl=tpl3.html")
    assert response.text == "<html><body>templates2/tpl3:Hello</body></html>"


def test_return_template4(client):
    response = client.get("/return_template/?msg=Hello&tpl=prefix1/tpl1.html")
    assert response.text == "<html><body>templates1/tpl1:Hello</body></html>"


def test_return_template5(client):
    response = client.get("/return_template/?msg=Hello&tpl=prefix2/tpl3.html")
    assert response.text == "<html><body>templates2/tpl3:Hello</body></html>"
