from fastapi import APIRouter, Depends, status
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.post("/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset():
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
            TRUNCATE TABLE 
                review_reports, 
                owner_replies, 
                saved_restaurants, 
                reviews, 
                restaurants 
            CASCADE;
        """))
    return None