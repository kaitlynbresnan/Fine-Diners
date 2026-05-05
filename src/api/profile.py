from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


class SuccessResponse(BaseModel):
    success: bool


@router.post("/restaurants/{restaurant_id}/", response_model=SuccessResponse)
def save_restaurant(restaurant_id: int):
    user_id = "test_user"

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO saved_restaurants (user_id, restaurant_id)
                VALUES (:user_id, :restaurant_id)
                """
            ),
            {
                "user_id": user_id,
                "restaurant_id": restaurant_id,
            },
        )

    return SuccessResponse(success=True)


@router.delete("/restaurants/{restaurant_id}/", response_model=SuccessResponse)
def delete_saved_restaurant(restaurant_id: int):
    user_id = "test_user"

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM saved_restaurants
                WHERE user_id = :user_id
                AND restaurant_id = :restaurant_id
                """
            ),
            {
                "user_id": user_id,
                "restaurant_id": restaurant_id,
            },
        )

    return SuccessResponse(success=True)


@router.get("/")
def get_profile():
    user_id = "test_user"

    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT r.restaurant_id, r.name, r.location, r.cuisine
                FROM saved_restaurants sr
                JOIN restaurants r ON sr.restaurant_id = r.restaurant_id
                WHERE sr.user_id = :user_id
                """
            ),
            {"user_id": user_id},
        ).mappings().all()

    return {
        "user_id": user_id,
        "saved_restaurants": [dict(row) for row in rows],
    }