import typing
from meow.webs import http, Component


Context = typing.NewType("Context", dict)


class ContextComponent(Component):
    def resolve(self) -> Context:
        return Context({})


ERROR_HOOK = 0


class CustomResponseHeader:
    def __init__(self, header="Custom"):
        self.header = header

    def on_request(self, context: Context):
        context["hook"] = "Ran hooks"

    def on_response(self, response: http.Response, context: Context):
        if "hook" in context:
            response.headers[self.header] = context["hook"]

    def on_error(self):
        global ERROR_HOOK
        ERROR_HOOK += 1


class NonHook:
    pass


class NonComponent:
    pass
