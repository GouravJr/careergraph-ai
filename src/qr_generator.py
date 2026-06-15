from io import BytesIO

import qrcode


def generate_qr_png_bytes(url: str) -> bytes:
    """
    Generate a QR code PNG in memory and return it as bytes.
    No file is saved locally.
    """
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()