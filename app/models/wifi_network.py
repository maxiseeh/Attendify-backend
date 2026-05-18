from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.extensions import Base
from app.models.base import CRUDMixin, TimestampMixin


class WifiNetwork(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "wifi_networks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ssid = Column(String(64), nullable=False, index=True)
    description = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    location = Column(String(150), nullable=True)

    sessions = relationship("Session", back_populates="wifi_network", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "ssid": self.ssid,
            "description": self.description,
            "location": self.location,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
