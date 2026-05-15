# user_schema.py
# This file defines how user data should look and how to validate it.
# We use Marshmallow library to help with this validation and conversion.

from marshmallow import Schema, fields, validate, ValidationError
from email_validator import validate_email, EmailNotValidError


class UserSchema(Schema):
    """
    Schema for validating user data (students and teachers).
    It checks that all required fields are present and correct format.
    """
    
    # User ID - this comes from the database, not user input
    id = fields.Int(dump_only=True)  # dump_only means we only send this in responses, never accept it from users
    
    # User's full name - required and must have at least 2 characters
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "Name is required"}
    )
    
    # User's email - required and must be a valid email format
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required", "invalid": "Email format is invalid"}
    )
    
    # User's password - required, must be strong (at least 6 characters)
    # We only accept this during registration/login, never send it back
    password = fields.Str(
        required=True,
        load_only=True,  # load_only means we only accept this, never send it back
        validate=validate.Length(min=6, max=255),
        error_messages={"required": "Password is required"}
    )
    
    # User's role: "student" or "teacher" or "admin"
    role = fields.Str(
        required=True,
        validate=validate.OneOf(["student", "teacher", "admin"]),
        error_messages={"required": "Role is required"}
    )
    
    # Phone number - optional but if provided, should be valid
    phone = fields.Str(
        required=False,
        validate=validate.Length(min=10, max=15),
        allow_none=True
    )
    
    # When the user account was created (auto-set by database)
    created_at = fields.DateTime(dump_only=True)
    
    # When the user account was last updated
    updated_at = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    """
    Simpler schema just for login - only needs email and password.
    """
    
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserProfileSchema(Schema):
    """
    Schema for displaying user profile - excludes sensitive data like password.
    """
    
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    role = fields.Str()
    phone = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
