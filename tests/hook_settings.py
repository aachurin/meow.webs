import hooks


ROUTES = "tests.routes.routes"

EVENT_HOOKS = [
    "hooks.CustomResponseHeader",
    hooks.CustomResponseHeader(header="AnotherCustom"),
]

COMPONENTS = ["hooks.ContextComponent"]
