from marshmallow import ValidationError
from datetime import datetime

from app.schemas.device_schema import DeviceSchema, DeviceListSchema
from app.utils.mac_verifier import is_valid_mac, normalize_mac


class DeviceService:

    @staticmethod
    def register_device(data):
        try:
            schema = DeviceSchema()
            validated_data = schema.load(data)

            if not is_valid_mac(validated_data['mac_address']):
                return {"error": "Invalid MAC address format"}, 400

            mac = normalize_mac(validated_data['mac_address'])

            # TODO: Save device to database

            return {
                "message": "Device registered successfully",
                "mac_address": mac,
                "device_name": validated_data['device_name']
            }, 201
        
        except ValidationError as e:
            return {"errors": e.messages}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_user_devices(user_id):
        try:
            # TODO: Query devices for this user

            return {
                "message": "Devices retrieved",
                "user_id": user_id
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_device(device_id):
        try:
            # TODO: Find device by ID

            return {"message": "Device retrieved"}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def update_device(device_id, data, user_id):
        try:
            # TODO: Check ownership and update device

            return {"message": "Device updated successfully"}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def delete_device(device_id, user_id):
        try:
            

            return {"message": "Device deleted successfully"}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_mac(mac_address):
        try:
            if not is_valid_mac(mac_address):
                return {"error": "Invalid MAC address"}, 400

            mac = normalize_mac(mac_address)

            

            return {"message": "Device found", "mac_address": mac}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def check_device_exists(mac_address):
        try:
            mac = normalize_mac(mac_address)
            
            return True
        except:
            return False

    @staticmethod
    def update_last_seen(device_id):
        try:
            
            return True
        except:
            return False
