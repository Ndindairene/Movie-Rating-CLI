from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie, User
from faker import Faker

DATABASE_URI = 'sqlite:///movie_ratings.db'
engine = create_engine(DATABASE_URI)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def generate_fake_data(num_movies=10, num_users=5):
    fake = Faker()

    # Generate fake movies
    for _ in range(num_movies):
        movie = Movie(
            title=fake.text(20),
            director=fake.name(),
            genre=fake.word(),
            release_year=fake.year()
        )
        session.add(movie)

    # Generate fake users
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            age=fake.random_int(18, 60)
        )
        session.add(user)

    session.commit()

if __name__ == "__main__":
    generate_fake_data()
