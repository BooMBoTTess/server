import requests
import pandas as pd
from config import IP_ADDRESS
def get_data_from_server():
    """
    return: pd.DataFrame
    """

    r = requests.get(
        f'http://{IP_ADDRESS}:8000/staff/get_staff')
    df = r.json()

    df_active_users = pd.DataFrame(df[0]['TableData'])

    df_active_users = df_active_users[df_active_users['is_pregnant'] == False]
    df_active_users = df_active_users[df_active_users['is_active'] == True]

    df_staff = pd.DataFrame(df[1]['TableData'])

    r = requests.get(
        f'http://{IP_ADDRESS}:8000/staff/zamruk')
    df_zamruk_table = r.json()
    df_zamruk_table = pd.DataFrame(df_zamruk_table['TableData'])


    return df_active_users, df_staff, df_zamruk_table

def get_data_from_excel():
    pass



def preproc_data(df_users : pd.DataFrame, df_staff: pd.DataFrame, df_zamruk_table : pd.DataFrame):
    # custom_columns = ['id', 'ФИО', 'Должность_id', 'Должность', 'Отдел_id', 'Отдел']
    # cols = {df.columns[i]: custom_columns[i] for i in range(len(df.columns))}
    # df.rename(columns=cols, inplace=True)

    df_users_temp = df_users.loc[:, ['dep', 'post', 'Username']]
    df_users_temp = df_users_temp.groupby(by=['dep', 'post'], as_index=False).count().rename(columns={'Username': 'Штат'})


    df_staff_temp = df_staff.loc[:, ['dep', 'post', 'count']]


    df_dashboard_data = df_staff_temp.merge(df_users_temp, how='outer').fillna(0)
    df_dashboard_data = df_dashboard_data.merge(df_zamruk_table[['dep', 'zamruk_name']])
    # В этом моменте добавляются замруки, и убираются все чуваки, у которых нет замрука
    df_dashboard_data[['count', 'Штат']] = df_dashboard_data[['count', 'Штат']].astype(int)
    df_dashboard_data['Вакант'] = df_dashboard_data['count'] - df_dashboard_data['Штат']


    df_dashboard_data.rename(columns={'count': 'Всего', 'zamruk_name' : 'Замрук'}, inplace=True)
    df_dashboard_data = df_dashboard_data[['Замрук', 'dep', 'post', 'Штат', 'Вакант', 'Всего']]
    return df_dashboard_data



def main():
    """

    return: pd.DataFrame
    """
    try:
        df_active_users, df_staff, df_zamruk = get_data_from_server()
        df = preproc_data(df_active_users, df_staff, df_zamruk)
    except Exception as e:
        print(e)
        return(404)
    print('data get')
    # Штат, вакант, всего
    staff_values = [len(df_active_users), int(df_staff.sum()['count']) - len(df_active_users), df_staff.sum()['count']]
    return df, staff_values


if __name__ == '__main__':

    main()