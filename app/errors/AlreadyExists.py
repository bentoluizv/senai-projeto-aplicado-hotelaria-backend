class AlreadyExistsError(Exception):
    def __init__(self):
        self.message = "Resource already exists"
        self.status = 409
        super().__init__(self.message)
