class CategoryAlreadyExistsException(Exception):
    def __init__(self, message: str = "Category with the given name already exists"):
        super().__init__(message)
