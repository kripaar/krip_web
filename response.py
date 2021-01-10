class BaseResponse:
    def __init__(self):
        self.app = None  # Given at app.App.__process_response
        self.content_type = b""  #
        self.body = b""

    def get_resp_head(self):
        return {
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', self.content_type],
            ]
        }

    def get_resp_body(self):
        return {
            'type': 'http.response.body',
            'body': self.body,
        }


class ImageResponse(BaseResponse):
    def __init__(self, filepath: str, use_static_path=True):
        super().__init__()
        self.content_type = f'image/{self.fp.split(".")[-1]}'.encode()
        self.body = open(self.app.static_path + filepath if use_static_path else filepath, 'rb').read()


class TextResponse(BaseResponse):
    def __init__(self, text: str):
        super().__init__()
        self.content_type = b'text/plain'
        self.body = text.encode()


class HTMLResponse(BaseResponse):
    def __init__(self, code):
        super().__init__()
        self.content_type = b'text/html'
        self.body = code.encode()
