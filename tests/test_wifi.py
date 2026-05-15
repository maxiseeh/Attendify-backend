# tests/test_wifi.py
# Tests for the WiFi scanning endpoint.
# These tests check that the WiFi scan route works correctly.


def test_wifi_scan_requires_login(client):
    """
    Test that the WiFi scan endpoint requires a login token.
    If no token is provided, it should return 401 Unauthorized.
    """

    response = client.get("/api/wifi/scan")

    # Should be rejected because no JWT token was provided
    assert response.status_code == 401


def test_mac_address_validation():
    """
    Test that our MAC address validator works correctly.
    A MAC address must be in the format: AA:BB:CC:DD:EE:FF
    """
    from app.utils.mac_verifier import is_valid_mac, normalize_mac

    # Valid MAC addresses
    assert is_valid_mac("AA:BB:CC:DD:EE:FF") is True
    assert is_valid_mac("aa:bb:cc:dd:ee:ff") is True
    assert is_valid_mac("AA-BB-CC-DD-EE-FF") is True

    # Invalid MAC addresses
    assert is_valid_mac("not-a-mac") is False
    assert is_valid_mac("") is False
    assert is_valid_mac(None) is False

    # Normalization
    assert normalize_mac("aa-bb-cc-dd-ee-ff") == "AA:BB:CC:DD:EE:FF"