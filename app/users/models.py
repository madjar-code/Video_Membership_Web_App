import uuid
from uuid import UUID
from typing import Optional
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from app.config import get_settings

from . import validators, security
from .exceptions import (
    UserHasAccountException,
    InvalidEmailException,
)

settings = get_settings()


class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(
        primary_key=True,
        default=uuid.uuid1
    )
    password = columns.Text()

    def __str__(self) -> str:
        return f'User(email={self.email}, user_id={self.user_id})'

    def __repr__(self) -> str:
        return f'User(email="{self.email}", user_id="{self.user_id}")'

    def set_password(self, pw, commit=False):
        pw_hash = security.generate_hash(pw)
        self.password = pw_hash
        if commit:
            self.save()
        return True

    def verify_password(self, pw_str):
        pw_hash = self.password
        verified, _ = security.verify_hash(pw_hash, pw_str)
        return verified

    @staticmethod
    def create_user(email, password=None):
        q = User.objects.filter(email=email)
        if q.count() != 0:
            raise UserHasAccountException('User already has an account.')

        valid, msg, email = validators._validate_email(email)
        if not valid:
            raise InvalidEmailException(f'Invalid email: {msg}')

        obj = User(email=email)
        obj.set_password(password)
        obj.save()
        return obj

    @staticmethod
    def check_exists(user_id: UUID) -> bool:
        q = User.objects.filter(user_id=user_id).allow_filtering()
        return q.count() != 0

    @staticmethod
    def by_user_id(user_id: Optional[UUID]) -> 'User':
        if user_id is None:
            return None
        q = User.objects.filter(user_id=user_id).allow_filtering()
        if q.count() != 1:
            return None
        return q.first()
