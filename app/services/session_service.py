# session_service.py
# This file handles everything related to lecture sessions.
# A session is like a class period — a lecturer starts one, students attend it,
# and then it gets closed when the class is over.

from datetime import datetime


class SessionService:

    @staticmethod
    def list_sessions():
        """
        Get all sessions from the database.
        For now returns an empty list — will be filled in when models are connected.
        """
        try:
            # TODO: Replace with actual database query
            # sessions = Session.query.all()
            # return {"sessions": [s.to_dict() for s in sessions]}, 200

            return {"message": "Sessions retrieved", "sessions": []}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create_session(data):
        """
        Create a new lecture session.
        Requires session_name, wifi_network_id, and lecturer_id.
        """
        try:
            # Check that all required fields are provided
            required_fields = ['session_name', 'wifi_network_id', 'lecturer_id']
            for field in required_fields:
                if field not in data:
                    return {"error": f"Missing field: {field}"}, 400

            # TODO: Save session to database
            # new_session = Session(
            #     session_name=data['session_name'],
            #     wifi_network_id=data['wifi_network_id'],
            #     lecturer_id=data['lecturer_id'],
            #     start_time=datetime.utcnow(),
            #     is_active=True
            # )
            # db.session.add(new_session)
            # db.session.commit()

            return {
                "message": "Session created successfully",
                "session_name": data['session_name']
            }, 201

        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def update_session(session_id, data):
        """
        Update an existing session (like changing its name or end time).
        """
        try:
            # TODO: Find and update the session in the database
            # session = Session.query.get(session_id)
            # if not session:
            #     return {"error": "Session not found"}, 404
            # session.update(**data)
            # db.session.commit()

            return {"message": "Session updated", "session_id": session_id}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def close_session(session_id):
        """
        Close/end an active session.
        Sets is_active to False and records the end time.
        """
        try:
            # TODO: Find and close the session
            # session = Session.query.get(session_id)
            # if not session:
            #     return {"error": "Session not found"}, 404
            # session.is_active = False
            # session.end_time = datetime.utcnow()
            # db.session.commit()

            return {"message": "Session closed successfully", "session_id": session_id}, 200

        except Exception as e:
            return {"error": str(e)}, 500