from meow.webs import http
from meow.webs.datastructures import MutableHeaders, ImmutableHeaders


def test_headers_type():
    h = MutableHeaders([("a", "123"), ("A", "456"), ("b", "789")])
    assert "a" in h
    assert "A" in h
    assert "b" in h
    assert "B" in h
    assert "c" not in h
    assert h["a"] == "123"
    assert h.getlist("a") == ["123", "456"]
    assert list(h.keys()) == ["a", "b"]
    assert list(h.values()) == ["123", "789"]
    assert list(h.items()) == [("a", "123"), ("b", "789")]
    assert h.multi_items() == [("a", "123"), ("a", "456"), ("b", "789")]
    assert list(h) == ["a", "b"]
    assert dict(h) == {"a": "123", "b": "789"}
    assert repr(h) == "MutableHeaders([('a', '123'), ('a', '456'), ('b', '789')])"
    assert MutableHeaders({"a": "123", "b": "456"}) == MutableHeaders(
        [("a", "123"), ("b", "456")]
    )
    h.add("b", "000")
    assert h.multi_items() == [("a", "123"), ("a", "456"), ("b", "789"), ("b", "000")]
    h["a"] = "222"
    assert h["a"] == "222"
    assert h.multi_items() == [("a", "222"), ("b", "789"), ("b", "000")]
    h.add("a", "333")
    assert h.multi_items() == [("a", "222"), ("b", "789"), ("b", "000"), ("a", "333")]
    assert h["a"] == "222"
    del h["b"]
    assert "b" not in h
    assert h.multi_items() == [("a", "222"), ("a", "333")]
    h.add("c", "444")
    assert h.multi_items() == [("a", "222"), ("a", "333"), ("c", "444")]


def test_immutable_headers_type():
    h = ImmutableHeaders({"a": "123", "b": "234"})
    assert "a" in h
    assert "A" in h
    assert "b" in h
    assert "B" in h
    assert "c" not in h
    assert h["a"] == "123"
    assert list(h.keys()) == ["a", "b"]
    assert list(h.values()) == ["123", "234"]
    assert list(h.items()) == [("a", "123"), ("b", "234")]
    assert list(h) == ["a", "b"]
    assert dict(h) == {"a": "123", "b": "234"}
    assert repr(h) == "ImmutableHeaders({'a': '123', 'b': '234'})"
    assert ImmutableHeaders({"a": "123", "b": "456"}) == ImmutableHeaders(
        {"a": "123", "b": "456"}
    )


def test_query_params_type():
    q = http.QueryParams([("a", "123"), ("a", "456"), ("b", "789")])
    assert "a" in q
    assert "A" not in q
    assert "c" not in q
    assert q["a"] == "123"
    assert q.getlist("a") == ["123", "456"]
    assert list(q.keys()) == ["a", "b"]
    assert list(q.values()) == ["123", "789"]
    assert list(q.items()) == [("a", "123"), ("b", "789")]
    assert list(q) == ["a", "b"]
    assert dict(q) == {"a": "123", "b": "789"}
    assert repr(q) == "QueryParams([('a', '123'), ('a', '456'), ('b', '789')])"
    assert http.QueryParams({"a": "123", "b": "456"}) == http.QueryParams(
        [("a", "123"), ("b", "456")]
    )
    assert http.QueryParams({"a": "123", "b": "456"}) != {"a": "123", "b": "789"}
    assert http.QueryParams(
        http.QueryParams({"a": "123", "b": "456"})
    ) == http.QueryParams([("a", "123"), ("b", "456")])
