# tests/confest.py
# This file sets up the test environment.
# It creates a test database and sample data that all tests can use.
# Note: conftest.py (with a 't') is the standard name — this file works the same way.

import pytest
from datetime import datetime

# Import our Flask app factory and database
from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.device import Device
from app.models.wifi_network import WifiNetwork


# --- App and Client Setup ---

@pytest.fixture(scope="session")
def app():
    """
    Create a test version of the Flask app.
    Uses an in-memory SQLite database so we don't touch the real Supabase database.
    """
    test_app = create_app()
    test_app.config.update({
        "TESTING": True,
        # Use a temporary in-memory database just for tests
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-jwt-secret"
    })

    # Create all the tables in the test database
    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """A test client to make fake HTTP requests to our Flask app."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """A database session for tests that need to add/read records directly."""
    with app.app_context():
        yield _db.session
        # Clean up after each test
        _db.session.rollback()


# --- Sample Data Fixtures ---

@pytest.fixture
def test_lecturer(db_session):
    """A sample lecturer user for tests."""
    lecturer = User(
        fullname="Dr. Emily Carter",
        email="emily.carter@university.edu",
        password_hash="$2b$12$fakehashfortest",
        role="lecturer"
    )
    db_session.add(lecturer)
    db_session.commit()
    db_session.refresh(lecturer)
    return lecturer


@pytest.fixture
def test_student(db_session):
    """A sample student user for tests."""
    student = User(
        fullname="Alex Student",
        email="alex.student@university.edu",
        password_hash="$2b$12$fakehashfortest",
        role="student"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student


@pytest.fixture
def test_wifi(db_session):
    """A sample WiFi network for tests."""
    wifi = WifiNetwork(
        ssid="Uni-Campus-WiFi",
        description="Main Campus Lecture Halls",
        location="Engineering Block B"
    )
    db_session.add(wifi)
    db_session.commit()
    db_session.refresh(wifi)
    return wifi
