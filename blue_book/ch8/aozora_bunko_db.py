"""Database model"""
import datetime

import peewee
from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase(
    'aozora_bunko',
    max_connections=8,
    stale_timeout=10,
    user='root',
    password="Qt2ZhGWQ"
)


class BaseModel(peewee.Model):
    """common base model"""
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = peewee.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        super().save(*args, **kwargs)

    class Meta:
        database = db


class Writer(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()
    is_active = peewee.BooleanField()

    class Meta:
        db_table = 'writers'
