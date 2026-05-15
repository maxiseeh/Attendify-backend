from datetime import datetime
from sqlalchemy import Column, DateTime


class TimestampMixin:
    """
    Adds 'created_at' and 'updated_at' columns to any model that uses this.
    This way we always know when a record was created or last changed.
    """

    # Set automatically when a record is first saved
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Set automatically every time a record is updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CRUDMixin:
    """
    Adds simple helper methods to create and update records.
    CRUD stands for Create, Read, Update, Delete.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new instance of the model without saving it yet."""
        instance = cls(**kwargs)
        return instance

    def update(self, **kwargs):
        """Update one or more fields on this record."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self