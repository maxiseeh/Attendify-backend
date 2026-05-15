"""
app/models/session.py
---------------------
Represents a lecture/academic session conducted by a lecturer on a specific WiFi network.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.extensions import Base
from app.models.base import CRUDMixin, TimestampMixin


class Session(CRUDMixin, TimestampMixin, Base):
    """
    Lecture Session (not login session).
    Created when a lecturer starts a class on a WiFi network.
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core fields
    lecturer_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    wifi_network_id = Column(
        Integer, 
        ForeignKey("wifi_networks.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )

    session_name = Column(String(150), nullable=False)                    # e.g. "Data Structures - Week 5"
    start_time   = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time     = Column(DateTime, nullable=True)
    is_active    = Column(Boolean, default=True, nullable=False)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    lecturer = relationship(
        "User",
        back_populates="lecturer_sessions",
        foreign_keys="Session.lecturer_id"
    )

    wifi_network = relationship(
        "WifiNetwork",
        back_populates="sessions"
    )

    # Connection logs during this lecture session
    connection_logs = relationship(
        "ConnectionLog",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    # Attendance records linked to this lecture session
    attendance_records = relationship(
        "Attendance",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    # Computed properties
    @property
    def duration_minutes(self) -> int | None:
        """Returns duration in minutes if end_time is set."""
        if self.end_time and self.start_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        return None

    @property
    def is_ongoing(self) -> bool:
        """Check if session is currently active."""
        return self.is_active and self.end_time is None

    def to_dict(self):
        return {
            "id": self.id,
            "lecturer_id": self.lecturer_id,
            "wifi_network_id": self.wifi_network_id,
            "session_name": self.session_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "is_active": self.is_active,
            "duration_minutes": self.duration_minutes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }