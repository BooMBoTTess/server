from fastapi import APIRouter, Depends, Request
from sqlalchemy import select, insert, update
from starlette import status
from starlette.responses import JSONResponse
from pydantic import BaseModel

from server_app.database import user_manager
from server_app.database.database import get_async_session
from server_app.database.user_manager import auth_backend, UserManager, get_user_manager
from server_app.src.auth.schemas import UserRead, UserCreate
from server_app.database.user_manager import fastapi_users
from server_app.src.utils import current_active_user, templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from server_app.src.staff.schemas import UserChange, Staff, Department, Post
from server_app.src.auth.model import User, post, department, staff_positions, zamruk

router = APIRouter(
    prefix='/staff',
    tags=['staff'],
    # dependencies=[Depends(current_active_user)]
)


@router.post('/', response_model=UserRead)
async def change_staff(user_change: UserChange, session: AsyncSession = Depends(get_async_session),
                       user_manager: UserManager = Depends(get_user_manager)):
    """
    Обновляет информацию о пользователе в зависимости от указанного действия.

    :param user_change: Данные для обновления пользователя.
        - action: 1 для изменения должности и департамента, 2 для деактивации пользователя, 3 для создания пользователя.
        - user_name: Имя пользователя для обновления.
        - post_id: Новый идентификатор должности для пользователя (для действия 1/3).
        - department_id: Новый идентификатор департамента для пользователя (для действия 1/3).
        - is_active: Новое значение для is_active (для действия 2).
    :param session: AsyncSession
    :return: Обновленная информация о пользователе.
    """
    print('Bзмененный пользователь', user_change)
    action = user_change.action
    if action is None or (action != 1 and action != 2 and action != 3):
        raise HTTPException(status_code=400, detail="Invalid action")

    user = await session.execute(select(User).filter(User.username == user_change.user_name))
    user = user.scalar()

    if user is None:
        if action == 3:
            user_data = {'email': 'allipupi@murmur.ru', 'hashed_password': '1234', 'username': user_change.user_name,
                         'fk_department_id': user_change.department_id, 'fk_post_id': user_change.post_id
                         }
            res = await UserManager.create(
                user_manager,
                user_create=UserCreate(email=user_data['email'], password=user_data['hashed_password'],
                                       username=user_data['username'], fk_department_id=user_data['fk_department_id'],
                                       fk_post_id=user_data['fk_post_id']),
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")

    if action == 1:
        post_e = await session.get(post, user_change.post_id)
        if post_e is None:
            raise HTTPException(status_code=404, detail="Post not found")

        department_e = await session.get(department, user_change.department_id)
        if department_e is None:
            raise HTTPException(status_code=404, detail="Department not found")

        user.fk_post_id = user_change.post_id
        user.fk_department_id = user_change.department_id
    elif action == 2:
        user.is_active = user_change.is_active



    await session.commit()
    return 202


async def get_tables(session):
    query = ((select(User.id, User.username, User.fk_department_id, department.name, User.fk_post_id, post.name,
                     User.is_pregnant, User.is_active)
              .join(department).filter(User.fk_department_id == department.id)
              .join(post).filter(User.fk_post_id == post.id))
              .where(User.is_superuser != True)
              .order_by(department.id).order_by(post.id))

    result = await session.execute(query)
    users = {'TableName': 'Пользователи',
             'TableData': []
             }

    result = result.all()
    for row in result:
        r = {
            'id': str(row[0]),
            'Username': row[1],
            'dep_id': row[2],
            'dep': row[3],
            'post_id': row[4],
            'post': row[5],
            'is_pregnant': row[6],
            'is_active': row[7]
        }

        users['TableData'].append(r)

    query = ((select(staff_positions.pk_fk_dep, department.name, staff_positions.pk_fk_post, post.name,
                     staff_positions.count)
              .join(department).filter(staff_positions.pk_fk_dep == department.id)
              .join(post).filter(staff_positions.pk_fk_post == post.id))
             .order_by(department.id).order_by(post.id))

    result = await session.execute(query)
    staff = {'TableName': 'Штатка',
             'TableData': []
             }

    result = result.all()
    for row in result:
        r = {
            'dep_id': row[0],
            'dep': row[1],
            'post_id': row[2],
            'post': row[3],
            'count': row[4]
        }
        staff['TableData'].append(r)
    return users, staff


@router.get('/get_staff', response_model=Staff)
async def get_staff(session: AsyncSession = Depends(get_async_session)):
    """Возвращает ВСЕХ пользователей"""
    users, staff = await get_tables(session)
    response_json = [users, staff]
    return JSONResponse(content=response_json, status_code=202)


async def download_zamruk(session: AsyncSession):
    query = (select(zamruk.fk_user_id, User.username, zamruk.fk_dep_id, department.name)
             .select_from(zamruk)
             .join(User, zamruk.fk_user_id == User.id)
             .join(department, zamruk.fk_dep_id == department.id)).order_by(zamruk.fk_dep_id)

    result = await session.execute(query)
    zamruk_table = {'TableName': 'Замруки',
                    'TableData': []
                    }

    result = result.all()
    for row in result:
        r = {
            'zamruk_id': str(row[0]),
            'zamruk_name': row[1],
            'dep_id': row[2],
            'dep': row[3]
        }
        zamruk_table['TableData'].append(r)
    return zamruk_table


@router.get('/zamruk')
async def get_zamruk(session: AsyncSession = Depends(get_async_session)):
    zamruk_table = await download_zamruk(session)
    return JSONResponse(content=zamruk_table, status_code=202)

@router.get('/post', response_model=Post)
async def get_zamruk(session: AsyncSession = Depends(get_async_session)):
    query = select(post.id, post.name)
    result = await session.execute(query)
    result = result.all()
    response_json = {int(elem[0]): elem[1] for elem in result}
    return JSONResponse(content=response_json, status_code=202)

@router.get('/dep', response_model=Department)
async def get_zamruk(session: AsyncSession = Depends(get_async_session)):
    query = select(department.id, department.name)
    result = await session.execute(query)
    result = result.all()
    response_json = {int(elem[0]): elem[1] for elem in result}
    return JSONResponse(content=response_json, status_code=202)