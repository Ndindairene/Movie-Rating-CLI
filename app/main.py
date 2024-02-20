import os
import sys
from sqlalchemy import desc
from sqlalchemy import func  # Add this line
from sqlalchemy.orm import sessionmaker
from models import Movie, User, Rating, engine
from tabulate import tabulate
from colorama import Fore, Style


sys.path.append(os.getcwd())

# CLI functionality
def view_movies(session):
    movies = session.query(Movie).all()
    movie_data = [[movie.id, movie.title, movie.release_year] for movie in movies]
    print(tabulate(movie_data, headers=["ID", "Title", "Release Year"], tablefmt="fancy_grid"))

def view_movie_details(session, movie_id):
    movie = session.query(Movie).filter(Movie.id == movie_id).first()
    if movie:
        print(f"{Fore.BLUE}Title:{Style.RESET_ALL} {movie.title}")
        print(f"{Fore.BLUE}Director:{Style.RESET_ALL} {movie.director}")
        print(f"{Fore.BLUE}Genre:{Style.RESET_ALL} {movie.genre}")
        print(f"{Fore.BLUE}Release Year:{Style.RESET_ALL} {movie.release_year}")
        print(f"{Fore.BLUE}Ratings:{Style.RESET_ALL}")
        for rating in movie.ratings:
            print(f"{Fore.GREEN}- User:{Style.RESET_ALL} {rating.user.username}, {Fore.GREEN}Score:{Style.RESET_ALL} {rating.score}")
    else:
        print(f"{Fore.RED}Movie not found.{Style.RESET_ALL}")

def rate_movie(session, user_id, movie_id, score):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        movie = session.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
            session.add(rating)
            session.commit()
            print(f"{Fore.GREEN}Rating added successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Movie not found.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}User not found.{Style.RESET_ALL}")

def create_user(session, username, age):
    user = User(username=username, age=age)
    session.add(user)
    session.commit()
    print(f"{Fore.GREEN}User created successfully.{Style.RESET_ALL}")

def delete_user(session, user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"{Fore.GREEN}User deleted successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}User not found.{Style.RESET_ALL}")

def create_movie(session, title, director, genre, release_year):
    movie = Movie(title=title, director=director, genre=genre, release_year=release_year)
    session.add(movie)
    session.commit()
    print(f"{Fore.GREEN}Movie created successfully.{Style.RESET_ALL}")

def delete_movie(session, movie_id):
    movie = session.query(Movie).filter(Movie.id == movie_id).first()
    if movie:
        session.delete(movie)
        session.commit()
        print(f"{Fore.GREEN}Movie deleted successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Movie not found.{Style.RESET_ALL}")

def view_users(session):
    users = session.query(User).all()
    user_data = [[user.id, user.username, user.age] for user in users]
    print(tabulate(user_data, headers=["ID", "Username", "Age"], tablefmt="fancy_grid"))

def update_user(session, user_id, new_username, new_age):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.username = new_username
        user.age = new_age
        session.commit()
        print(f"{Fore.GREEN}User details updated successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}User not found.{Style.RESET_ALL}")

def update_movie(session, movie_id, new_title, new_director, new_genre, new_release_year):
    movie = session.query(Movie).filter(Movie.id == movie_id).first()
    if movie:
        movie.title = new_title
        movie.director = new_director
        movie.genre = new_genre
        movie.release_year = new_release_year
        session.commit()
        print(f"{Fore.GREEN}Movie details updated successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Movie not found.{Style.RESET_ALL}")

def top_rated_movies(session, num_movies=5):
    # Query movies and their average ratings
    query = (
        session.query(Movie, func.avg(Rating.score).label('average_rating'))
        .join(Rating, Movie.id == Rating.movie_id)
        .group_by(Movie.id)
        .order_by(desc('average_rating'))
        .limit(num_movies)
    )
    top_movies = query.all()

    if top_movies:
        print(f"{Fore.YELLOW}Top {num_movies} Rated Movies:{Style.RESET_ALL}")
        for movie, avg_rating in top_movies:
            print(f"{Fore.GREEN}- {movie.title}:{Style.RESET_ALL} {avg_rating:.2f}")
    else:
        print(f"{Fore.RED}No movies found.{Style.RESET_ALL}")
