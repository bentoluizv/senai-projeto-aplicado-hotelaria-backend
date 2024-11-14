from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .api import accommodations, amenities, bookings, guests, users

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:4321', 'http://127.0.0.1:4321', '*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.middleware('http')
async def log_request(request: Request, call_next):
    print(f'Request headers: {request.headers}')
    response = await call_next(request)
    return response


app.include_router(bookings.router)
app.include_router(amenities.router)
app.include_router(accommodations.router)
app.include_router(guests.router)
app.include_router(users.router)
