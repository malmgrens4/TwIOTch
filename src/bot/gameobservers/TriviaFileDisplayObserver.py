import logging
import os
import asyncio
import shutil
from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot
from src.bot.gameobservers.utils import create_trivia_display
from typing import Dict

class TriviaFileDisplayObserver(Observer):
    display_file_path = os.environ['DISPLAY_FILE_PATH']
    image_template_file_name = 'trivia_image_template.png'
    on_path = os.path.join(display_file_path, 'on/').replace("\\", "/")
    off_path = os.path.join(display_file_path, 'off/').replace("\\", "/")
    question_path = os.path.join(display_file_path, "question.txt")

    def __init__(self):
        self.display_on = False

    async def update(self, subject: TriviaBot) -> None:
        """Toggle all trivia displays to sync with game."""
        if not self.display_on and subject.game_started:
            self.display_on = True
            create_trivia_display(subject.question, subject.options)

        if subject.won:
            correct_options: Dict[str, str] = {}
            # create a display with only right answers
            for key, value in subject.options.items():
                if key in subject.correct_options:
                    correct_options[key] = value

            create_trivia_display(subject.question, correct_options)

        # if the time between rounds is greater than 5 seconds display the answers then delete it
        # otherwise just delete the trivia_question.png file
        await asyncio.sleep(os.environ[''])

    @staticmethod
    def write_to_path(file_path, content: str = ""):
        """Writes empty space to file."""
        option_file = open(file_path, 'w')
        option_file.write(content + " "*10)

    @staticmethod
    def toggle_file_display(visible: bool, file_name):
        """Moves the file to on or off depending on current location."""
        file_on_path = os.path.join(TriviaFileDisplayObserver.on_path, file_name)
        file_off_path = os.path.join(TriviaFileDisplayObserver.off_path, file_name)
        if visible:
            if not os.path.exists(file_on_path):
                shutil.move(file_off_path, file_on_path)
        else:
            if not os.path.exists(file_off_path):
                shutil.move(file_on_path, file_off_path)



