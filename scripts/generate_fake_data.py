import random
from faker import Faker
import sqlalchemy
import os

os.environ["API_KEY"] = "brat"
os.environ["POSTGRES_URI"] = "postgresql+psycopg://myuser:mypassword@localhost:5432/mydatabase"
from src import database as db


fake = Faker()

NUM_RESTAURANTS = 10000
NUM_REVIEWS = 900000
NUM_REPORTS = 50000
NUM_REPLIES = 20000
NUM_SAVED = 20000

cuisines = ["Thai", "Italian", "Mexican", "Japanese", "American", "Indian", "Chinese"]


def main():
    with db.engine.begin() as conn:
        print("Clearing old data...")
        conn.execute(sqlalchemy.text("DELETE FROM review_reports"))
        conn.execute(sqlalchemy.text("DELETE FROM owner_replies"))
        conn.execute(sqlalchemy.text("DELETE FROM saved_restaurants"))
        conn.execute(sqlalchemy.text("DELETE FROM reviews"))
        conn.execute(sqlalchemy.text("DELETE FROM restaurants"))

        print("Adding restaurants...")
        restaurants = []
        for i in range(1, NUM_RESTAURANTS + 1):
            restaurants.append({
                "restaurant_id": i,
                "name": f"{fake.company()} Restaurant {i}",
                "location": fake.city(),
                "cuisine": random.choice(cuisines),
                "price_range": random.randint(1, 5),
                "allergen_free_options": random.choice([True, False]),
                "allows_animals": random.choice([True, False]),
            })

        conn.execute(sqlalchemy.text("""
            INSERT INTO restaurants (
                restaurant_id, name, location, cuisine, price_range,
                allergen_free_options, allows_animals
            )
            VALUES (
                :restaurant_id, :name, :location, :cuisine, :price_range,
                :allergen_free_options, :allows_animals
            )
        """), restaurants)

        print("Adding reviews...")
        batch = []
        for i in range(1, NUM_REVIEWS + 1):
            batch.append({
                "review_id": i,
                "restaurant_id": random.randint(1, NUM_RESTAURANTS),
                "rating": random.randint(1, 5),
                "description": fake.sentence(),
                "food_quality_score": random.randint(1, 5),
                "service_score": random.randint(1, 5),
                "romantic_score": random.randint(1, 5),
                "pricing_score": random.randint(1, 5),
                "photos": "",
            })

            if len(batch) == 5000:
                conn.execute(sqlalchemy.text("""
                    INSERT INTO reviews (
                        review_id, restaurant_id, rating, description,
                        food_quality_score, service_score, romantic_score,
                        pricing_score, photos
                    )
                    VALUES (
                        :review_id, :restaurant_id, :rating, :description,
                        :food_quality_score, :service_score, :romantic_score,
                        :pricing_score, :photos
                    )
                """), batch)
                batch = []
                print(f"Inserted {i} reviews")

        if batch:
            conn.execute(sqlalchemy.text("""
                INSERT INTO reviews (
                    review_id, restaurant_id, rating, description,
                    food_quality_score, service_score, romantic_score,
                    pricing_score, photos
                )
                VALUES (
                    :review_id, :restaurant_id, :rating, :description,
                    :food_quality_score, :service_score, :romantic_score,
                    :pricing_score, :photos
                )
            """), batch)

        print("Adding reports...")
        reports = []
        for i in range(1, NUM_REPORTS + 1):
            reports.append({
                "report_id": i,
                "review_id": random.randint(1, NUM_REVIEWS),
                "user_id": f"user_{random.randint(1, 50000)}",
                "reason": random.choice(["Inappropriate language", "Biased review", "Spam"]),
            })

        conn.execute(sqlalchemy.text("""
            INSERT INTO review_reports (report_id, review_id, user_id, reason)
            VALUES (:report_id, :review_id, :user_id, :reason)
        """), reports)
        print("Adding owner replies...")
        replies = []
        for i in range(1, NUM_REPLIES + 1):
            replies.append({
                "reply_id": i,
                "review_id": random.randint(1, NUM_REVIEWS),
                "user_id": f"owner_{random.randint(1, NUM_RESTAURANTS)}",
                "reply": fake.sentence(),
            })

        conn.execute(sqlalchemy.text("""
            INSERT INTO owner_replies (reply_id, review_id, user_id, reply)
            VALUES (:reply_id, :review_id, :user_id, :reply)
        """), replies)

        print("Adding saved restaurants...")
        saved = []
        for i in range(1, NUM_SAVED + 1):
            saved.append({
                "saved_restaurant_id": i,
                "user_id": f"user_{random.randint(1, 50000)}",
                "restaurant_id": random.randint(1, NUM_RESTAURANTS),
            })

        conn.execute(sqlalchemy.text("""
            INSERT INTO saved_restaurants (saved_restaurant_id, user_id, restaurant_id)
            VALUES (:saved_restaurant_id, :user_id, :restaurant_id)
        """), saved)

        print("Done.")


if __name__ == "__main__":
    main()