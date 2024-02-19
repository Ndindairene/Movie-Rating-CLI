# models.py
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import func

engine = create_engine('sqlite:///movie_ratings.db')
Base = declarative_base()

# Create tables in the database
Base.metadata.create_all(bind=engine)

movie_user_association = Table(
    'movie_user_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    director = Column(String)
    genre = Column(String)
    release_year = Column(Integer)

    ratings = relationship('Rating', back_populates='movie')
    users = relationship('User', secondary=movie_user_association, back_populates='movies')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    age = Column(Integer)

    ratings = relationship('Rating', back_populates='user')
    movies = relationship('Movie', secondary=movie_user_association, back_populates='users')

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='ratings')

    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movie', back_populates='ratings')
