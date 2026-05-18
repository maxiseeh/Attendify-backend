import re

# Accepts AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF
MAC_PATTERN = re.compile(r'^([0-9A-Fa-f]{2}[:\-]){5}([0-9A-Fa-f]{2})$')


def is_valid_mac(mac_address):
    """Returns True if the MAC address format is valid."""
    if not mac_address:
        return False
    return bool(MAC_PATTERN.match(mac_address))


def normalize_mac(mac_address):
    """Converts MAC address to uppercase with colons: AA:BB:CC:DD:EE:FF"""
    return mac_address.replace("-", ":").upper()


def macs_match(mac1, mac2):
    """Returns True if two MAC addresses refer to the same device."""
    return normalize_mac(mac1) == normalize_mac(mac2)