def main():
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n" + "-"*50)
        print(f"{Fore.CYAN}Welcome to Movie Rating System{Style.RESET_ALL}")
        print("-"*50)
        print("1. View Movies")
        print("2. View Movie Details")
        print("3. Rate Movie")
        print("4. Create User")
        print("5. Delete User")
        print("6. Update User Details")
        print("7. List Users")
        print("8. Create Movie")
        print("9. Delete Movie")
        print("10. Update Movie Details")
        print("11. Top Rated Movies")
        print("12. Exit")
        choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")

        if choice == '1':
            view_movies(session)
        elif choice == '2':
            movie_id = int(input(f"{Fore.YELLOW}Enter the movie ID: {Style.RESET_ALL}"))
            view_movie_details(session, movie_id)
        elif choice == '3':
            user_id = int(input(f"{Fore.YELLOW}Enter your user ID: {Style.RESET_ALL}"))
            movie_id = int(input(f"{Fore.YELLOW}Enter the movie ID: {Style.RESET_ALL}"))
            score = int(input(f"{Fore.YELLOW}Enter your rating (1-10): {Style.RESET_ALL}"))
            rate_movie(session, user_id, movie_id, score)
        elif choice == '4':
            username = input(f"{Fore.YELLOW}Enter username: {Style.RESET_ALL}")
            age = int(input(f"{Fore.YELLOW}Enter age: {Style.RESET_ALL}"))
            create_user(session, username, age)
        elif choice == '5':
            user_id = int(input(f"{Fore.YELLOW}Enter user ID to delete: {Style.RESET_ALL}"))
            delete_user(session, user_id)
        elif choice == '6':
            user_id = int(input(f"{Fore.YELLOW}Enter user ID to update: {Style.RESET_ALL}"))
            new_username = input(f"{Fore.YELLOW}Enter new username: {Style.RESET_ALL}")
            new_age = int(input(f"{Fore.YELLOW}Enter new age: {Style.RESET_ALL}"))
            update_user(session, user_id, new_username, new_age)
        elif choice == '7':
            view_users(session)
        elif choice == '8':
            title = input(f"{Fore.YELLOW}Enter movie title: {Style.RESET_ALL}")
            director = input(f"{Fore.YELLOW}Enter movie director: {Style.RESET_ALL}")
            genre = input(f"{Fore.YELLOW}Enter movie genre: {Style.RESET_ALL}")
            release_year = int(input(f"{Fore.YELLOW}Enter movie release year: {Style.RESET_ALL}"))
            create_movie(session, title, director, genre, release_year)
        elif choice == '9':
            movie_id = int(input(f"{Fore.YELLOW}Enter movie ID to delete: {Style.RESET_ALL}"))
            delete_movie(session, movie_id)
        elif choice == '10':
            movie_id = int(input(f"{Fore.YELLOW}Enter movie ID to update: {Style.RESET_ALL}"))
            new_title = input(f"{Fore.YELLOW}Enter new title: {Style.RESET_ALL}")
            new_director = input(f"{Fore.YELLOW}Enter new director: {Style.RESET_ALL}")
            new_genre = input(f"{Fore.YELLOW}Enter new genre: {Style.RESET_ALL}")
            new_release_year = int(input(f"{Fore.YELLOW}Enter new release year: {Style.RESET_ALL}"))
            update_movie(session, movie_id, new_title, new_director, new_genre, new_release_year)
        elif choice == '11':
            num_movies = int(input(f"{Fore.YELLOW}Enter the number of top-rated movies to display: {Style.RESET_ALL}"))
            top_rated_movies(session, num_movies)

        elif choice == '12':
            print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

