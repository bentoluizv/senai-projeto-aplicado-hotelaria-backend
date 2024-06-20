import json


class NotFoundError(Exception):
    def __init__(self):
        self.message = 'Resource not found'
        self.status_code = 404
        super().__init__(self.message)

    def json(self):
        return json.dumps({
            'message': self.message,
            'status': self.status_code,
        })
