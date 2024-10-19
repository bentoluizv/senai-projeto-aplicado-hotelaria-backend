from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import accommodations, amenities, bookings, guests

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    # TODO: Configurar origin para aceitar somente o endereço do frontend
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(bookings.router)
app.include_router(amenities.router)
app.include_router(accommodations.router)
app.include_router(guests.router)
