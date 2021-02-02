from .routes import *
import abc


class Blueprint:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self._route = Route()

    @abc.abstractmethod
    def route(new_path: str, name: str, method: str = "get", request=None):
        def decorator(func):
            def _decorator(self):
                if node := self._routes.get_node(name, "call"):
                    node.page.make_view("", method.upper(), request)
                else:
                    if new_path.find("/") == 0:
                        path = new_path[1:]
                    else:
                        path = new_path
                    parent_call = self._routes.get_parent_name_of(name, "call")
                    page = Page().make_view(func, method, request)
                    node = Node(self._routes.get_childest_name_of(name), path, page)
                    self._routes.add_note_to(parent_call, "call", node)
            return _decorator
        return decorator

    def register_(self, app):
        print(self._route.route)
        app._routes.append_route(self._route, self.namespace)
