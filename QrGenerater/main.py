import qrcode

url = input("Enter the URL to generate QR code: ").strip()
file_path = "D:/Git Repository/PyFusion/QrGenerater/qrcode.png"

qr = qrcode.QRCode()

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="white", back_color="black")
img.save(file_path)