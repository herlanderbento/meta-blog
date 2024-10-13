from rest_framework.request import Request

from src.core.shared.domain.exceptions import InvalidArgumentException


class FileUploadHandler:

    def handle_uploaded_files_by_dict(
        self, request: Request, file_fields: dict
    ) -> list:

        if not any(
            request.FILES.get(field_name) for field_name in file_fields.values()
        ):
            raise InvalidArgumentException(
                "No files uploaded for the specified fields."
            )

        files = []
        for field, field_name in file_fields.items():
            file = request.FILES.get(field_name)
            if file:
                files.append(
                    {
                        "field": field,
                        "file_name": file.name,
                        "content": file.read(),
                        "content_type": file.content_type,
                    }
                )
        return files

    def handle_uploaded_files_by_list(self, request: Request, fields: list) -> list:

        if not any(request.FILES.get(field) for field in fields):
            raise InvalidArgumentException(
                "No files uploaded for the specified fields."
            )

        files = []
        for field in fields:
            file = request.FILES.get(field)
            if file:
                files.append(
                    {
                        "field": field,
                        "file_name": file.name,
                        "content": file.read(),
                        "content_type": file.content_type,
                    }
                )
        return files
