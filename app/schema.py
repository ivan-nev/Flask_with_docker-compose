from pydantic import BaseModel, validator
from pydantic import ValidationError
from errors import HttpError
import re

password_regex = re.compile('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{6,20})')
title_regex = re.compile('^.{5,20}')


class CreateUser(BaseModel):
    username: str
    password: str

    @validator('password')
    def validate_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValueError('password to simple')
        return value


def validate_create_user(json_data):
    try:
        user_schema = CreateUser(**json_data)
        return user_schema.dict()
    except ValidationError as er:
        print(er.errors())
        raise HttpError(status_code=400, message=er.errors())

class CreateAdvertisement(BaseModel):
    title: str
    description: str
    id_user: int

    @validator('title')
    def validate_title(cls, value: str):
        if len(value) > 20 or len(value) <5:
            raise ValueError('5 < Title < 20')
        return value

def validate_create_advertisement(json_data):
    try:
        adv_schema = CreateAdvertisement(**json_data)
        return adv_schema.dict()
    except ValidationError as er:
        print(er.errors())
        raise HttpError(status_code=400, message=er.errors())




#Пример проверки
# print(validate_create_user({'username':'1', 'passwor': 'sdf'}))
# print(validate_create_advertisement({'title':'1236', 'description': 'sdf', 'id_user':1}))