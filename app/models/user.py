"""
app/models/user.py
------------------
Represents a system user (student, lecturer, or admin).

DBML fields: id, fullname, email, password_hash, created_at, updated_at
App-level fields: role, is_active
"""

import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app.extensions import Base
from app.models.base import CRUDMixin, TimestampMixin


class UserRole(str, enum.Enum):
    STUDENT = "student"
    LECTURER = "lecturer"
    ADMIN = "admin"


class User(CRUDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Lecture sessions created by this lecturer
    lecturer_sessions = relationship(
        "Session",
        back_populates="lecturer",
        cascade="all, delete-orphan",
        foreign_keys="Session.lecturer_id",
    )

    attendance_records = relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan",
        foreign_keys="Attendance.student_id",
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    qr_attendance = relationship(
        "QrAttendance",
        back_populates="student",
        cascade="all, delete-orphan",
        foreign_keys="QrAttendance.student_id",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }