import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np

fake = Faker()
def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)
Num_users = 200_000
Num_restaurants = 40_000
Num_reviews = 760_000

# create fake posters with fake names and birthdays
with engine.begin() as conn:
    print("Creating users...")
    users = []
    for i in range(Num_users):
        users.append({
            "username": fake.user_name() + str(i),
            "email": fake.unique.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name()})

    conn.execute(
        sqlalchemy.text("""
            INSERT INTO users
            (username, email, first_name, last_name)
            VALUES
            (:username, :email, :first_name, :last_name)
            """),users)

    print("Creating restaurants...")
    restaurants = []
    cuisines = ["American", "Korean","Mexican","Chinese","Japanese", "Indian", "Thai", "French","Mediterranean", "Italian", "Peruvian", "Vietnamese", "Vegan"]
    for i in range(Num_restaurants):
        restaurants.append({
            "name": fake.company() + " Restaurant",
            "city": fake.city(),
            "cuisine": np.random.choice(cuisines,p=[
            0.20,  # American
            0.07,  # Korean
            0.15,  # Mexican
            0.09,  # Chinese
            0.08,  # Japanese
            0.08,  # Indian
            0.06,  # Thai
            0.03,  # French
            0.05,  # Mediterranean
            0.16,  # Italian
            0.03,  # Peruvian
            0.07,  # Vietnamese
            0.01  # Vegan
            ]),
            "price": np.random.choice(["$", "$$", "$$$", "$$$$"],p=[0.30, 0.40, 0.20, 0.1]),
            "animal_friendly": np.random.choice( [True, False], p=[0.25, 0.75])
        })

    conn.execute(
        sqlalchemy.text("""
            INSERT INTO restaurants
            (name, city, cuisine, price, animal_friendly)
            VALUES
            (:name, :city, :cuisine, :price, :animal_friendly)
            """), restaurants)
    print("Creating reviews...")
    reviews = []
    for i in range(Num_reviews):
        reviews.append({
            "user_id": np.random.randint(1, Num_users + 1),
            "restaurant_id": np.random.randint(1,Num_restaurants + 1),
            "rating": np.random.choice([1, 2, 3, 4, 5],p=[0.05, 0.10, 0.20, 0.35, 0.30]),
            "comment": fake.paragraph()})
        if len(reviews) >= 10000:
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO reviews
                    (user_id, restaurant_id, rating, comment)
                    VALUES
                    (:user_id, :restaurant_id, :rating, :comment)
                    """),reviews)
            reviews.clear()

    if reviews:
        conn.execute(
            sqlalchemy.text("""
                INSERT INTO reviews
                (user_id, restaurant_id, rating, comment)
                VALUES
                (:user_id, :restaurant_id, :rating, :comment)
                """),reviews)

    print("Total reviews:", Num_reviews)
    print("Total rows:", Num_users + Num_restaurants + Num_reviews)