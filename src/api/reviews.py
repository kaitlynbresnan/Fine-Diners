from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


class ReviewRequest(BaseModel):
    restaurant_id: Optional[int] = None
    rating: Optional[int] = Field(default=None, ge=0, le=5)
    description: str = Field(min_length=5, max_length=1000)
    food_quality_score: Optional[int] = Field(default=None, ge=0, le=5)
    service_score: Optional[int] = Field(default=None, ge=0, le=5)
    romantic_score: Optional[int] = Field(default=None, ge=0, le=5)
    pricing_score: Optional[int] = Field(default=None, ge=0, le=5)
    photos: List[str] = Field(default_factory=list, max_length=5)


class ReviewResponse(BaseModel):
    success: bool
    review_id: int


class SuccessResponse(BaseModel):
    success: bool


@router.post("/{review_id}", response_model=ReviewResponse)
def write_review(review_id: int, review: ReviewRequest):
    if review.rating is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating is required",
        )

    if review.rating < 0 or review.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 0 and 5",
        )

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                                """
                INSERT INTO reviews (
                    review_id,
                    restaurant_id,
                    rating,
                    description,
                    food_quality_score,
                    service_score,
                    romantic_score,
                    pricing_score,
                    photos
                )
                VALUES (
                    :review_id,
                    :restaurant_id,
                    :rating,
                    :description,
                    :food_quality_score,
                    :service_score,
                    :romantic_score,
                    :pricing_score,
                    :photos
                )
                """
            ),
            {
                "review_id": review_id,
                "restaurant_id": review.restaurant_id,
                "rating": review.rating,
                "description": review.description,
                "food_quality_score": review.food_quality_score,
                "service_score": review.service_score,
                "romantic_score": review.romantic_score,
                "pricing_score": review.pricing_score,
                "photos": ",".join(review.photos),
            },
        )

    return ReviewResponse(success=True, review_id=review_id)


@router.put("/{review_id}", response_model=SuccessResponse)
def edit_review(review_id: int, review: ReviewRequest):
    if review.rating is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating is required",
        )

    if review.rating < 0 or review.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 0 and 5",
        )

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                UPDATE reviews
                SET
                    restaurant_id = :restaurant_id,
                    rating = :rating,
                    description = :description,
                    food_quality_score = :food_quality_score,
                    service_score = :service_score,
                    romantic_score = :romantic_score,
                    pricing_score = :pricing_score,
                    photos = :photos,
                    updated_at = CURRENT_TIMESTAMP
                WHERE review_id = :review_id
                """
            ),
            {
                "review_id": review_id,
                "restaurant_id": review.restaurant_id,
                "rating": review.rating,
                "description": review.description,
                "food_quality_score": review.food_quality_score,
                "service_score": review.service_score,
                "romantic_score": review.romantic_score,
                "pricing_score": review.pricing_score,
                "photos": ",".join(review.photos),
            },
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

    return SuccessResponse(success=True)


@router.delete("/{review_id}", response_model=SuccessResponse)
def delete_review(review_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM reviews
                WHERE review_id = :review_id
                """
            ),
            {"review_id": review_id},
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

    return SuccessResponse(success=True)

class ReviewSearchResult(BaseModel):
    review_id: int
    restaurant_id: Optional[int] = None
    review_name: str
    user_name: str
    timestamp: str


class ReviewSearchResponse(BaseModel):
    previous: Optional[str] = None
    next: Optional[str] = None
    results: List[ReviewSearchResult]


@router.get("/search/", response_model=ReviewSearchResponse)
def search_reviews(
    user_name: str = "",
    restaurant_name: str = "",
    search_page: int = 1,
    page_size: int = 10,
):
    offset = (search_page - 1) * page_size

    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    rv.review_id,
                    rv.restaurant_id,
                    rv.description AS review_name,
                    'test_user' AS user_name,
                    rv.created_at::text AS timestamp
                FROM reviews rv
                LEFT JOIN restaurants r ON rv.restaurant_id = r.restaurant_id
                WHERE (:restaurant_name = '' OR r.name ILIKE :restaurant_name_filter)
                  AND (:user_name = '' OR 'test_user' ILIKE :user_name_filter)
                ORDER BY rv.created_at DESC
                LIMIT :page_size OFFSET :offset
                """
            ),
            {
                "restaurant_name": restaurant_name,
                "restaurant_name_filter": f"%{restaurant_name}%",
                "user_name": user_name,
                "user_name_filter": f"%{user_name}%",
                "page_size": page_size,
                "offset": offset,
            },
        ).mappings().all()

    return ReviewSearchResponse(
        previous=f"/reviews/search/?search_page={search_page - 1}" if search_page > 1 else None,
        next=f"/reviews/search/?search_page={search_page + 1}" if len(rows) == page_size else None,
        results=[ReviewSearchResult(**dict(row)) for row in rows],
    )


@router.get("/{review_id}")
def get_review(review_id: int):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM reviews
                WHERE review_id = :review_id
                """
            ),
            {"review_id": review_id},
        ).mappings().first()

        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

    return dict(row)

class ReplyRequest(BaseModel):
    user_id: str
    reply: str


class ReplyResponse(BaseModel):
    reply_id: int
    success: bool


class ReportRequest(BaseModel):
    user_id: str
    reason: str


class ReportResponse(BaseModel):
    report_id: int
    success: bool


@router.post("/{review_id}/reply", response_model=ReplyResponse)
def reply_to_review(review_id: int, reply_request: ReplyRequest):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO owner_replies (review_id, user_id, reply)
                VALUES (:review_id, :user_id, :reply)
                RETURNING reply_id
                """
            ),
            {
                "review_id": review_id,
                "user_id": reply_request.user_id,
                "reply": reply_request.reply,
            },
        ).one()

    return ReplyResponse(reply_id=row.reply_id, success=True)


@router.post("/{review_id}/report", response_model=ReportResponse)
def report_review(review_id: int, report_request: ReportRequest):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO review_reports (review_id, user_id, reason)
                VALUES (:review_id, :user_id, :reason)
                RETURNING report_id
                """
            ),
            {
                "review_id": review_id,
                "user_id": report_request.user_id,
                "reason": report_request.reason,
            },
        ).one()

    return ReportResponse(report_id=row.report_id, success=True)