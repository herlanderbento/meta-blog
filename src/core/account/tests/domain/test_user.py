import datetime
from typing import Annotated

from pydantic import Strict
from src.core.shared.domain.entity import AggregateRoot
from src.core.account.domain.user import CreateUserCommand, User, UserId
from src.core.account.domain.user_role import UserRole


class TestUser:
    def test_should_be_a_aggregate_root_subclass(self):
        assert issubclass(User, AggregateRoot)

    def test_should_be_slots(self):
        assert User.__slots__ == (
            "id",
            "name",
            "email",
            "password",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        )

    def test_should_be_able_generate_a_new_id(self):
        user = User(
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        assert user.id is not None
        assert isinstance(user.id, UserId)

    def test_should_be_able_generate_a_new_created_at(self):
        user = User(
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime.datetime)

    def test_should_be_able_generate_a_new_updated_at(self):
        user = User(
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )
        assert user.updated_at is not None
        assert isinstance(user.updated_at, datetime.datetime)

    def test_should_be_able_create_user(self):
        command = CreateUserCommand(
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )
        user = User.create(command)

        assert user is not None
        assert user.name == "John Doe"
        assert user.email == "john.doe@example.com"
        assert user.password == "password123"
        assert user.role == UserRole.USER
        assert user.is_active is True
        assert isinstance(user.id, UserId)
        assert isinstance(user.created_at, datetime.datetime)
        assert isinstance(user.updated_at, datetime.datetime)

    def test_should_generate_an_error_in_change_name(self):
        user = User(
            id=UserId(),
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        user.change_name(1)

        assert user.notification.has_errors() is True
        assert len(user.notification.errors) == 1
        assert user.notification.errors == {
            "name": ["Input should be a valid string"],
        }

    def test_should_change_name(self):
        user = User(
            id=UserId(),
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        user.change_name("Jane Doe")

        assert user.name == "Jane Doe"
        assert user.notification.has_errors() is False

    def test_should_generate_an_error_in_change_email(self):
        user = User(
            id=UserId(),
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        user.change_email(1)

        assert user.notification.has_errors() is True
        assert len(user.notification.errors) == 1
        assert user.notification.errors == {
            "email": ["Input should be a valid string"],
        }

    def test_should_change_email(self):
        user = User(
            id=UserId(),
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        user.change_email("jane.doe@example.com")

        assert user.email == "jane.doe@example.com"
        assert user.notification.has_errors() is False

    def test_should_generate_an_error_in_change_password(self):
        user = User(
            id=UserId(),
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        user.change_password(1)

        assert user.notification.has_errors() is True
        assert len(user.notification.errors) == 1
        assert user.notification.errors == {
            "password": ["Input should be a valid string"],
        }

    def test_should_change_password(self):
        user = User(
            id=UserId(),
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        user.change_password("new_password123")

        assert user.password == "new_password123"
        assert user.notification.has_errors() is False

    def test_should_generate_an_error_in_change_role(self):
        user = User(
            id=UserId(),
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        user.change_role("fake role")

        assert user.notification.has_errors() is True
        assert len(user.notification.errors) == 1
        assert user.notification.errors == {
            "role": ["Input should be 'admin' or 'user'"]
        }

    def test_should_change_role(self):
        user = User(
            id=UserId(),
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            role=UserRole.USER,
            is_active=True,
        )

        user.change_role(UserRole.ADMIN)

        assert user.role == UserRole.ADMIN
        assert user.notification.has_errors() is False

    def test_fields_mapping(self):
        assert User.__annotations__ == {
            "id": UserId,
            "name": str,
            "email": str,
            "password": str,
            "role": UserRole | None,
            "is_active": bool | None,
            "created_at": Annotated[datetime.datetime, Strict()],
            "updated_at": Annotated[datetime.datetime, Strict()],
        }
