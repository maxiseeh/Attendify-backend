from datetime import datetime, timedelta
from marshmallow import ValidationError

from app.utils.duration_calculator import get_current_utc_time, calculate_duration


class ConnectionService:

    @staticmethod
    def create_log(data):
        try:
            required = ['device_id', 'connected_at', 'status']
            for field in required:
                if field not in data:
                    return {"error": f"Missing {field}"}, 400

            if data['status'] not in ['connected', 'disconnected']:
                return {"error": "Invalid status"}, 400

            

            return {
                "message": "Connection logged",
                "device_id": data['device_id'],
                "status": data['status']
            }, 201
        
        except ValidationError as e:
            return {"errors": e.messages}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def log_connection(device_id):
        try:
            data = {
                'device_id': device_id,
                'connected_at': get_current_utc_time(),
                'status': 'connected'
            }
            _, status = ConnectionService.create_log(data)
            return status == 201
        except:
            return False

    @staticmethod
    def log_disconnection(device_id, connected_at):
        try:
            data = {
                'device_id': device_id,
                'connected_at': connected_at,
                'disconnected_at': get_current_utc_time(),
                'status': 'disconnected'
            }
            _, status = ConnectionService.create_log(data)
            return status == 201
        except:
            return False

    @staticmethod
    def get_active_connections():
        try:
            

            return {
                "message": "Active connections retrieved"
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_device_history(device_id, limit=100):
        try:
            

            return {
                "message": "History retrieved",
                "device_id": device_id
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_statistics():
        try:
            

            return {
                "message": "Statistics generated",
                "generated_at": datetime.utcnow().isoformat()
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_daily_statistics():
        try:
            

            return {
                "message": "Daily stats retrieved",
                "generated_at": datetime.utcnow().isoformat()
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def cleanup_old_logs(days=30):
        try:
            cutoff = datetime.utcnow() - timedelta(days=days)

            

            return {
                "message": f"Cleaned logs older than {days} days"
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500
