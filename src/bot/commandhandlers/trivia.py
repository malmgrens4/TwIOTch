from twitchio.dataclasses import Message
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import func
from src.bot.commandhandlers.utils import parse_args
from src.bot.gameobservers.TriviaChatObserver import TriviaChatObserver
from src.bot.gameobservers.TriviaAnswerTimerObserver import TriviaAnswerTimerObserver
from src.bot.db.schema import session_scope, Session, TriviaQuestion, TriviaOption
from src.bot.botstates.TriviaBot import TriviaBot
from src.bot.botstates.BotState import BotState
from src.bot.TeamData import TeamData


async def categories(msg: Message):
    with session_scope() as session:

        category_query = session.query(TriviaQuestion.category).distinct().all()

        for row in category_query:
            await msg.channel.send("%s" % row[0])


async def start_trivia(msg: Message, team_data: TeamData, botState: BotState):
    if not msg.author.is_mod:
        return

    args = parse_args(msg, ['category'])
    category = args['category']

    trivia_question, trivia_options = get_random_trivia(category)
    if not trivia_question:
        await msg.channel.send("Failed to find any trivia questions. Try another category.")

    options_map = {}
    for i, option in enumerate(trivia_options):
        options_map[chr(i + 97)] = option.option

    correct_responses = [chr(i + 97) for i, option in enumerate(trivia_options) if option.is_correct]

    trivia_bot = TriviaBot(team_data=team_data,
                           question=trivia_question.question,
                           options=trivia_options,
                           correct_responses=correct_responses,
                           msg=msg)

    trivia_bot.attach(TriviaChatObserver())
    trivia_bot.attach(TriviaAnswerTimerObserver())
    botState.transition_to(trivia_bot)
    await trivia_bot.game_start()


def get_random_trivia(category: str = None) -> tuple[TriviaQuestion, [TriviaOption]]:
    session = Session()
    question_query: Query = session.query(TriviaQuestion)
    if category:
        question_query: Query = question_query.filter(TriviaQuestion.category.contains(category))

    question_row: TriviaQuestion = question_query.order_by(func.random()).first()

    options = session.query(TriviaOption).filter(TriviaOption.question_id == question_row.id).all()
    return question_row, options