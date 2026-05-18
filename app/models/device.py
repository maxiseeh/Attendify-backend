import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship

from app.extensions import Base
from app.models.base import CRUDMixin, TimestampMixin


class DeviceType(str, enum.Enum):
    PHONE = "phone"
    LAPTOP = "laptop"
    TABLET = "tablet"


class Device(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mac_address = Column(String(17), unique=True, nullable=False, index=True)
    device_name = Column(String(120), nullable=True)
    device_type = Column(Enum(DeviceType), nullable=True)
    verified = Column(Boolean, default=False, nullable=False)
    last_seen = Column(DateTime, nullable=True)

    connection_logs = relationship(
        "ConnectionLog",
        back_populates="device",
        cascade="all, delete-orphan",
    )

    @property
    def is_auto_login_ready(self):
        return self.verified and bool(self.mac_address)

    def to_dict(self):
        return {
            "id": self.id,
            "mac_address": self.mac_address,
            "device_name": self.device_name,
            "device_type": self.device_type.value if self.device_type else None,
            "verified": self.verified,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "created_at": self.created_at.isoformat(),
        }
