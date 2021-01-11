from jinja2 import Environment, FileSystemLoader


class App:
    def __init__(self):
        self.routes = {}
        template_path = "template"
        self.jinja2_env = Environment(loader=FileSystemLoader(template_path))

    async def __call__(self, scope, receive, send):
        things = Things(scope, receive, send)
        if scope["type"] == "http":
            if scope["path"] in self.routes:
                await self.__process_response(await self.routes[scope["path"]](), things)

    def route(self, path):
        def decorator(f):
            self.routes[path] = f
        return decorator

    async def __process_response(self, response, things):
        await things.send(response.head)
        await things.send(response.body)


class Things:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self.receive = receive
        self.send = send
