from jinja2 import Environment, FileSystemLoader


class App:
    def __init__(self, template_path="template"):
        self.routes = {}
        self.template_path = template_path
        self.jinja2_env = Environment(loader=FileSystemLoader(self.template_path))
        self.request_required_on_default_if_received_such_requests_types = ["POST"]

    async def __call__(self, scope, receive, send):
        things = Things(scope, receive, send)
        if scope["type"] == "http":
            if scope["path"] in self.routes:
                if scope["method"] in self.routes[scope["path"]]:
                    the_long_thing = self.routes[scope["path"]][scope["method"]]
                    await things.set_request_post_form()

                    things_to_give_view = []
                    if the_long_thing["request_required"]: things_to_give_view.append(things.request)
                    await self.__process_response(await the_long_thing["function"](*things_to_give_view), things)

    def route(self, path, method="get", i_want_request=None):
        def decorator(f):
            if self.routes.get(path) is None:
                self.routes[path] = {}
            self.routes[path][method.upper()] = {"function": f, "request_required": i_want_request or ((method.upper() in self.request_required_on_default_if_received_such_requests_types) if i_want_request is None else False)}
            # i_want_request: True if request is NEEDED, False if request is NOT NEEDED (even when you're receiving a POST request), None if you just go on default
        return decorator

    async def __process_response(self, response, things):
        await things.send(response.head)
        await things.send(response.body)


class Things:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self.receive = receive
        self.send = send
        self.request = Request()

    async def get_request_body(self):
        body = b''
        more_body = True

        while more_body:
            message = await self.receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        return body

    async def set_request_post_form(self):
        body = await self.get_request_body()
        if body != b'':
            self.request.POST._set_form_from_body(body)


class Request:
    class __Post:
        def __init__(self):
            self.form = {}

        def _set_form_from_body(self, body: bytes, reset_form:bool=True):
            self.form = {} if reset_form else self.form
            body = body.decode()
            things = body.split("&")
            for t in things:
                k, v = t.split("=")
                self.form[k] = v

    def __init__(self):
        self.POST = self.__Post()




