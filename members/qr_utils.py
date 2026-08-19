import qrcode
import qrcode.image.svg
from io import BytesIO

def make_qr_svg(data):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgImage)
    buf = BytesIO()
    img.save(buf)
    return buf.getvalue()
