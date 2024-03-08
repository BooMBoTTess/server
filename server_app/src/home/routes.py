from __future__ import annotations

from typing import Union

from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import select
from starlette import status
from starlette.responses import RedirectResponse

from server_app.database.database import get_async_session
from server_app.src.utils import current_active_user, templates
from sqlalchemy.ext.asyncio import AsyncSession
from server_app.src.auth.model import User, post, department

router = APIRouter(
    prefix='/home',
    tags=['home'],
    dependencies=[Depends(current_active_user)]
)


@router.get('/')
async def home_page(request: Request, user: User = Depends(current_active_user),
                    session: AsyncSession = Depends(get_async_session)):
    """Открывает home.html в нем можно открыть дашборд для руководства и замруков
    Если user.post == рук, замрук, извращенцы рисуем ему кнопку с дашбордом.
    руководителя - дашборд руководителя.
    Замрук - дашборд замрука
    1. Загрузить данные департаментов
    2. Проверить доступен пользователю дашборд
    """
    is_dash_available = False
    if user.fk_post_id == 0 or user.fk_post_id == 1:
        is_dash_available = True

    querry = select(department.id, department.name)
    departments = await session.execute(querry)
    departments = departments.all()
    departments_dict = {}

    querry = select(User.username, User.fk_department_id).where(User.fk_post_id == 3)
    heads = await session.execute(querry)
    heads = heads.all()
    heads_dict = {}

    for item in departments:
        departments_dict[item[0]] = [item[1]]
    for item in heads:
        heads_dict[item[1]] = item[0]
    for key, value in heads_dict.items():
        departments_dict[key].append(value)

    departments_dict.pop(0)
    departments_dict.pop(1)
    user_info = {'ФИО': user.username, 'Отдел': departments[user.fk_department_id][1]}

    return templates.TemplateResponse("home.html", {'request': request, 'is_dash_available': is_dash_available,
                                                    'departments': departments_dict, 'user_info': user_info})


@router.get('/{dep}')
async def dep_page(dep: Union[str, int], request: Request, user: User = Depends(current_active_user),
                   session: AsyncSession = Depends(get_async_session)):
    """Открывает окно определенного департамента.
        user.post == НО, user.dep == тот же департамент.
        Дашборд начальника отдела
        :type dep: object
    """
    if dep == 'my_dep':
        return RedirectResponse(f'/home/{user.fk_department_id}')
    else:
        # Не допускаем человека при этих условиях
        if (user.fk_department_id != int(dep)) and (not user.is_superuser):
            return status.HTTP_403_FORBIDDEN
        else:
            # Загрузить данные по департаменту
            query = ((select(User.username, department.name, post.name)
                      .join(department).filter(User.fk_department_id == department.id)
                      .join(post).filter(User.fk_post_id == post.id))
                     .where(department.id == int(dep))
                     .order_by(department.id).order_by(post.id))

            result = await session.execute(query)
            result = result.all()

            is_dash_available = False
            if user.fk_post_id == 3:
                is_dash_available = True
            if len(result) == 0:
                dep = 'Отсутствуют сотрудники'
            else:
                dep = result[0][1]

            return templates.TemplateResponse("department.html",
                                              {'request': request, 'is_dash_available': is_dash_available,
                                               'workers': result, 'department': dep})

@router.post('/dep')
async def fire_worker(worker_id = Form()):
    """Уволить сотрудника при нажатии на кнопку"""

    pass

@router.get('/{dep}/{worker}')
async def worker_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    """Открывает окно с инфой о человеке"""
    pass
