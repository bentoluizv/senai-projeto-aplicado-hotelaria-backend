import json
from http import HTTPStatus


class AlreadyExistsError(Exception):
    def __init__(self):
        self.message = 'Resource already exists'
        self.status_code = HTTPStatus.CONFLICT
        super().__init__(self.message)

    def json(self):
        return json.dumps({
            'message': self.message,
            'status': self.status_code,
        })
