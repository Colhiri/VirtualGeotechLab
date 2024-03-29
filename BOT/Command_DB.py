import sqlite3
import datetime
import random

def OBJID():
    OBJID = (''.join([random.choice(list('1234567890ABCDEF'))
                      for x in range(32)]))
    return OBJID

def create_base():

    """
    Создание базы
    :return:
    """

    create_main_table = '''CREATE TABLE company (
    id TEXT PRIMARY KEY NOT NULL UNIQUE,
    name_company TEXT,
    ip_prefix TEXT NOT NULL UNIQUE,
    joining_date DATETIME
    );
    '''

    create_people_in_clients = '''CREATE TABLE peoples (
    id TEXT PRIMARY KEY NOT NULL UNIQUE,
    id_company TEXT NOT NULL,
    ip TEXT UNIQUE,
    name_company TEXT,
    traxial TEXT,
    volume_traxial TEXT,
    unaxial TEXT,
    consolidation TEXT,
    connect_per_day INTEGER,
    FOREIGN KEY (id_company) REFERENCES company(id) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
    );
    '''

    create_table_schemas = '''CREATE TABLE schemas (
    id TEXT PRIMARY KEY UNIQUE NOT NULL,
    name_schema TEXT NOT NULL,
    id_people TEXT NOT NULL,
    type TEXT NOT NULL,
    interpolation TEXT NOT NULL,
    limit_axe_X REAL,
    limit_axe_Y REAL,
    count_points_min INTEGER,
    count_points_max INTEGER,
    random_percent_min REAL,
    random_percent_max REAL,
    FOREIGN KEY (id_people) REFERENCES peoples(id) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
    );
    '''

    create_table_temporary_user = '''CREATE TABLE temp_user (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    user_name TEXT,
    user_surname TEXT,
    username STRING
    );
    '''

    for command in [create_main_table,
                    create_people_in_clients,
                    create_table_schemas,
                    create_table_temporary_user]:
        cursor.execute(command)

    # Генерируем перечисление столбцов point0, point1, ..., point49
    point_columns = ", ".join([f"point{i} REAL" for i in range(50)])

    # SQL запрос с подставленным перечислением столбцов
    for table in ['point_values_X',
                  'point_values_Y',
                  'list_X_min',
                  'list_X_max',
                  'list_Y_min',
                  'list_Y_max']:

        create_table = f'''CREATE TABLE {table} (
            schema_id TEXT PRIMARY KEY UNIQUE NOT NULL,
            name_schema TEXT NOT NULL,
            interpolation TEXT NOT NULL,
            id_people TEXT NOT NULL,
            type TEXT NOT NULL,
            {point_columns}
        );
        '''
        cursor.execute(create_table)

    conn.commit()
    cursor.close()


conn = sqlite3.connect('geofvck.db')

cursor = conn.cursor()

create_base()


"""
Создание company, user
"""

create_admin = f'''INSERT INTO company 
(id,
name_company, 
ip_prefix, 
joining_date)
VALUES 
('{OBJID()}',
'GEOF',
'192.168.',
'{datetime.date.today()}')
;
'''

create_company = f'''INSERT INTO peoples 
(id,
id_company,
name_company
)
VALUES 
('356379915',
(SELECT id FROM company WHERE name_company = 'GEOF'),
'GEOF'
);
'''

"""
delete_data = [cursor.execute(f'DELETE FROM {table}') for table in ['schemas', 'point_values_X', 'point_values_Y', 'list_X_min', 'list_X_max', 'list_Y_min', 'list_Y_max']]
conn.commit()
"""
for command in [
    create_admin,
    create_company,
                ]:
    cursor.execute(command)
    conn.commit()

cursor.close()