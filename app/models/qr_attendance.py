"""
app/models/qr_attendance.py
---------------------------
QR Code based attendance as alternative / backup to WiFi-based attendance.
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.extensions import Base
from app.models.base import CRUDMixin, TimestampMixin


class QrAttendance(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "qr_attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)

    student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    scanned_at = Column(DateTime, nullable=False)
    qr_code    = Column(String(100), nullable=True)        # optional: store the actual code used

    # Relationships
    student = relationship(
        "User",
        back_populates="qr_attendance",
        foreign_keys="QrAttendance.student_id"
    )

    session = relationship("Session")

    # ------------------------------------------------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "session_id": self.session_id,
            "scanned_at": self.scanned_at.isoformat(),
            "qr_code": self.qr_code,
            "created_at": self.created_at.isoformat(),
        }