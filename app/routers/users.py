from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import User
from sqlalchemy import insert, select
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/registration")
async def registration(request: Request):
    context = {'request': request}
    return templates.TemplateResponse(name='personality/registration.html', context=context)


@router.post("/registration_info")
async def registration_info(request: Request, db: Annotated[Session, Depends(get_db)],
                            username: str = Form(),
                            password: str = Form(),
                            repeat_password: str = Form(),
                            email: str = Form(),
                            phone: str = Form(default="Не указан"),
                            birthday: str = Form(default="Не указан")):
    """
    function that is triggered
    when the "confirm" button is clicked on a registration page
    and verifies the data entered by the user
    :param username, password, repeat_password, email, phone, birthday:
    info about user from the page
    :return: page template and message about the result of data verification
    """
    context = {'request': request}
    user_find = db.scalar(select(User).where(User.username == username))
    if len(username) > 20 or len(password) < 8 or len(phone) > 12 or len(birthday) > 10:
        context['message'] = 'Неверный формат данных!'
        return templates.TemplateResponse(name='personality/registration.html', context=context)
    if user_find:
        context['message'] = 'Такой пользователь уже существует!'
        return templates.TemplateResponse(name='personality/registration.html', context=context)
    if password != repeat_password:
        context['message'] = 'Пароли не совпадают!'
        return templates.TemplateResponse(name='personality/registration.html', context=context)

    db.execute(insert(User).values(username=username,
                                   password=password,
                                   email=email,
                                   phone=phone,
                                   birthday=birthday))
    db.commit()
    context['message'] = 'Вы успешно зарегистрированы!'
    return templates.TemplateResponse(name='personality/registration.html', context=context)


@router.get("/login")
async def login(request: Request):
    context = {'request': request}
    return templates.TemplateResponse(name='personality/login.html', context=context)


@router.post("/login_info")
async def login_info(request: Request, db: Annotated[Session, Depends(get_db)],
                     username: str = Form(),
                     password: str = Form()):
    """
    function that is triggered
    when the "confirm" button is clicked on a login page
    and verifies the data entered by the user
    :param username, password: info about user from the page
    :return: page template and message about the result of data verification
    """
    context = {'request': request}
    user_find = db.scalar(select(User).where(User.username == username))
    if not user_find:
        context['message'] = 'Такой пользователь не зарегистрирован!'
        return templates.TemplateResponse(name='personality/login.html', context=context)
    if password != user_find.password:
        context['message'] = 'Пароли не совпадают!'
        return templates.TemplateResponse(name='personality/login.html', context=context)

    context.update({
        'username': user_find.username,
        'email': user_find.email,
        'phone': user_find.phone,
        'birthday': user_find.birthday
    })
    return templates.TemplateResponse(name='personality/profil.html', context=context)
