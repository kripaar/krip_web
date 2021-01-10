from .response import HTMLResponse


class Shortcut:
    def __init__(self, app):
        self.app = app

    def render(self, filepath, use_template_path=True):
        return HTMLResponse(open(self.app.template_path + filepath if use_template_path else filepath).read())
