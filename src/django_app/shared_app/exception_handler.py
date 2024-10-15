from pydantic import ValidationError
from rest_framework.views import exception_handler as rest_framework_exception_handler
from rest_framework.response import Response
from rest_framework import status

from src.core.shared.domain.exceptions import (
    EntityValidationException,
    InvalidArgumentException,
    NotFoundException,
    ApplicationNotFoundException,
)
from src.core.account.application.use_cases.common.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)


def handle_validation_error(exc: ValidationError, context):
    errors = [{error["loc"][-1]: [error["msg"]]} for error in exc.errors()]
    return Response(errors, status.HTTP_422_UNPROCESSABLE_ENTITY)


def handle_entity_validation_error(exc: EntityValidationException, context):
    response = Response({"message": exc.args[0]}, status.HTTP_422_UNPROCESSABLE_ENTITY)
    response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return response


def handle_not_found_error(exc: NotFoundException, context):
    response = Response({"message": exc.args[0]}, status.HTTP_404_NOT_FOUND)
    response.status_code = status.HTTP_404_NOT_FOUND
    return response


def handle_application_not_found_error(exc: ApplicationNotFoundException, context):
    response = Response({"message": exc.args[0]}, status.HTTP_404_NOT_FOUND)
    return response


def handle_invalid_argument_error(exc: InvalidArgumentException, context):
    response = Response({"message": exc.args[0]}, status.HTTP_400_BAD_REQUEST)
    return response


def handle_user_already_exists_error(exc: UserAlreadyExistsException, context):
    response = Response({"message": exc.args[0]}, status.HTTP_409_CONFLICT)
    return response


def handle_invalid_credentials_error(exc: InvalidCredentialsException, context):
    response = Response({"message": exc.args[0]}, status.HTTP_401_UNAUTHORIZED)
    return response


handlers = [
    {"exception": ValidationError, "handle": handle_validation_error},
    {"exception": EntityValidationException, "handle": handle_entity_validation_error},
    {"exception": NotFoundException, "handle": handle_not_found_error},
    {"exception": InvalidArgumentException, "handle": handle_invalid_argument_error},
    {
        "exception": ApplicationNotFoundException,
        "handle": handle_application_not_found_error,
    },
    {
        "exception": UserAlreadyExistsException,
        "handle": handle_user_already_exists_error,
    },
    {
        "exception": InvalidCredentialsException,
        "handle": handle_invalid_credentials_error,
    },
]


def custom_exception_handler(exc, context):

    for handler in handlers:
        if isinstance(exc, handler["exception"]):
            return handler["handle"](exc, context)

    return rest_framework_exception_handler(exc, context)
