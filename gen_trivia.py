import requests
import html
from src.bot.db.schema import session_factory
from src.bot.db.schema import TriviaQuestion
from src.bot.db.schema import TriviaOption


def add_trivia_to_db(token: str = None):
    if not token:
        response = requests.get("https://opentdb.com/api_token.php?command=request")
        token_json = response.json()
        token = token_json['token']

    response = requests.get("""https://opentdb.com/api.php?amount=50&token=%s""" % token)
    questions_json = response.json()
    results = questions_json['results']

    session = session_factory()

    for result in results:
        new_question = TriviaQuestion(category=result['category'], question=html.unescape(result['question']))
        session.add(new_question)
        session.commit()
        question_id = new_question.id

        # add correct answer
        session.add(TriviaOption(question_id=question_id,
                                 option=html.unescape(result['correct_answer']),
                                 is_correct=True))
        # add incorrect answers
        for option in result['incorrect_answers']:
            session.add(TriviaOption(question_id=question_id, option=html.unescape(option), is_correct=False))

    session.commit()


if __name__ == "__main__":
    add_trivia_to_db()
