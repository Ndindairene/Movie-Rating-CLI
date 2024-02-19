from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie, User, Rating, movie_user_association
from faker import Faker
import random

DATABASE_URI = 'sqlite:///movie_ratings.db'
engine = create_engine(DATABASE_URI)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def generate_fake_data(num_movies=10, num_users=5):
    fake = Faker()

    # Generate fake movies
    movies = []
    for _ in range(num_movies):
        movie = Movie(
            title=fake.text(30),
            director=fake.name(),
            genre=fake.word(),
            release_year=fake.year()
        )
        session.add(movie)
        movies.append(movie)

    # Generate fake users
    users = []
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            age=fake.random_int(18, 60)
        )
        session.add(user)
        users.append(user)

    session.commit()

    # Generate fake ratings
    for movie in movies:
        for _ in range(10):
            rating = Rating(
                score=fake.random_int(1, 5),
                user_id=fake.random_int(1, num_users),
                movie_id=movie.id
            )
            session.add(rating)

    session.commit()

    # Establish relationships and add entries to association table
    for user in users:
        user.movies = movies  # Establish the relationship
        for movie in movies:
            session.execute(movie_user_association.insert().values(movie_id=movie.id, user_id=user.id))

    session.commit()

    # Generate fake associations
    for user in session.query(User).all():
        for movie in session.query(Movie).all():
            if random.choice([True, False]):
                session.execute(movie_user_association.insert().values(movie_id=movie.id, user_id=user.id))

    session.commit()


if __name__ == "__main__":
    generate_fake_data()
