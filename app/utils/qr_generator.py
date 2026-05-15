# qr_generator.py
# This file generates QR codes that users can scan to check in to a session.
# The QR code contains a session ID or a URL that the app then reads.

import qrcode
import io
import base64


def generate_qr_code(data):
    """
    Generate a QR code from any text or URL.
    Returns the QR code image as a base64 string.
    Base64 is useful because we can send it directly to the frontend as text.

    Example:
        qr_string = generate_qr_code("session-id-12345")
        # Then send qr_string to the frontend and show it as an image
    """
    # Set up the QR code settings
    qr = qrcode.QRCode(
        version=1,                          # Size of the QR code (1 is small, 40 is big)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Some damage tolerance
        box_size=10,                        # Size of each box in pixels
        border=4,                           # White space around the QR code
    )

    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Turn it into a black and white image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to memory (we don't need to save it to a file)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Convert the image bytes to a base64 string
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return img_base64


def generate_qr_and_save_to_file(data, file_path):
    """
    Generate a QR code and save it as a PNG image file on disk.
    Useful when you want to store the QR image somewhere.

    Example:
        generate_qr_and_save_to_file("session-id-12345", "qrcodes/session1.png")
    """
    img = qrcode.make(data)
    img.save(file_path)
    return file_path