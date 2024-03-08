import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server_app.src.auth.model import User, department, post, staff_positions


async def get_staff(session: AsyncSession):
    """Забирает user и staff_position и отдает датафреймы их"""
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


async def fire_staff(session: AsyncSession, user_uuid: uuid):
    """Уволить сотрудника по uuid"""



async def hire_staff(session: AsyncSession, name: str, post_id: int, dep_id: int):
    """Нанять сотрудника
    params:
        name: Имя
        post_id: Должность
        dep_id: Отдел
    """


async def get_orders(session: AsyncSession):
    """Вернуть все приказы"""

async def create_order(session: AsyncSession):
    """Создать новый приказ"""


async def delete_order(session: AsyncSession, order_uuid: uuid):
    """Удалить приказ по uuid"""

