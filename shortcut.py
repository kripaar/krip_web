def Render(app, HTMLResponse):
    def to_render(filepath, **variables):
        return HTMLResponse(app.jinja2_env.get_template(filepath).render(**variables))
    return to_render
