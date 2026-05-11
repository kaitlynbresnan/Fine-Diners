from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
)


class RestaurantRequest(BaseModel):
    name: str
    location: str
    cuisine: str
    price_range: int
    allergen_free_options: bool
    allows_animals: bool


class RestaurantResponse(BaseModel):
    success: bool
    restaurant_id: int


class RestaurantSearchResult(BaseModel):
    restaurant_id: int
    name: str
    location: str
    cuisine: str
    price_range: int
    allergen_free_options: bool
    allows_animals: bool


class RestaurantSearchResponse(BaseModel):
    previous: Optional[str] = None
    next: Optional[str] = None
    results: List[RestaurantSearchResult]


@router.post("/", response_model=RestaurantResponse)
def add_restaurant(restaurant: RestaurantRequest):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO restaurants (
                    name,
                    location,
                    cuisine,
                    price_range,
                    allergen_free_options,
                    allows_animals,
                )
                VALUES (
                    :name,
                    :location,
                    :cuisine,
                    :price_range,
                    :allergen_free_options,
                    :allows_animals,
                )
                RETURNING restaurant_id
                """
            ),
            {
                "name": restaurant.name,
                "location": restaurant.location,
                "cuisine": restaurant.cuisine,
                "price_range": restaurant.price_range,
                "allergen_free_options": restaurant.allergen_free_options,
                "allows_animals": restaurant.allows_animals,
            },
        ).one()

    return RestaurantResponse(success=True, restaurant_id=row.restaurant_id)


@router.get("/search/", response_model=RestaurantSearchResponse)
def search_restaurants(
    restaurant_name: str = "",
    cuisine: str = "",
    price_max: Optional[int] = None,
    allergen_free: Optional[bool] = None,
    allows_animals: Optional[bool] = None,
):
    query = """
        SELECT restaurant_id, name, location, cuisine, price_range,
               allergen_free_options, allows_animals
        FROM restaurants
        WHERE (:restaurant_name = '' OR name ILIKE :restaurant_name_filter)
          AND (:cuisine = '' OR cuisine ILIKE :cuisine_filter)
          AND (:price_max::int IS NULL OR price_range <= :price_max::int)
          AND (:allergen_free::boolean IS NULL OR allergen_free_options = :allergen_free::boolean)
          AND (:allows_animals::boolean IS NULL OR allows_animals = :allows_animals::boolean)
        ORDER BY price_range ASC
    """

    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(query),
            {
                "restaurant_name": restaurant_name,
                "restaurant_name_filter": f"%{restaurant_name}%",
                "cuisine": cuisine,
                "cuisine_filter": f"%{cuisine}%",
                "price_max": price_max,
                "allergen_free": allergen_free,
                "allows_animals": allows_animals,
            },
        ).mappings().all()

    return RestaurantSearchResponse(
        previous=None,
        next=None,
        results=[RestaurantSearchResult(**dict(row)) for row in rows],
    )