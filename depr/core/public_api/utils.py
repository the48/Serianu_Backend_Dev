class UnexpectedAPIError(Exception):
    pass
    # def __init__(self, message, filename=None):
    #     super().__init__(message)
    #     self.filename = filename or inspect.stack()[1].filename

    # def __str__(self):
    #     return f"Error raised in {self.filename}: {super().__str__()}"