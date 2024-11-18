from datetime import datetime, timedelta

from jwt import encode
from zoneinfo import ZoneInfo

from app.settings.Settings import Settings

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode,
        Settings().SECRET_KEY,  # type: ignore
        algorithm=Settings().ALGORITHM,  # type: ignore
    )
    return encoded_jwt
