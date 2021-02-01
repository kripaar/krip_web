from jinja2 import Environment, FileSystemLoader
from .response import FileResponse
from .routes import Route, Node, Page


class App:
    def __init__(self, template_path="template", static_path="static", static_url="static", route_call_name_splitter=":", route_url_name_splitter="/"):
        self.template_path = template_path
        self.static_path = static_path
        self.static_url = static_url

        self.jinja2_env = Environment(loader=FileSystemLoader(self.template_path))
        self.request_required_on_default_if_received_such_requests_types = ["POST"]
        self._routes = Route(route_call_name_splitter, route_url_name_splitter)

        self.jinja2_env.globals["url_for"] = self.__get_static_file_url

    async def __call__(self, scope, receive, send):
        things = Things(scope, receive, send)
        await things.set_request_post_form()
        if scope["type"] == "http":
            if node := self._routes.get_node(scope["path"], "url"):
                if (method := scope["method"]) in node.page:
                    view = node.page.get_view(method)
                    to_give_view = {}
                    if view.request_required or (view.request_required is None and method in self.request_required_on_default_if_received_such_requests_types):
                        to_give_view["request"] = things.request
                    response = await view.function(**to_give_view)
                    await self.__process_response(response, things)

    def route(self, new_path, name, method="get", i_want_request=None):
        def decorator(f):
            # if self._routes.get(path) is None:
            #     self._routes[path] = {}
            # self._routes[path][method.upper()] = {"function": f, "request_required": i_want_request or ((method.upper() in self.request_required_on_default_if_received_such_requests_types) if i_want_request is None else False)}
            if node := self._routes.get_node(name, "call"):
                node.page.make_view(f, method, i_want_request)
            else:
                if new_path.find("/") == 0:
                    path = new_path[1:]
                else:
                    path = new_path
                parent_call = self._routes.get_parent_name_of(name, "call")
                page = Page().make_view(f, method, i_want_request)
                node = Node(self._routes.get_childest_name_of(name), path, page)
                self._routes.add_note_to(parent_call, "call", node)

        return decorator

    # def error_handler(self, error_status_code=404, request_required=False):
    #     def decorator(f):
    #         self._error_pages[error_status_code] = {"function": f, "request_required": request_required}
    #     return decorator

    def __get_static_file_url(self, fp):
        return self.static_url + "/" + fp

    async def __process_response(self, response, things):
        await things.send(response.head)
        await things.send(response.body)
        response.afterthat_function()


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


