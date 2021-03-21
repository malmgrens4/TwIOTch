from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert


Base = declarative_base()


# Probably not best practice but add OR IGNORE prefix for insert statements
@compiles(Insert)
def _prefix_insert_with_ignore(insert, compiler, **kw):
    return compiler.visit_insert(insert.prefix_with('OR IGNORE'), **kw)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    trivia_points = Column(Integer, nullable=False, default=0)
    number_game_wins = Column(Integer, nullable=False, default=0)


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class TriviaQuestion(Base):
    __tablename__ = 'trivia_question'
    id = Column(Integer, primary_key=True)
    category = Column(String(250), nullable=False)
    question = Column(String(250), nullable=False)
    options = relationship("TriviaOption")


class TriviaOption(Base):
    __tablename__ = 'trivia_option'
    id = Column(Integer, primary_key=True)
    option = Column(String(250), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey('trivia_question.id'), nullable=False)


engine = create_engine('sqlite:///twitch_db.db')
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except BaseException as err:
        session.rollback()
        raise err
    finally:
        session.close()
