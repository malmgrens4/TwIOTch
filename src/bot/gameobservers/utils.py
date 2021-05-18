import os
import PIL
import logging
from PIL import Image, ImageFont, ImageDraw
from typing import Dict


class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def create_trivia_display(question: str, options: Dict[str, str]):
    display_path = os.environ['DISPLAY_FILE_PATH']
    trivia_template_path = os.path.join(display_path, 'trivia_image_template.png').replace("\\", "/")
    output_path = os.path.join(display_path, 'trivia_formatted.png').replace("\\", "/")
    font_path = os.path.join(display_path, 'fonts/Roboto-Black.ttf').replace("\\", "/")
    coordinate_map = {'a': Coordinate(300, 200),
                      'b': Coordinate(1000, 200),
                      'c': Coordinate(300, 450),
                      'd': Coordinate(800, 500)}
    try:
        font = ImageFont.truetype(font_path, 12)

        template_image: Image = Image.open(trivia_template_path)
        draw = ImageDraw.Draw(template_image)

        for letter, option_text in options.items():
            text_x = coordinate_map[letter].x
            text_y = coordinate_map[letter].y
            draw.text((text_x + 1, text_y), option_text, (0, 0, 0), font=font)
            draw.text((text_x, text_y), option_text, (255, 255, 255), font=font)

        draw.text((100, 100), question, (0, 0, 0), font=font)
        draw.text((100 + 1, 100), question, (255, 255, 255), font=font)

        template_image.save(output_path)
        return draw

    except Exception as err:
        logging.exception("Issue creating trivia image", err)
