from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError
from datetime import timedelta
from bcrypt import hashpw, checkpw, gensalt
from app.schemas.user_schema import UserSchema, UserLoginSchema, UserProfileSchema

class AuthService:
    @staticmethod
    def register(data):
        try:
            schema = UserSchema()
            validated_data = schema.load(data)
            hashed_pwd = hashpw(
                validated_data['password'].encode('utf-8'),
                gensalt()
            ).decode('utf-8')
            
            return {
                "message": "Registration successful",
                "email": validated_data['email'],
                "role": validated_data['role']
            }, 201
        
        except ValidationError as e:
            return {"errors": e.messages}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def login(data):
        try:
            schema = UserLoginSchema()
            validated_data = schema.load(data)
            
            access_token = create_access_token(
                identity=validated_data['email'],
                expires_delta=timedelta(hours=24)
            )
            
            return {
                "message": "Login successful",
                "access_token": access_token  
            }, 200
        
        except ValidationError as e:
            return {"errors": e.messages}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def logout(user_id):
        try:
            return {"message": "Logged out successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def profile(user_id):
        try:
            return {"message": "Profile fetched"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def refresh_token(user_id):
        try:
            return {
                "message": "Token refreshed"
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500