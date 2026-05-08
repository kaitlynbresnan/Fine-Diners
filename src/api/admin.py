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
        connection.execute(sqlalchemy.text("DELETE FROM review_reports"))
        connection.execute(sqlalchemy.text("DELETE FROM owner_replies"))
        connection.execute(sqlalchemy.text("DELETE FROM saved_restaurants"))
        connection.execute(sqlalchemy.text("DELETE FROM restaurants"))
        connection.execute(sqlalchemy.text("DELETE FROM reviews"))
    return None