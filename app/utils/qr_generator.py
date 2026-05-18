import qrcode
import io
import base64


def generate_qr_code(data):
    """Generates a QR code from any string and returns it as a base64 image."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def generate_qr_and_save_to_file(data, file_path):
    """Generates a QR code and saves it as a PNG file to disk."""
    img = qrcode.make(data)
    img.save(file_path)
    return file_path
