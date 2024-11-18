from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth

from .api import accommodations, amenities, bookings, guests, users

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(bookings.router)
app.include_router(amenities.router)
app.include_router(accommodations.router)
app.include_router(guests.router)
app.include_router(users.router)
app.include_router(auth.router)
