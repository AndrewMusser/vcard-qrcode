import qrcode
from PIL import Image, ImageDraw, ImageOps
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask

vcard_data = ""
with open('../data/contact.vcf', 'r', encoding='utf-8') as file:
    vcard_data = file.read()

# Generate the QR code with customized colors
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for embedding a logo
    box_size=8,
    border=4,
)
qr.add_data(vcard_data)
qr.make(fit=True)

# Create the QR code image with custom colors (change 'fill' and 'back_color')
img = qr.make_image(
    image_factory=StyledPilImage,
    embeded_image_path="../data/Logo-with-circle.png",
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(back_color=(234,224,218), front_color=(84, 176, 251))
)

# Add rounded corners to the QR code
def add_rounded_corners(image, radius):
    # Create a rounded mask
    rounded_mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(rounded_mask)
    draw.rounded_rectangle((0, 0) + image.size, radius=radius, fill=255)
    
    # Apply the rounded mask to the image
    rounded_img = ImageOps.fit(image, image.size)
    rounded_img.putalpha(rounded_mask)
    return rounded_img

# Apply rounded corners to the QR code
img = add_rounded_corners(img, radius=50)

# Save and show the customized QR code
img.save("../data/vcard_qrcode.png")
img.show()
