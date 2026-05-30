import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np

fake = Faker()
def database_connection_url():
    dotenv.load_dotenv("default.env")
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)
Num_restaurants = 40_000
Num_reviews = 760_000
Num_saved_restaurants = 100_000
Num_owner_replies = 50_000
Num_review_reports = 50_000

# create fake posters with fake names and birthdays
with engine.begin() as conn:

    print("Creating restaurants...")
    restaurants = []
    cuisines = ["American", "Korean","Mexican","Chinese","Japanese", "Indian", "Thai", "French","Mediterranean", "Italian", "Peruvian", "Vietnamese", "Vegan"]
    for i in range(Num_restaurants):
        restaurants.append({
            "name": fake.company() + " Restaurant",
            "location": fake.city(),
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
            "price_range": np.random.randint(1, 5),
            "allergen_free_options": np.random.choice([True, False], p=[0.30, 0.7]),
            "allows_animals": np.random.choice( [True, False], p=[0.25, 0.75])
        })
    conn.execute(
        sqlalchemy.text("""
            INSERT INTO restaurants
            (name, location, cuisine, price_range, allergen_free_options, allows_animals)
            VALUES
            (:name, :location, :cuisine, :price_range, :allergen_free_options, :allows_animals)
            """), restaurants)

    print("Creating reviews...")
    reviews = []
    for i in range(Num_reviews):
        reviews.append({
            "restaurant_id": np.random.randint(1, Num_restaurants + 1),
            "rating": np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.10, 0.20, 0.35, 0.30]),
            "description": fake.paragraph(),
            "food_quality_score": round(np.random.uniform(1, 5), 1),
            "service_score": round(np.random.uniform(1, 5), 1),
            "romantic_score": round(np.random.uniform(1, 5), 1),
            "pricing_score": round(np.random.uniform(1, 5), 1),
            "photos": None})
        if len(reviews) >= 10000:
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO reviews
                    (restaurant_id, rating, description, food_quality_score, service_score, romantic_score, pricing_score, photos)
                    VALUES
                    (:restaurant_id, :rating, :description, :food_quality_score, :service_score, :romantic_score, :pricing_score, :photos)
                    """),reviews)
            reviews.clear()
    if reviews:
        conn.execute(
            sqlalchemy.text("""
                INSERT INTO reviews
                (restaurant_id, rating, description, food_quality_score, service_score, romantic_score, pricing_score, photos)
                VALUES
                (:restaurant_id, :rating, :description, :food_quality_score, :service_score, :romantic_score, :pricing_score, :photos)
                """),reviews)


    print("Creating saved restaurants...")
    saved_restaurants = []
    for i in range(Num_saved_restaurants):
        saved_restaurants.append({
            "restaurant_id": np.random.randint(1, Num_restaurants + 1)})
        if len(saved_restaurants) >= 10000:
            conn.execute(
                sqlalchemy.text("""
                        INSERT INTO saved_restaurants
                        (restaurant_id)
                        VALUES
                        (:restaurant_id)
                    """),saved_restaurants)
            saved_restaurants.clear()
    if saved_restaurants:
        conn.execute(
            sqlalchemy.text("""
                    INSERT INTO saved_restaurants
                    (restaurant_id)
                    VALUES
                    (:restaurant_id)
                """),saved_restaurants)


    print("Creating owner replies...")
    owner_replies = []
    for i in range(Num_owner_replies):
        owner_replies.append({
            "review_id": np.random.randint(1, Num_reviews + 1),
            "reply": fake.paragraph()
        })
        if len(owner_replies) >= 10000:
            conn.execute(
                sqlalchemy.text("""
                        INSERT INTO owner_replies
                        (review_id, reply)
                        VALUES
                        (:review_id, :reply)
                    """),
                owner_replies)
            owner_replies.clear()
    if owner_replies:
        conn.execute(
            sqlalchemy.text("""
                    INSERT INTO owner_replies
                    (review_id, reply)
                    VALUES
                    (:review_id, :reply)
                """),
            owner_replies)


    print("Creating review reports...")
    review_reports = []
    for i in range(Num_review_reports):
        review_reports.append({
            "review_id": np.random.randint(1, Num_reviews + 1),
            "reason": fake.sentence()})
        if len(review_reports) >= 10000:
            conn.execute(
                sqlalchemy.text("""
                        INSERT INTO review_reports
                        (review_id, reason)
                        VALUES
                        (:review_id, :reason)
                    """),review_reports)
            review_reports.clear()
    if review_reports:
        conn.execute(
            sqlalchemy.text("""
                    INSERT INTO review_reports
                    (review_id, reason)
                    VALUES
                    (:review_id, :reason)
                """), review_reports)

    print("Total restaurants:", Num_restaurants)
    print("Total reviews:", Num_reviews)
    print("Total saved restaurants:", Num_saved_restaurants)
    print("Total owner replies:", Num_owner_replies)
    print("Total review reports:", Num_review_reports)
    print("Total rows:", Num_restaurants + Num_reviews + Num_saved_restaurants + Num_owner_replies + Num_review_reports)