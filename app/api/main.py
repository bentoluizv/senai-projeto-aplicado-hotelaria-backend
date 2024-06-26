from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import accommodation, booking, guests

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(guests.router)
app.include_router(accommodation.router)
app.include_router(booking.router)
