"""
tests/conftest.py
Shared fixtures for all tests
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.extensions import Base, get_db
from app.main import app  # Make sure this exists and imports correctly
from app.models.user import User
from app.models.device import Device
from app.models.wifi_network import WifiNetwork


# Test Database
@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, expire_on_commit=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with database override"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Sample Data Fixtures
@pytest.fixture
def test_lecturer(db_session):
    lecturer = User(
        fullname="Dr. Emily Carter",
        email="emily.carter@university.edu",
        password_hash="$2b$12$test hashed password123",  # fake hash
        role="lecturer"
    )
    db_session.add(lecturer)
    db_session.commit()
    db_session.refresh(lecturer)
    return lecturer


@pytest.fixture
def test_student(db_session):
    student = User(
        fullname="Alex Student",
        email="alex.student@university.edu",
        password_hash="$2b$12$test hashed password123",
        role="student"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student


@pytest.fixture
def test_wifi(db_session):
    wifi = WifiNetwork(
        ssid="Uni-Campus-WiFi",
        description="Main Campus Lecture Halls",
        location="Engineering Block B"
    )
    db_session.add(wifi)
    db_session.commit()
    db_session.refresh(wifi)
    return wifi