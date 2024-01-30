import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from app.config import get_settings


settings = get_settings()


class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self) -> str:
        return f'User(emial={self.email}, user_id={self.user_id})'

    def __repr__(self) -> str:
        return f'User(emial={self.email}, user_id={self.user_id})'
