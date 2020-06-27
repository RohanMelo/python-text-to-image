import os
import io
import requests
import tempfile
from PIL import Image, ImageDraw, ImageFont
import textwrap


# First, download image from an url. Note: Pathlib did not work in this case
is_finished = False
out_dir = os.getcwd()
img_url = input("Type image url: ")
buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
request = requests.get(img_url, stream=True)

if request.status_code == 200:
    downloaded = 0
    filesize = int(request.headers['content-length'])
    for chunk in request.iter_content():
        downloaded += len(chunk)
        buffer.write(chunk)
        print(downloaded/filesize)
    buffer.seek(0)
    image = Image.open(io.BytesIO(buffer.read()))
    image.save(os.path.join(out_dir, os.path.basename(img_url)), quality=85)
    is_finished = True
buffer.close()


def generate_text(image_path, top_text, bottom_text='', font_path='./fonts/impact.ttf', font_size=9):

    # Time to load the downloaded image
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size

    # Loading font
    font = ImageFont.truetype(
        font=font_path, size=int(image_height * font_size) // 100)

    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # First part of placing text in the image: wrapping it
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # Divide in lines for placement on top
    y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    # and bottom
    y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    # Finally save the image
    im.save('text-' + im.filename.split('/')[-1])
    # Opens the final image and shows to the user
    im.show()


if __name__ == '__main__':
    if is_finished:
        top_text = input("Type top text: ")
        bottom_text = input("Type bottom text: ")
        generate_text(os.path.basename(img_url), top_text=top_text, bottom_text=bottom_text)



