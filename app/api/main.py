from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import accommodation, amenities, booking, guests

app = FastAPI()


const = origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://127.0.0.1:4321/',
    'http://127.0.0.1:8000/',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(guests.router)
app.include_router(accommodation.router)
app.include_router(booking.router)
app.include_router(amenities.router)
