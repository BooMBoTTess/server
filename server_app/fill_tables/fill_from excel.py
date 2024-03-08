import datetime

import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from uuid import UUID, uuid4
from config import DB_USER, DB_PORT, DB_PASS, DB_NAME, DB_HOST
from fill_tables import fill_post
"""
TRUNCATE TABLE post CASCADE;
TRUNCATE TABLE department CASCADE;
TRUNCATE TABLE "user" CASCADE;
TRUNCATE TABLE staff_position CASCADE;
"""
def fill_users():
    print('users')
    for index, row in df_dep.iterrows():
        insert_query = f"INSERT INTO department (id, name) VALUES ('{index}' ,'{row['Подразделение']}')"
        cursor.execute(insert_query)


    for index, row in df_post.iterrows():
        insert_query = f"INSERT INTO post (id, name) VALUES ('{index}' ,'{row['Должность']}')"
        cursor.execute(insert_query)

    df['uuid'] = ''

    for index, row in df.iterrows():
        my_uuid = uuid4()
        df.loc[index, 'uuid'] = my_uuid

        #Добавлять беременным беременность
        name = row['ФИО']
        if ')' in name:
            name = name.split('-')
            name = name[0]
            name = name.strip(' ')
            is_pregnant = True
        else:
            is_pregnant = False

        if row['Беременность'] != 1:
            is_pregnant_replaced = False
        else:
            is_pregnant_replaced = True


        kur_compare_name = name.split(' ')
        kur_compare_name = f"{kur_compare_name[0]} {kur_compare_name[1][0]}.{kur_compare_name[2][0]}."
        df_kurators.loc[df_kurators['Куратор'] == kur_compare_name, 'uuid'] = my_uuid

        datetime.datetime.now().strftime('%d.%m.%Y')

        insert_query = f"""
                    INSERT INTO "user" (id, username, registered_at, email, fk_department_id, fk_post_id, hashed_password, is_active, is_superuser, is_verified, is_pregnant, is_pregnant_replaced)
                VALUES ('{my_uuid}', '{name}', '{datetime.datetime.now().strftime('%d.%m.%Y')}', '{'qweqwe'}', '{row['Index_dep']}', '{row['Index_post']}', '{'$2b$12$tFnHx5nr.UBQfdwVzxiDfeNnCQw3jirBScPOwXxxNvhPP84ll7aza'}', '{'True'}', '{'False'}', '{'False'}', '{is_pregnant}', {is_pregnant_replaced})
            """
        cursor.execute(insert_query)

def fill_staff():
    print('staff')
    for index, row in df_staff.iterrows():
        insert_query = f"""
                INSERT INTO staff_position (pk_fk_dep, pk_fk_post, count)
                VALUES ('{row['Index_dep']}', '{row['Index_post']}', '{row['Количество']}')
            """
        cursor.execute(insert_query)

def fill_kurators():
    print('kurators')
    for index, row in df_kurators.iterrows():
        insert_query = f"""
                            INSERT INTO "dep_kurators" (fk_user_id, fk_dep_id)
                        VALUES ('{row['uuid']}', '{row['Index_dep']}')
                    """
        cursor.execute(insert_query)


# Ваши параметры подключения к PostgresSQL
db_params = {
    'host': DB_HOST,
    'port': DB_PORT,
    'user': DB_USER,
    'password': DB_PASS,
    'database': DB_NAME
}

try:
    engine = create_engine(
         f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()


    df = pd.read_excel('kadrifile.xlsx', sheet_name='Штатка', usecols='B:E', names=['Подразделение', 'Должность', 'ФИО', 'Беременность'])
    df1 = df.copy()


    df_dep = df.drop_duplicates(subset=['Подразделение'])
    df_dep = df_dep['Подразделение']
    df_dep.reset_index(drop=True, inplace=True)


    posts = []
    posts = list(reversed(posts))
    post_table = [[i, posts[i]] for i in range(len(posts))]
    df_post = pd.DataFrame(post_table)
    df_post.rename(columns={0 : 'Index', 1 : 'Должность'}, inplace=True)
    posts = {posts[i] : i for i in range(len(posts))}

    df['Index_dep'] = df['Подразделение'].replace(df_dep.reset_index().set_index('Подразделение').iloc[:, 0])
    df['Index_post'] = df['Должность'].replace(posts)
    df = df.dropna(subset='ФИО')


    df1.drop(columns='ФИО')

    df1 = df1[df1['Беременность'].isna()]
    df1.fillna('', inplace=True)

    df1['Index_dep'] = df1['Подразделение'].replace(df_dep.reset_index().set_index('Подразделение').iloc[:, 0])
    df1['Index_post'] = df1['Должность'].replace(posts)
    df_staff = df1.groupby(['Index_dep', 'Index_post']).size().reset_index(name='Количество')


    df_kurators = pd.read_excel('kadrifile.xlsx', sheet_name='zamruk', usecols='B:C', skiprows=2, header=1)
    df_kurators['Index_dep'] = df_kurators['Структурное подразделение'].replace(df_dep.reset_index().set_index('Подразделение').iloc[:, 0])
    df_kurators['uuid'] = ''

    df_dep = pd.DataFrame(df_dep)
    df_post = pd.DataFrame(df_post)

    print('users')
    fill_users()
    print('staff')
    fill_staff()
    print('kurators')
    fill_kurators()
    conn.commit()




except Exception as e:
    conn.rollback()
    print("Ошибка:", e)

