import os
import logging
from PIL import Image, ImageFont, ImageDraw
from typing import Dict

from PIL.ImageFont import FreeTypeFont


class TextBox:
    def __init__(self, x: int, y: int, width: int, height: int, font_path: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_path = font_path

    def get_fitted_font(self, draw: ImageDraw, text: str, font: FreeTypeFont):
        if font.size == 0:
            return font

        cur_text_width, cur_text_height = draw.textsize(text, font=ImageFont.truetype(self.font_path, font.size))
        if self.x + cur_text_width > self.x + self.width:
            return self.get_fitted_font(draw, text, ImageFont.truetype(self.font_path, font.size - 1))

        return font


def create_trivia_display(question: str, options: Dict[str, str]):
    display_path = os.environ['DISPLAY_FILE_PATH']
    trivia_template_path = os.path.join(display_path, 'trivia_image_template.png').replace("\\", "/")
    output_path = os.path.join(display_path, 'trivia_question.png').replace("\\", "/")
    font_path = os.path.join(display_path, 'fonts/Roboto-Black.ttf').replace("\\", "/")
    textbox_map = {'a': TextBox(x=198, y=402, width=620, height=50, font_path=font_path),
                   'b': TextBox(x=1100, y=402, width=620, height=50, font_path=font_path),
                   'c': TextBox(x=198, y=560, width=620, height=50, font_path=font_path),
                   'd': TextBox(x=1100, y=560, width=620, height=50, font_path=font_path)}
    try:
        template_image: Image = Image.open(trivia_template_path)
        draw = ImageDraw.Draw(template_image)

        question_font = ImageFont.truetype(font_path, 50)
        question_textbox = TextBox(x=270, y=197, width=1380, height=83, font_path=font_path)
        # TODO if our determined font size is less than the min
        # TODO then attempt to wrap the text working backwards through whitespaces
        for letter, option_text in options.items():
            option_font = ImageFont.truetype(font_path, 40)

            option_textbox = textbox_map[letter]

            option_font = option_textbox.get_fitted_font(draw, option_text, option_font)

            draw.text((option_textbox.x + 1, option_textbox.y), f"{letter}. {option_text}", (0, 0, 0), font=option_font)
            draw.text((option_textbox.x, option_textbox.y), f"{letter}. {option_text}", (255, 255, 255), font=option_font)

        question_font = question_textbox.get_fitted_font(draw, question, question_font)

        draw.text((question_textbox.x, question_textbox.y),
                  question, (0, 0, 0), font=question_font)

        draw.text((question_textbox.x + 1, question_textbox.y),
                  question, (255, 255, 255), font=question_font)

        template_image.save(output_path)
        return draw

    except Exception as err:
        logging.exception("Issue creating trivia image", err)


def test():
    question = "What are the real reasons that the thing you know. Like how does it do that no way that's so crazy the way it does that?"
    options = {'a': 'Thats exactly what I have been saying', 'b': 'no way', 'c': 'the ...', 'd': 'it just so happens'}
    create_trivia_display(question, options)


def test_position(x: int, y: int, text: str = "x"):
    display_path = os.environ['DISPLAY_FILE_PATH']
    trivia_template_path = os.path.join(display_path, 'trivia_image_template.png').replace("\\", "/")
    output_path = os.path.join(display_path, 'trivia_question.png').replace("\\", "/")
    font_path = os.path.join(display_path, 'fonts/Roboto-Black.ttf').replace("\\", "/")

    template_image: Image = Image.open(trivia_template_path)
    draw = ImageDraw.Draw(template_image)
    draw.text((x, y),
              text, (255, 255, 255), font=ImageFont.truetype(font_path, 40))
    template_image.save(output_path)

