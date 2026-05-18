from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.extensions import Base
from app.models.base import CRUDMixin, TimestampMixin


class ConnectionLog(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "connection_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    device_id = Column(Integer, ForeignKey("devices.id", ondelete="SET NULL"), nullable=True, index=True)
    connected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    disconnected_at = Column(DateTime, nullable=True)
    ip_address = Column(String(45), nullable=True)

    session = relationship("Session", back_populates="connection_logs")
    device = relationship("Device", back_populates="connection_logs")

    @property
    def is_connected(self):
        return self.disconnected_at is None

    @property
    def duration_seconds(self):
        if self.disconnected_at and self.connected_at:
            return int((self.disconnected_at - self.connected_at).total_seconds())
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "device_id": self.device_id,
            "connected_at": self.connected_at.isoformat(),
            "disconnected_at": self.disconnected_at.isoformat() if self.disconnected_at else None,
            "ip_address": self.ip_address,
            "is_connected": self.is_connected,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat(),
        }
