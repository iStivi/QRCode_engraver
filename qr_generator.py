import qrcode
import qrcode.image.svg

qrstring = "133Gf5WZEJpNN77upypUGGHZU8pW3oui1c"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
    image_factory=qrcode.image.svg.SvgPathImage,
)
factory = qrcode.image.svg.SvgImage
qr.add_data(qrstring)
qr.make(fit=True)
img = qr.make_image()
img.save("test.svg")
