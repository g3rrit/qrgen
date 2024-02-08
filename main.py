import sys

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from PIL import ImageFont, ImageDraw 

import click

BG_COLOR = (0, 70, 30)

def add_title(img, title, bg_color, font_file):
    draw = ImageDraw.Draw(img)
    img_w, _ = img.size
    font = ImageFont.truetype(font_file, 150)
    _, _, w, _ = draw.textbbox((0, 0), title, font=font)
    draw.text(((img_w-w)/2, 0), title, fill=bg_color, font=font)
    return img

@click.command()
@click.option("--logo", help="Logo to add in the center of the QR code", required=True)
@click.option('--output', default="qr.png", help="Output file name", required=True)
@click.option('--font', help="Path to a ttf font", required=True)
@click.option('--data', help="Data to encode", required=True)
@click.option('--title', help="Title text", required=True)
@click.option('--color-r', default=0, help="Red color part", required=True)
@click.option('--color-g', default=70, help="Green color part", required=True)
@click.option('--color-b', default=30, help="Blue color part", required=True)
def main(logo, output, font, data, title, color_r, color_g, color_b):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=50,
        border=5,
    )
    qr.add_data(data)

    bg_color = (int(color_r), int(color_g), int(color_b))

    img = qr.make_image(
        fill_color="black",
        back_color="white",
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        embeded_image_path=logo,
        color_mask=RadialGradiantColorMask(edge_color=bg_color),
    )
    img = add_title(img, title, bg_color, font)
    img.save(output)

if __name__ == "__main__":
    main()