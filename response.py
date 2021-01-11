def _to_head(content_type):
    return {
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', content_type],
            ]
        }


def _to_body(body):
    return {
            'type': 'http.response.body',
            'body': body,
        }


class Response:
    def __init__(self, content_type: bytes, app=None, encode=True):
        self.app = app
        self.head = _to_head(content_type)
        self.encode = encode

    def __call__(self, body: (bytes or str)):
        self.body = _to_body(body.encode()) if self.encode else _to_body(body)
        return self
