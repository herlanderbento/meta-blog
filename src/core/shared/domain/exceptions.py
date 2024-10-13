from typing import Any, List


class NotFoundException(Exception):
    def __init__(self, _id: Any | List[Any], entity_name: str):
        if isinstance(_id, list):
            _id = ", ".join(str(i) for i in _id)
        super().__init__(f"{entity_name.__name__} with id {_id} not found")

class EntityValidationException(Exception):
    def __init__(self, errors: str = "Entity validation error occurred."):
        super().__init__(errors)


class ApplicationNotFoundException(Exception):
    def __init__(self, message: str = "Related entity not found"):
        super().__init__(message)

class InvalidArgumentException(Exception):
    def __init__(self, message):
        super().__init__(message)