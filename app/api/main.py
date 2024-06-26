from fastapi import FastAPI

from .routers import accommodation, guests

app = FastAPI()

app.include_router(guests.router)
app.include_router(accommodation.router)
