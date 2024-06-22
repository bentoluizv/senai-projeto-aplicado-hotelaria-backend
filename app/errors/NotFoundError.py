import json
from http import HTTPStatus


class NotFoundError(Exception):
    def __init__(self):
        self.message = 'Resource not found'
        self.status_code = HTTPStatus.NOT_FOUND
        super().__init__(self.message)

    def json(self):
        return json.dumps({
            'message': self.message,
            'status': self.status_code,
        })
