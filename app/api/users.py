from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.controller.UserController import UserController
from app.entities.schemas.Message import Message
from app.entities.User import User, UserCreateDTO

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[],
)

UserController = Annotated[UserController, Depends(UserController)]


class UserList(BaseModel):
    user: list[User]


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=User)
def find_by_id(user_controller: UserController, id: str):  # type: ignore
    user = user_controller.find_by_id(id)
    return user


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Message,
)
def create_new_user(
    data: UserCreateDTO,
    user_controller: UserController,  # type: ignore
):
    user_controller.create(data)
    return Message(message='CREATED')
