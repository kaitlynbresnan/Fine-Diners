from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


class SuccessResponse(BaseModel):
    success: bool


class SavedRestaurant(BaseModel):
    restaurant_id: int
    name: str
    location: str
    cuisine: str


class ProfileResponse(BaseModel):
    user_id: str
    saved_restaurants: List[SavedRestaurant]


@router.post("/restaurants/{restaurant_id}/", response_model=SuccessResponse)
def save_restaurant(
    restaurant_id: int,
    user_id: str = Query(default="test_user"),
):
    with db.engine.begin() as connection:
        restaurant = connection.execute(
            sqlalchemy.text(
                """
                SELECT restaurant_id
                FROM restaurants
                WHERE restaurant_id = :restaurant_id
                """
            ),
            {"restaurant_id": restaurant_id},
        ).mappings().first()

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

        existing = connection.execute(
            sqlalchemy.text(
                """
                SELECT saved_restaurant_id
                FROM saved_restaurants
                WHERE user_id = :user_id
                AND restaurant_id = :restaurant_id
                """
            ),
            {
                "user_id": user_id,
                "restaurant_id": restaurant_id,
            },
        ).mappings().first()

        if existing is None:
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
def delete_saved_restaurant(
    restaurant_id: int,
    user_id: str = Query(default="test_user"),
):
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


@router.get("/", response_model=ProfileResponse)
def get_profile(user_id: str = Query(default="test_user")):
    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT r.restaurant_id, r.name, r.location, r.cuisine
                FROM saved_restaurants sr
                JOIN restaurants r ON sr.restaurant_id = r.restaurant_id
                WHERE sr.user_id = :user_id
                ORDER BY sr.saved_at DESC
                """
            ),
            {"user_id": user_id},
        ).mappings().all()

    return ProfileResponse(
        user_id=user_id,
        saved_restaurants=[SavedRestaurant(**dict(row)) for row in rows],
    )