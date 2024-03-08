from typing import Annotated, Optional
import typing

from fastapi import APIRouter, Depends, Request, Form
from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy.exc import IntegrityError
from starlette.responses import RedirectResponse
from sqlalchemy.orm import sessionmaker, Session
from server_app.database.database import engine, get_async_session
from server_app.database.database import AsyncSession
from sqlalchemy import select, insert, update

from server_app.database import user_manager
from server_app.database.user_manager import auth_backend, UserManager, get_user_manager, get_jwt_strategy
from server_app.src.auth.model import User, department, post
from server_app.src.auth.schemas import UserCreate, LoginRequest
from server_app.database.user_manager import fastapi_users
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status

from server_app.src.utils import templates, current_active_verified_user, current_active_user

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


#TODO: Страничка с изменение логина и пароля



@router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse("login.html", {'request': request})

@router.post("/login")                                  #логика авторизации
async def login(
    login_data: LoginRequest,
    user_manager: UserManager = Depends(get_user_manager),
):
    user = await user_manager.authenticate(
        OAuth2PasswordRequestForm(username=login_data.email, password=login_data.password)
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials",
        )
    res = await auth_backend.login(get_jwt_strategy(), user)
    return res

@router.get('/registration')
async def registration_page(request: Request,
                            user: User = Depends(current_active_user),
                            session: AsyncSession = Depends(get_async_session)):
    department_name = await session.execute(select(department.name).filter(department.id == user.fk_department_id))
    department_name = department_name.scalar()
    post_name = await session.execute(select(post.name).filter(post.id == user.fk_post_id))
    post_name = post_name.scalar()

    return templates.TemplateResponse("registration.html",
                                      {'request': request,
                                       'registered_flag': False,
                                       'user': user,
                                       'department_name': department_name,
                                       'post_name': post_name})

@router.post('/registration')
async def registration_page(request: Request, password = Form(), email = Form(),
                      user_manager: UserManager = Depends(get_user_manager)
                      ):
    user_data = User(hashed_password=password, email=email)


    return templates.TemplateResponse("registration.html", {'request': request, 'registered_flag': True})
