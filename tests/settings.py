ROUTES = "tests.routes.routes"

DEBUG = False

TEMPLATE_DIRS = [
    "tests/templates1",
    "tests/templates2",
    {"prefix1": "templates1:.", "prefix2": "tests/templates2"},
]

STATIC_DIRS = [
    "tests/statics1",
    "tests/statics2",
    {"prefix1": "statics1:.", "prefix2": "tests/statics2"},
]

MY_SETTING = 1
