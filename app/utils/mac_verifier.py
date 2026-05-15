# mac_verifier.py
# This file helps with MAC address validation and formatting.
# A MAC address is a unique ID that every device (phone, laptop, etc.) has on its network card.
# Example of a MAC address: A1:B2:C3:D4:E5:F6

import re

# This pattern checks if a MAC address looks right.
# It allows formats like AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF
MAC_PATTERN = re.compile(r'^([0-9A-Fa-f]{2}[:\-]){5}([0-9A-Fa-f]{2})$')


def is_valid_mac(mac_address):
    """
    Check if the given MAC address is in a valid format.
    Returns True if it looks correct, False if not.
    """
    if not mac_address:
        return False

    return bool(MAC_PATTERN.match(mac_address))


def normalize_mac(mac_address):
    """
    Convert a MAC address to a standard format: uppercase with colons.
    Example: aa-bb-cc-dd-ee-ff  →  AA:BB:CC:DD:EE:FF
    This makes it easier to compare MAC addresses in the database.
    """
    # Replace dashes with colons, then make everything uppercase
    return mac_address.replace("-", ":").upper()


def macs_match(mac1, mac2):
    """
    Compare two MAC addresses to see if they are the same device.
    This ignores formatting differences like dashes vs colons or uppercase vs lowercase.
    """
    return normalize_mac(mac1) == normalize_mac(mac2)