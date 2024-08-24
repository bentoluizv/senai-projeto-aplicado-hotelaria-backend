class AlreadyExistsError(Exception):
    def __init__(self, id):
        message = f'Resource with id "{id}" already exists!'
        super().__init__(message)
