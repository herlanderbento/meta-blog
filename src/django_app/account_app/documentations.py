from drf_yasg import openapi


class UserDocumentation:

    @staticmethod
    def user_query_parameters():
        return [
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                description="User Name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="User Email",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "is_staff",
                openapi.IN_QUERY,
                description="User is staff",
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                "is_superuser",
                openapi.IN_QUERY,
                description="User is superuser",
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                "is_active",
                openapi.IN_QUERY,
                description="User is active",
                type=openapi.TYPE_BOOLEAN,
            ),
        ]

    @staticmethod
    def user_response_schema():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid"),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_staff": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "is_superuser": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "created_at": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date-time"
                        ),
                        "updated_at": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date-time"
                        ),
                    },
                )
            },
        )

    @staticmethod
    def user_list_response_schema():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_STRING, format="uuid"
                            ),
                            "name": openapi.Schema(type=openapi.TYPE_STRING),
                            "email": openapi.Schema(type=openapi.TYPE_STRING),
                            "is_staff": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            "is_superuser": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            "created_at": openapi.Schema(
                                type=openapi.TYPE_STRING, format="date-time"
                            ),
                            "updated_at": openapi.Schema(
                                type=openapi.TYPE_STRING, format="date-time"
                            ),
                        },
                    ),
                ),
                "meta": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "total": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "current_page": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "per_page": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "last_page": openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                ),
            },
        )
