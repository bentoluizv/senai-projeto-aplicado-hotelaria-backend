class NotFoundError(Exception):
    def __init__(self):
        self.message = "Resource not found"
        self.status = 404
        super().__init__(self.message)
