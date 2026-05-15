# device_schema.py
# This file validates device data - devices are the phones/laptops that students use.
# Each device has a unique MAC address (like a fingerprint for network devices).

from marshmallow import Schema, fields, validate, pre_load
from app.utils.mac_verifier import is_valid_mac, normalize_mac


class DeviceSchema(Schema):
    """
    Schema for validating student devices.
    A device is identified by its MAC address (the unique network identifier).
    """
    
    # Device ID - from database, not from users
    id = fields.Int(dump_only=True)
    
    # User who owns this device
    user_id = fields.Int(required=True)
    
    # MAC address - the unique network ID of the device
    # Example: "A1:B2:C3:D4:E5:F6"
    mac_address = fields.Str(
        required=True,
        validate=validate.Length(min=17, max=17),  # MAC addresses are always 17 characters (with colons)
        error_messages={"required": "MAC address is required"}
    )
    
    # Device name - what the user wants to call it (like "My iPhone" or "Laptop")
    device_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={"required": "Device name is required"}
    )
    
    # Device type: "phone", "laptop", "tablet", etc.
    device_type = fields.Str(
        required=True,
        validate=validate.OneOf(["phone", "laptop", "tablet", "other"]),
        error_messages={"required": "Device type is required"}
    )
    
    # When device was registered
    registered_at = fields.DateTime(dump_only=True)
    
    # When device was last used/seen on the network
    last_seen = fields.DateTime(dump_only=True)
    
    # Is this device currently active/verified?
    is_active = fields.Bool(dump_only=True)
    
    @pre_load
    def normalize_mac_address(self, data, **kwargs):
        """
        Before validation, clean up the MAC address.
        Convert it to standard format: uppercase with colons.
        Example: "a1-b2-c3-d4-e5-f6" becomes "A1:B2:C3:D4:E5:F6"
        """
        if "mac_address" in data and data["mac_address"]:
            data["mac_address"] = normalize_mac(data["mac_address"])
        return data


class DeviceListSchema(Schema):
    """
    Schema for displaying a list of devices.
    Shows all important device info without sensitive data.
    """
    
    id = fields.Int()
    user_id = fields.Int()
    mac_address = fields.Str()
    device_name = fields.Str()
    device_type = fields.Str()
    registered_at = fields.DateTime()
    last_seen = fields.DateTime()
    is_active = fields.Bool()
