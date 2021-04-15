import logging
import random
from collections import Callable

from twitchio.dataclasses import Message
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import func
from src.bot.gameobservers.BalloonBoxObserver import BalloonBoxTeamObserver
from src.bot.gameobservers.RoundsObserver import RoundsObserver
from src.bot.gameobservers.TriviaChatObserver import TriviaChatObserver
from src.bot.gameobservers.TriviaAnswerTimerObserver import TriviaAnswerTimerObserver
from src.bot.db.schema import session_scope, Session, TriviaQuestion, TriviaOption
from src.bot.botstates.TriviaBot import TriviaBot
from src.bot.botstates.BotState import BotState
from src.bot.TeamData import TeamData
from src.bot.gameobservers.WinGameChatObserver import WinGameChatObserver
from src.bot.gameobservers.TriviaDBObserver import TriviaDBObserver

max_message_length = 500


async def categories(msg: Message):
    with session_scope() as session:
        category_query = session.query(TriviaQuestion.category).distinct().all()
        categories_joined: str = " | ".join([row[0] for row in category_query])
        if categories_joined:
            logging.error("No categories. Database trivia may need to be populated.")
        category_section: str = categories_joined[0]
        for i in range(1, len(categories_joined)):
            # TODO make this more generic for all messages
            if i % max_message_length == 0:
                await msg.channel.send(category_section)
                category_section = ""

            category_section += categories_joined[i]

        if category_section != "":
            await msg.channel.send(category_section)


async def start_trivia(send_message: Callable[[str]], category: str, team_data: TeamData, botState: BotState):
    if len(team_data.teams) == 0:
        await send_message("The teams have no players. Use !joingame to participate.")
        return



    trivia_response = get_random_trivia(category)
    if not trivia_response:
        await send_message("Failed to find any trivia questions. Try another category.")
        return

    trivia_question, trivia_options = trivia_response
    options_map = {}
    for i, option in enumerate(trivia_options):
        options_map[chr(i + 97)] = option.option

    correct_options = [chr(i + 97) for i, option in enumerate(trivia_options) if option.is_correct]

    trivia_bot = TriviaBot(team_data=team_data,
                           question=trivia_question.question,
                           options=options_map,
                           correct_options=correct_options,
                           send_message=send_message)
    trivia_bot.attach(TriviaChatObserver())
    trivia_bot.attach(TriviaAnswerTimerObserver())
    trivia_bot.attach(TriviaDBObserver())
    trivia_bot.attach(WinGameChatObserver())
    # trivia_bot.attach(BalloonBoxTeamObserver())
    trivia_bot.attach(RoundsObserver())
    botState.transition_to(trivia_bot)
    await trivia_bot.game_start()
    return


def get_random_trivia(category: str = None) -> tuple[TriviaQuestion, [TriviaOption]]:
    session = Session()
    question_query: Query = session.query(TriviaQuestion)
    if category:
        question_query: Query = question_query.filter(func.replace(TriviaQuestion.category, ' ', '').contains(category))

    question_row: TriviaQuestion = question_query.order_by(func.random()).first()

    options = session.query(TriviaOption).filter(TriviaOption.question_id == question_row.id).all()
    random.shuffle(options)
    return question_row, options
