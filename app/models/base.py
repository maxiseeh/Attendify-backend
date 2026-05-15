"""
app/models/base.py
------------------
Common mixins for all models.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Mapped


class TimestampMixin:
    """Adds created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class CRUDMixin:
    """Common CRUD helper methods (optional)."""

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self