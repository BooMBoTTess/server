from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker
from server_app.src.auth.model import department, post, User, staff_positions
import random
import uuid
from config import DB_USER, DB_PORT, DB_PASS, DB_NAME, DB_HOST


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
fake = Faker(['ru_RU'])

# with Session(engine) as session:


def fill_dep():
    dep_table = [department(id=0, name='Отдел 1'),
                 department(id=1, name='Отдел 2'),
                 department(id=2, name='Отдел 3'),
                 department(id=3, name='Отдел 4'),
                 department(id=4, name='Отдел 5',),
                 department(id=5, name='Отдел 6')
                 ]

    with Session(engine) as session:
        session.add_all(dep_table)
        session.commit()

    return len(dep_table)


def fill_post():
    posts = ["Должность 1", "Должность 2", "Должность 3"]
    posts = list(reversed(posts))
    post_table = [post(id=i, name=posts[i]) for i in range(len(posts))]

    with Session(engine) as session:
        session.add_all(post_table)
        session.commit()

    return 12


def fill_users(count_dep):
    users = []
    for id in range(100):
        users.append([
            uuid.uuid4(),
            fake.name(),
            datetime.now(),
            f'{random.randint(100,999)}',
            '$2b$12$tFnHx5nr.UBQfdwVzxiDfeNnCQw3jirBScPOwXxxNvhPP84ll7aza',
            True,
            False,
            False,
            random.randint(0, count_dep),
            random.randint(3, 11)
        ])
    user_table = []
    for item in users:
        user_table.append(User(
            id=item[0],
            username=item[1],
            registered_at=item[2],
            email=item[3],
            hashed_password=item[4],
            is_active=item[5],
            is_superuser=item[6],
            is_verified=item[7],
            fk_department_id=item[8],
            fk_post_id=item[9]
        ))
    with Session(engine) as session:
        session.add_all(user_table)
        session.commit()
    print(users)
    return 0


def fill_staff(count_post : int, count_dep : int):
    table = []
    for d in range(count_dep):
        for p in range(3, count_post):
            table.append(
                staff_positions(
                    pk_fk_dep=d,
                    pk_fk_post=p,
                    count=random.randint(5, 10)
                )
            )

    with Session(engine) as session:
        session.add_all(table)
        session.commit()
    return 0


if __name__ == '__main__':
    fill_dep()
    fill_post()
    fill_users(5)
