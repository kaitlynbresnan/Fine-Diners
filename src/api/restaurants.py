from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
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
    average_price: int = Field(ge=0, le=100)
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
    average_price: int
    allergen_free_options: bool
    allows_animals: bool
    average_rating: Optional[float] = None
    food_quality_score: Optional[float] = None
    service_score: Optional[float] = None
    romantic_score: Optional[float] = None


class RestaurantSearchResponse(BaseModel):
    previous: Optional[str] = None
    next: Optional[str] = None
    results: List[RestaurantSearchResult]


class RestaurantAnalyticsResponse(BaseModel):
    restaurant_id: int
    restaurant_name: str
    review_count: int
    average_rating: Optional[float] = None
    average_food_quality_score: Optional[float] = None
    average_service_score: Optional[float] = None
    average_romantic_score: Optional[float] = None
    average_pricing_score: Optional[float] = None
    report_count: int
    owner_reply_count: int


@router.post("/", response_model=RestaurantResponse)
def add_restaurant(restaurant: RestaurantRequest):
    with db.engine.begin() as connection:
        existing = connection.execute(
            sqlalchemy.text(
                """
                SELECT restaurant_id
                FROM restaurants
                WHERE LOWER(name) = LOWER(:name)
                AND LOWER(location) = LOWER(:location)
                """
            ),
            {
                "name": restaurant.name,
                "location": restaurant.location,
            },
        ).mappings().first()

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Restaurant already exists",
            )

        row = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO restaurants (
                    name,
                    location,
                    cuisine,
                    average_price,
                    allergen_free_options,
                    allows_animals
                )
                VALUES (
                    :name,
                    :location,
                    :cuisine,
                    :average_price,
                    :allergen_free_options,
                    :allows_animals
                )
                RETURNING restaurant_id
                """
            ),
            {
                "name": restaurant.name,
                "location": restaurant.location,
                "cuisine": restaurant.cuisine,
                "average_price": restaurant.average_price,
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
    min_pricing: Optional[float] = None,
):
    query = """
        SELECT
            r.restaurant_id,
            r.name,
            r.location,
            r.cuisine,
            r.average_price,
            r.allergen_free_options,
            r.allows_animals,
            AVG(rv.rating) AS average_rating,
            AVG(rv.food_quality_score) AS food_quality_score,
            AVG(rv.service_score) AS service_score,
            AVG(rv.romantic_score) AS romantic_score,
            AVG(rv.pricing_score) AS pricing_score
        FROM restaurants r
        LEFT JOIN reviews rv ON r.restaurant_id = rv.restaurant_id
        WHERE (:restaurant_name = '' OR r.name ILIKE :restaurant_name_filter)
          AND (:cuisine = '' OR r.cuisine ILIKE :cuisine_filter)
          AND (:price_max IS NULL OR r.average_price <= :price_max)
          AND (:min_price IS NULL OR r.average_price >= :price_min)
          AND (:allergen_free IS NULL OR r.allergen_free_options = :allergen_free)
          AND (:allows_animals IS NULL OR r.allows_animals = :allows_animals)
        GROUP BY r.restaurant_id
        ORDER BY r.average_price ASC, average_rating DESC NULLS LAST
    """

    params = {
        "restaurant_name": restaurant_name,
        "restaurant_name_filter": f"%{restaurant_name}%",
        "cuisine": cuisine,
        "cuisine_filter": f"%{cuisine}%",
        "price_max": price_max,
        "allergen_free": allergen_free,
        "allows_animals": allows_animals,
        "min_pricing": min_pricing,
    }

    with db.engine.begin() as connection:
        rows = connection.execute(sqlalchemy.text(query), params).mappings().all()

    return RestaurantSearchResponse(
        results=[RestaurantSearchResult(**dict(row)) for row in rows],
    )


@router.get("/top/", response_model=RestaurantSearchResponse)
def get_top_restaurants(limit: int = Query(default=10, ge=1, le=10)):
    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    r.restaurant_id,
                    r.name,
                    r.location,
                    r.cuisine,
                    r.average_price,
                    r.allergen_free_options,
                    r.allows_animals,
                    AVG(rv.rating) AS average_rating,
                    AVG(rv.food_quality_score) AS food_quality_score,
                    AVG(rv.service_score) AS service_score,
                    AVG(rv.romantic_score) AS romantic_score,
                    AVG(rv.pricing_score) AS pricing_score
                FROM restaurants r
                JOIN reviews rv ON r.restaurant_id = rv.restaurant_id
                GROUP BY r.restaurant_id
                ORDER BY AVG(rv.rating) DESC, AVG(rv.food_quality_score) DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).mappings().all()

    return RestaurantSearchResponse(
        previous=None,
        next=None,
        results=[RestaurantSearchResult(**dict(row)) for row in rows],
    )


@router.get("/{restaurant_id}/analytics/", response_model=RestaurantAnalyticsResponse)
def get_restaurant_analytics(restaurant_id: int):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    r.restaurant_id,
                    r.name AS restaurant_name,
                    COUNT(DISTINCT rv.review_id) AS review_count,
                    AVG(rv.rating) AS average_rating,
                    AVG(rv.food_quality_score) AS average_food_quality_score,
                    AVG(rv.service_score) AS average_service_score,
                    AVG(rv.romantic_score) AS average_romantic_score,
                    AVG(rv.pricing_score) AS average_pricing_score,
                    COUNT(DISTINCT rr.report_id) AS report_count,
                    COUNT(DISTINCT oreply.reply_id) AS owner_reply_count
                FROM restaurants r
                LEFT JOIN reviews rv ON r.restaurant_id = rv.restaurant_id
                LEFT JOIN review_reports rr ON rv.review_id = rr.review_id
                LEFT JOIN owner_replies oreply ON rv.review_id = oreply.review_id
                WHERE r.restaurant_id = :restaurant_id
                GROUP BY r.restaurant_id, r.name
                """
            ),
            {"restaurant_id": restaurant_id},
        ).mappings().first()

        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

    return RestaurantAnalyticsResponse(**dict(row))