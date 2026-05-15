# tests/test_auth.py
# Tests for the registration and login endpoints.
# We check that users can sign up, log in, and get rejected if they give wrong info.


def test_register_student(client):
    """Test that a new student can register successfully."""

    response = client.post("/api/auth/register", json={
        "name": "New Student One",
        "email": "newstudent123@university.edu",
        "password": "SecurePass123",
        "role": "student"
    })

    # Should return 201 Created
    assert response.status_code == 201


def test_register_missing_fields(client):
    """Test that registration fails if required fields are missing."""

    response = client.post("/api/auth/register", json={
        "email": "incomplete@university.edu"
        # Missing name, password, role
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_login_missing_fields(client):
    """Test that login fails if email or password is missing."""

    response = client.post("/api/auth/login", json={
        "email": "someone@university.edu"
        # Missing password
    })

    # Should return 400 Bad Request
    assert response.status_code == 400


def test_profile_without_token(client):
    """Test that accessing your profile without being logged in is rejected."""

    response = client.get("/api/auth/profile")

    # Should return 401 Unauthorized (no token provided)
    assert response.status_code == 401