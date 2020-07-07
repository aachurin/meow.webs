import datetime
import typing
import uuid
import enum
import dataclasses
from meow.di import ReturnValue
from meow.webs import App, Templates, http, exceptions


def get_request(request: http.Request) -> dict:
    return {
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "body": request.body.decode("utf-8"),
    }


def get_method(method: http.Method) -> dict:
    return {"method": method}


def get_scheme(scheme: http.Scheme) -> dict:
    return {"scheme": scheme}


def get_host(host: http.Host) -> dict:
    return {"host": host}


def get_port(port: http.Port) -> dict:
    return {"port": port}


def get_path(path: http.Path) -> dict:
    return {"path": path}


def get_query_string(query_string: http.QueryString) -> dict:
    return {"query_string": query_string}


def get_query_params(query_params: http.QueryParams) -> dict:
    return {"query_params": dict(query_params)}


def get_page_query_param(page: http.QueryParam) -> dict:
    return {"page": page}


def get_url(url: http.URL) -> dict:
    return {"url": url, "url.components": url.components}


def get_body(body: http.Body) -> dict:
    return {"body": body.decode("utf-8")}


def get_headers(headers: http.Headers) -> dict:
    return {"headers": dict(headers)}


def get_accept_header(accept: http.Header) -> dict:
    return {"accept": accept}


def get_missing_header(missing: http.Header) -> dict:
    return {"missing": missing}


def get_path_params(params: http.PathParams) -> dict:
    return {"params": params}


def get_request_data(data: http.RequestData) -> dict:
    if isinstance(data, typing.Mapping):
        return {
            "data": {
                key: value
                if not hasattr(value, "filename")
                else {
                    "filename": value.filename,
                    "content": value.read().decode("utf-8"),
                }
                for key, value in data.items()
            }
        }
    return data


def get_multikey_request_data(data: http.RequestData) -> dict:
    if isinstance(data, (http.QueryParams, http.FormData)):
        return {
            "data": sorted(
                [
                    (key, value)
                    for key, value in data.multi_items()
                    if not hasattr(value, "filename")
                ]
            )
        }


def return_string() -> str:
    return "<html><body>example content</body></html>"


def return_bytes() -> bytes:
    return b"..."


class Enum(enum.Enum):
    X = 1


@dataclasses.dataclass
class Dataclass:
    a: str
    b: float


def return_data() -> dict:
    return {
        "str": "content",
        "date": datetime.datetime(2020, 7, 1, 12, 0, 0),
        "time": datetime.time(12, 0, 0, tzinfo=datetime.timezone.utc),
        "uuid": uuid.UUID("00000000-0000-0000-0000-000000000000"),
        "enum": Enum.X,
        "data": Dataclass(a="x", b=1.1),
    }


def return_response() -> http.Response:
    return http.JSONResponse({"example": "content"})


def return_template(msg: str, tpl: str, templates: Templates) -> str:
    return templates.render(tpl, msg=msg)


def return_none() -> None:
    return None


def return_own_status_code() -> http.Response:
    return http.Response("", status_code=999)


def return_unserializable_json() -> dict:
    class Dummy:
        pass

    return {"dummy": Dummy()}


def return_302(app: App) -> str:
    raise exceptions.Found(app.reverse_url("return_string"))


class MyResponse(http.Response):
    charset = None


def return_bad_response() -> MyResponse:
    return MyResponse("")


def get_extra_path_params(p1: int, p2: float, p3: uuid.UUID):
    return {"p1": p1, "p2": p2, "p3": p3}


def return_default_query_param(x: int = 1):
    return {"x": x}


def return_required_query_param(x: int):
    return {"x": x}  # pragma: nocover


@dataclasses.dataclass
class Input:
    x: str
    y: int


def return_input_data(input: Input):
    return input


def wrap_result(ret: ReturnValue):
    return {"wrapped": ret}
