def _to_head(headers:dict, cookies: dict):
    return {
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [k, v] for k, v in headers.items()  # Other headers
            ] + [
                [b"set-cookie", b"{}={}".format(k, v)] for k, v in cookies.items()  # Cookie headers
            ]
        }


def _to_body(body):
    return {
            'type': 'http.response.body',
            'body': body,
        }


class Response:
    def __init__(self, content_type: bytes, extra_headers: dict={}, encode=True):
        extra_headers[b"content-type"] = content_type
        self.headers = {(k if isinstance(k, bytes) else k.encode()):v for k, v in extra_headers.items()}
        self.cookies = {}
        self.encode = encode
        self.afterthat_function = lambda: 0

    def __call__(self, content):
        self.content = content.encode() if self.encode else content
        self._create_head()
        self._create_body()

    def set_cookie(self, name, value):
        self.cookies[name] = value

    def _create_head(self):
        self.head = _to_head(self.headers, self.cookies)
        return self.head

    def _create_body(self):
        self.body = _to_body(self.content)
        return self.body

    def set_afterthat_function(self, f, give_response=False, args_to_f: tuple=(), kwargs_to_f: dict={}):
        if give_response: kwargs_to_f["response"] = self
        self.afterthat_function = lambda: f(*args_to_f, **kwargs_to_f)


class TextResponse(Response):
    def __init__(self, extra_headers: dict={}):
        super().__init__(b"text/plain", extra_headers)

    def __call__(self, text:str):
        super().__call__(text)
        return self


class ImageResponse(Response):
    def __init__(self, extra_headers: dict={}, file_fmt:str="png"):
        super().__init__("image/{}".format(file_fmt).encode(), extra_headers, False)

    def __call__(self, image):
        super().__call__(image)
        return self


class HTMLResponse(Response):
    def __init__(self, extra_headers: dict={}):
        super().__init__(b"text/html", extra_headers)

    def __call__(self, code):
        super().__call__(code)
        return self


class FileResponse(Response):
    def __init__(self, extra_headers: dict={}):
        super().__init__(b"application/octet-stream", extra_headers, False)

    def __call__(self, content, filename, as_attachment=False, delete_original_file_after_sending_out=False):
        self.headers[b"content-disposition"] = "{}; filename={}".format("attachment" if as_attachment else "inline", filename).encode()
        super().__call__(content.read())
        if delete_original_file_after_sending_out: self.set_afterthat_function(__import__("os").remove, args_to_f=(content.name,))
        return self
