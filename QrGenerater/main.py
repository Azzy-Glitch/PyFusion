import qrcode

url = input("Enter the URL to generate QR code: ").strip()
file_path = "D:/Git Repository/PyFusion/QrGenerater/qrcode.png"

qr = qrcode.QRCode(
    # version=1,
    # error_correction=qrcode.constants.ERROR_CORRECT_H,
    # box_size=10,
    # border=4,
)

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save(file_path)