import os
import logging
from PIL import Image, ImageFont, ImageDraw
from typing import Dict


class Box:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class TextBox:
    def __init__(self, box: Box,
                 font_path: str, font_size: int, min_font_size: int,
                 text: str, wrap: bool = True, center: bool = True):
        self.box = box
        self.text = text
        self.wrap = wrap
        self.font_path = font_path
        self.font = ImageFont.truetype(font_path, font_size)
        self.min_font_size = min_font_size
        self.center = center

    def fit_font(self, draw: ImageDraw, cur_font: ImageFont):
        self.font = cur_font
        if cur_font.size <= self.min_font_size:
            self.font = cur_font

        cur_text_width, cur_text_height = \
            draw.textsize(self.text, font=ImageFont.truetype(self.font_path, cur_font.size))

        if cur_text_width > self.box.width:
            return self.fit_font(draw, ImageFont.truetype(self.font_path, cur_font.size - 1))

        return self.font

    def split_lines(self, draw: ImageDraw) -> list[str]:
        words = self.text.split(" ")
        lines: list[str] = []
        while len(words) > 0:
            cur_line = []
            cur_line_width = 0
            line_complete = False
            while not line_complete and len(words) > 0:
                word = words.pop(0)
                cur_text_width, cur_text_height = draw.textsize(word + " ", font=self.font)

                cur_line.append(word)
                cur_line_width += cur_text_width
                if cur_line_width >= self.box.width:
                    line_complete = True

            lines.append(" ".join(cur_line))

        return lines

    def wrap_text(self, draw: ImageDraw):
        # start from the initial font size - wrap one word.
        # see if it fits given the width and height constraints
        sections: list[str] = self.split_lines(draw)
        cur_text_width, cur_text_height = draw.multiline_textsize("\n".join(sections), font=self.font)

        if self.center:
            # we only want to center the y. The x will be done per line
            _x, y = (self.box.x + ((self.box.width - cur_text_width) / 2),
                     self.box.y + (self.box.height - (cur_text_height / 2)))

            for section in sections:
                cur_text_width, cur_text_height = \
                    draw.textsize(section + " ", font=self.font)

                cur_x, _y = (self.box.x + ((self.box.width - cur_text_width) / 2),
                                y + (self.box.height - (cur_text_height / 2)))

                draw.text((cur_x + 1, y), section, (0, 0, 0), font=self.font)
                draw.text((cur_x, y), section, (255, 255, 255), font=self.font)

                y += cur_text_height

        else:
            x, y = self.box.x, self.box.y
            draw.multiline_text((x, y), "\n".join(sections), font=self.font)

    def draw_text(self, draw: ImageDraw):
        if self.wrap:
            self.wrap_text(draw)

        else:
            self.font = self.fit_font(draw, self.font)

            cur_text_width, cur_text_height = draw.textsize(self.text + " ", font=self.font)

            if self.center:
                x, y = (self.box.x + ((self.box.width - cur_text_width) / 2),
                        self.box.y + (self.box.height - (cur_text_height / 2)))
            else:
                x, y = self.box.x, self.box.y

            draw.text((x + 1, y), self.text, (0, 0, 0), font=self.font)
            draw.text((x, y), self.text, (255, 255, 255), font=self.font)


def create_trivia_display(question: str, options: Dict[str, str]):
    trivia_template_path = os.path.join(os.environ['DISPLAY_FILE_PATH'],
                                        os.environ['TRIVIA_TEMPLATE_FILE_NAME']).replace("\\", "/")
    output_path = os.path.join(os.environ['DISPLAY_FILE_PATH'],
                               os.environ['TRIVIA_QUESTION_FILE_NAME']).replace("\\", "/")
    font_path = os.path.join(os.environ['FONT_PATH'], os.environ['FONT']).replace("\\", "/")
    box_map = {'a': Box(x=200, y=402, width=620, height=50),
               'b': Box(x=1100, y=402, width=620, height=50),
               'c': Box(x=200, y=560, width=620, height=50),
               'd': Box(x=1100, y=560, width=620, height=50)}
    try:
        template_image: Image = Image.open(trivia_template_path)
        draw = ImageDraw.Draw(template_image)

        question_box = Box(x=270, y=130, width=1380, height=83)
        question_textbox = TextBox(box=question_box,
                                   font_path=font_path,
                                   font_size=60,
                                   min_font_size=60,
                                   text=question)

        question_textbox.draw_text(draw)

        for letter, option_text in options.items():
            option_textbox = TextBox(box=box_map[letter],
                                     font_path=font_path,
                                     font_size=50,
                                     min_font_size=20,
                                     text=f"{letter}. {option_text}",
                                     wrap=False,
                                     center=False)

            option_textbox.draw_text(draw)

        template_image.save(output_path)
        return draw

    except Exception as err:
        logging.exception("Issue creating trivia image", err)


def test():
    question = "In Fallout: New Vegas, upon starting each one of the four campaign DLCs, which one of them does not have a warning screen/recommended level?"
    options = {'a': 'Thats exactly', 'b': 'no way', 'c': 'the ...', 'd': 'it just so happens'}
    create_trivia_display(question, options)


def test_position(x: int, y: int, text: str = "x"):
    display_path = os.environ['DISPLAY_FILE_PATH']
    trivia_template_path = os.path.join(display_path, 'trivia_image_template.png').replace("\\", "/")
    output_path = os.path.join(display_path, 'trivia_question.png').replace("\\", "/")
    font_path = os.path.join(display_path, 'fonts/Roboto-Black.ttf').replace("\\", "/")

    template_image: Image = Image.open(trivia_template_path)
    draw = ImageDraw.Draw(template_image)
    draw.text((x, y), text, (255, 255, 255), font=ImageFont.truetype(font_path, 40))
    template_image.save(output_path)

test()


