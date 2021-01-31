class Route:
    def __init__(self, route_call_name_splitter=":", route_url_name_splitter="/"):
        self.route = {}
        self.splitters = {"call": route_call_name_splitter, "url": route_url_name_splitter}

    def get_route(self):
        return self.route

    def add_note_to(self, parent_name, parent_name_type, node):
        self.get_child_branch_of(parent_name, parent_name_type)[node] = {}

    def get_node(self, name, name_type="call"):
        return self.get_node_and_parent_ranch(name, name_type)[0]

    def get_parent_branch_of(self, name, name_type="call"):
        return self.get_node_and_parent_branch(name, name_type)[1]

    def get_child_branch_of(self, name, name_type="call"):
        node, branch = self.get_node_and_parent_branch(name, name_type)
        return branch[node]

    def get_node_and_parent_branch(self, name, name_type="call"):
        names = name.split(self.splitters[name_type])
        current_branch = self.route
        for n in names:
            for node in current_branch:
                if node.names[name_type] == n:
                    if node.names[name_type] == names[-1]:
                        return node, current_branch
                    else:
                        current_branch = current_branch[node]

class Node:
    def __init__(self, call_name, url_name, page):
        self.names = {"call": call_name, "url": url_name}
        self.page = page

class Page:
    class View:
        def __init__(self, function, request_required):
            self.function = function
            self.request_required = request_required

    def make_view(self, function, method:str="get", request_required=None):
        self.__setattr__(method.upper(), self.View(function, request_required))
        return self

    def get_view(self, method):
        v = self.__getattribute__(method.upper())
        if v is None:  # Wanted view (e.g. POST) DNE => Give GET view
            v = self.__getattribute__("GET")
            if v is None:  # GET view DNE => Say bye bye
                return None
        return v
