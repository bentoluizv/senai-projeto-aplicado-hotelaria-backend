class NotFoundError(Exception):
    def __init__(self, id):
        message = f'Resource with id "{id}" not found!'
        super().__init__(message)
