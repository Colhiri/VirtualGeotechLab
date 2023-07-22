import sqlite3

conn = sqlite3.connect('geofvck.db')

cursor = conn.cursor()

create_main_table = '''CREATE TABLE clients (
id TEXT PRIMARY KEY UNIQUE,
name_client TEXT NOT NULL,
ip_prefix TEXT NOT NULL UNIQUE,
joining date datetime);
'''
create_people_in_clients = '''CREATE TABLE organisations_ip (
id TEXT PRIMARY KEY UNIQUE,
id_org TEXT,
ip TEXT UNIQUE,
name_comp TEXT,
connect_all INTEGER,
connect_per_day INTEGER,
FOREIGN KEY (id_org) REFERENCES clients(id));
'''
create_table_schemas = '''CREATE TABLE schemas (
id TEXT PRIMARY KEY,
name_schema TEXT,
id_ip TEXT,
type TEXT NOT NULL,
FOREIGN KEY (id_ip) REFERENCES organisation_ip(id));
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

"""
Возможные типы в точках:
traxial
unaxial
volume_traxial
"""
### Схемы для испытаний (Трехосное сжатие ((press, e1), (ev, e1)), Одноплоскостной срез (press, e1))
create_table_main_points = '''CREATE TABLE control_points_x (
id TEXT PRIMARY KEY,
schema_id TEXT,
type TEXT NOT NULL,
point1 INTEGER,
point2 INTEGER,
point3 INTEGER,
point4 INTEGER,
point5 INTEGER,
point6 INTEGER,
point7 INTEGER,
point8 INTEGER,
point9 INTEGER,
point10 INTEGER,
point11 INTEGER,
point12 INTEGER,
point13 INTEGER,
point14 INTEGER,
point15 INTEGER,
point16 INTEGER,
point17 INTEGER,
point18 INTEGER,
point19 INTEGER,
point20 INTEGER,
point21 INTEGER,
point22 INTEGER,
point23 INTEGER,
point24 INTEGER,
point25 INTEGER,
point26 INTEGER,
point27 INTEGER,
point28 INTEGER,
point29 INTEGER,
point30 INTEGER,
FOREIGN KEY (schema_id) REFERENCES schemas(id)
);
'''
create_table_main_points_y = '''CREATE TABLE control_points_y (
id TEXT PRIMARY KEY,
schema_id TEXT,
type TEXT NOT NULL,
point1 INTEGER,
point2 INTEGER,
point3 INTEGER,
point4 INTEGER,
point5 INTEGER,
point6 INTEGER,
point7 INTEGER,
point8 INTEGER,
point9 INTEGER,
point10 INTEGER,
point11 INTEGER,
point12 INTEGER,
point13 INTEGER,
point14 INTEGER,
point15 INTEGER,
point16 INTEGER,
point17 INTEGER,
point18 INTEGER,
point19 INTEGER,
point20 INTEGER,
point21 INTEGER,
point22 INTEGER,
point23 INTEGER,
point24 INTEGER,
point25 INTEGER,
point26 INTEGER,
point27 INTEGER,
point28 INTEGER,
point29 INTEGER,
point30 INTEGER,
FOREIGN KEY (schema_id) REFERENCES schemas(id)
);
'''
create_table_perc_points_x_min = '''CREATE TABLE perc_points_x_min (
id TEXT PRIMARY KEY,
schema_id TEXT,
type TEXT NOT NULL,
point1 INTEGER,
point2 INTEGER,
point3 INTEGER,
point4 INTEGER,
point5 INTEGER,
point6 INTEGER,
point7 INTEGER,
point8 INTEGER,
point9 INTEGER,
point10 INTEGER,
point11 INTEGER,
point12 INTEGER,
point13 INTEGER,
point14 INTEGER,
point15 INTEGER,
point16 INTEGER,
point17 INTEGER,
point18 INTEGER,
point19 INTEGER,
point20 INTEGER,
point21 INTEGER,
point22 INTEGER,
point23 INTEGER,
point24 INTEGER,
point25 INTEGER,
point26 INTEGER,
point27 INTEGER,
point28 INTEGER,
point29 INTEGER,
point30 INTEGER,
FOREIGN KEY (schema_id) REFERENCES schemas(id)
);
'''
create_table_perc_points_x_max = '''CREATE TABLE perc_points_x_max (
id TEXT PRIMARY KEY,
schema_id TEXT,
type TEXT NOT NULL,
point1 INTEGER,
point2 INTEGER,
point3 INTEGER,
point4 INTEGER,
point5 INTEGER,
point6 INTEGER,
point7 INTEGER,
point8 INTEGER,
point9 INTEGER,
point10 INTEGER,
point11 INTEGER,
point12 INTEGER,
point13 INTEGER,
point14 INTEGER,
point15 INTEGER,
point16 INTEGER,
point17 INTEGER,
point18 INTEGER,
point19 INTEGER,
point20 INTEGER,
point21 INTEGER,
point22 INTEGER,
point23 INTEGER,
point24 INTEGER,
point25 INTEGER,
point26 INTEGER,
point27 INTEGER,
point28 INTEGER,
point29 INTEGER,
point30 INTEGER,
FOREIGN KEY (schema_id) REFERENCES schemas(id)
);
'''
create_table_perc_points_y_min = '''CREATE TABLE perc_points_y_min (
id TEXT PRIMARY KEY,
schema_id TEXT,
type TEXT NOT NULL,
point1 INTEGER,
point2 INTEGER,
point3 INTEGER,
point4 INTEGER,
point5 INTEGER,
point6 INTEGER,
point7 INTEGER,
point8 INTEGER,
point9 INTEGER,
point10 INTEGER,
point11 INTEGER,
point12 INTEGER,
point13 INTEGER,
point14 INTEGER,
point15 INTEGER,
point16 INTEGER,
point17 INTEGER,
point18 INTEGER,
point19 INTEGER,
point20 INTEGER,
point21 INTEGER,
point22 INTEGER,
point23 INTEGER,
point24 INTEGER,
point25 INTEGER,
point26 INTEGER,
point27 INTEGER,
point28 INTEGER,
point29 INTEGER,
point30 INTEGER,
FOREIGN KEY (schema_id) REFERENCES schemas(id)
);
'''
create_table_perc_points_y_max = '''CREATE TABLE perc_points_y_max (
id TEXT PRIMARY KEY,
schema_id TEXT,
type TEXT NOT NULL,
point1 INTEGER,
point2 INTEGER,
point3 INTEGER,
point4 INTEGER,
point5 INTEGER,
point6 INTEGER,
point7 INTEGER,
point8 INTEGER,
point9 INTEGER,
point10 INTEGER,
point11 INTEGER,
point12 INTEGER,
point13 INTEGER,
point14 INTEGER,
point15 INTEGER,
point16 INTEGER,
point17 INTEGER,
point18 INTEGER,
point19 INTEGER,
point20 INTEGER,
point21 INTEGER,
point22 INTEGER,
point23 INTEGER,
point24 INTEGER,
point25 INTEGER,
point26 INTEGER,
point27 INTEGER,
point28 INTEGER,
point29 INTEGER,
point30 INTEGER,
FOREIGN KEY (schema_id) REFERENCES schemas(id)
);
'''
for command in [create_table_main_points,
                create_table_main_points_y,
                create_table_perc_points_x_min,
                create_table_perc_points_x_max,
                create_table_perc_points_y_min,
                create_table_perc_points_y_max]:
    cursor.execute(command)

# Удаление таблиц
# delete_table = '''DROP TABLE schemas'''

for command in []:
    cursor.execute(command)

conn.commit()

cursor.close()