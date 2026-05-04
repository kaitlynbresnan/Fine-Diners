from fastapi import FastAPI
from src.api import admin, reviews
from starlette.middleware.cors import CORSMiddleware

description = """
Fine Diners is a site for restaurant reviewing.
"""
tags_metadata = [
    {"name": "reviews", "description": "Leave a review."},
    {"name": "admin", "description": "Where you reset the game state."},
]

app = FastAPI(
    title="Fine Diners",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Kaitlyn Bresnan",
        "email": "kbresnan@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)

origins = ["https://fine-diners.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(reviews.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "Website is up!"}
