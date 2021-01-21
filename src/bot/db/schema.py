from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    correct_answers = Column(Integer, nullable=False, default=0)


class TriviaQuestion(Base):
    __tablename__ = 'trivia_question'
    id = Column(Integer, primary_key=True)
    question = Column(String(250), nullable=False)
    options = relationship("Options")


class TriviaOption(Base):
    __tablename__ = 'trivia_option'
    id = Column(Integer, primary_key=True)
    option = Column(String(250), nullable=False)
    question_id = Column(Integer, ForeignKey('trivia_question.id'))


engine = create_engine('sqlite:///twitch_db.db')
Base.metadata.create_all(engine)


