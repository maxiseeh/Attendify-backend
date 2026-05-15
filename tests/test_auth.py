"""
tests/test_auth.py
Authentication & Authorization Tests
"""
import pytest
from fastapi.testclient import TestClient


def test_register_student(client):
    response = client.post("/auth/register", json={
        "fullname": "New Student One",
        "email": "newstudent123@university.edu",
        "password": "SecurePass123!",
        "role": "student"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newstudent123@university.edu"
    assert data["role"] == "student"


def test_register_duplicate_email(client, test_student):
    response = client.post("/auth/register", json={
        "fullname": "Duplicate Student",
        "email": test_student.email,
        "password": "SecurePass123!",
        "role": "student"
    })
    assert response.status_code == 400  # or 409 depending on your implementation


def test_login_success(client, test_student):
    # Note: You'll need to adjust this based on your actual login endpoint
    response = client.post("/auth/login", json={
        "email": test_student.email,
        "password": "SecurePass123!"   # In real test you might need to hash properly
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_student):
    response = client.post("/auth/login", json={
        "email": test_student.email,
        "password": "WrongPassword123!"
    })
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401  # Unauthorized