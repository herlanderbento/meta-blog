class PostAlreadyExistsException(Exception):
    def __init__(self, message: str = "Post with the given name already exists"):
        super().__init__(message)
