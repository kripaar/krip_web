def _to_head(headers:dict):
    return {
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [k, v] for k, v in headers.items()
            ]
        }


def _to_body(body):
    return {
            'type': 'http.response.body',
            'body': body,
        }


class Response:
    def __init__(self, content_type: bytes, extra_headers:dict={}, app=None, encode=True):
        self.app = app
        self.encode = encode
        extra_headers[b"content-type"] = content_type
        self.headers = extra_headers

    def __call__(self, body: (bytes or str), header_formats:dict={}):
        if header_formats != {}:
            for k, v in header_formats.items():
                self.headers[k] = self.headers[k].decode().format(**v).encode()
        self.head = _to_head(self.headers)
        self.body = _to_body(body.encode()) if self.encode else _to_body(body)
        return self
