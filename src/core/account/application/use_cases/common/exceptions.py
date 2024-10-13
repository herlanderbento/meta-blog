class UserAlreadyExistsException(Exception):
    def __init__(self, message: str = "User with the given email already exists"):
        super().__init__(message)


class InvalidCredentialsException(Exception):
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message)
