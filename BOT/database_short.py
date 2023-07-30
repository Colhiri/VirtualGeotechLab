import sqlite3

conn = sqlite3.connect('geofvck.db')

cursor = conn.cursor()

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


### Схемы для испытаний (Трехосное сжатие ((press, e1), (ev, e1)), Одноплоскостной срез (press, e1))
create_table_main_points = '''CREATE TABLE point_values_X (
schema_id TEXT PRIMARY KEY UNIQUE NOT NULL,
id_people TEXT NOT NULL,
type TEXT NOT NULL,
point0 REAL,
point1 REAL,
point2 REAL,
point3 REAL,
point4 REAL,
point5 REAL,
point6 REAL,
point7 REAL,
point8 REAL,
point9 REAL,
point10 REAL,
point11 REAL,
point12 REAL,
point13 REAL,
point14 REAL,
point15 REAL,
point16 REAL,
point17 REAL,
point18 REAL,
point19 REAL,
point20 REAL,
point21 REAL,
point22 REAL,
point23 REAL,
point24 REAL,
point25 REAL,
point26 REAL,
point27 REAL,
point28 REAL,
point29 REAL,
point30 REAL
);
'''

create_table_main_points_y = '''CREATE TABLE point_values_Y (
schema_id TEXT PRIMARY KEY UNIQUE NOT NULL,
id_people TEXT NOT NULL,
type TEXT NOT NULL,
point0 REAL,
point1 REAL,
point2 REAL,
point3 REAL,
point4 REAL,
point5 REAL,
point6 REAL,
point7 REAL,
point8 REAL,
point9 REAL,
point10 REAL,
point11 REAL,
point12 REAL,
point13 REAL,
point14 REAL,
point15 REAL,
point16 REAL,
point17 REAL,
point18 REAL,
point19 REAL,
point20 REAL,
point21 REAL,
point22 REAL,
point23 REAL,
point24 REAL,
point25 REAL,
point26 REAL,
point27 REAL,
point28 REAL,
point29 REAL,
point30 REAL
);
'''
create_table_perc_points_x_min = '''CREATE TABLE list_X_min (
schema_id TEXT PRIMARY KEY UNIQUE NOT NULL,
id_people TEXT NOT NULL,
type TEXT NOT NULL,
point0 REAL,
point1 REAL,
point2 REAL,
point3 REAL,
point4 REAL,
point5 REAL,
point6 REAL,
point7 REAL,
point8 REAL,
point9 REAL,
point10 REAL,
point11 REAL,
point12 REAL,
point13 REAL,
point14 REAL,
point15 REAL,
point16 REAL,
point17 REAL,
point18 REAL,
point19 REAL,
point20 REAL,
point21 REAL,
point22 REAL,
point23 REAL,
point24 REAL,
point25 REAL,
point26 REAL,
point27 REAL,
point28 REAL,
point29 REAL,
point30 REAL
);
'''
create_table_perc_points_x_max = '''CREATE TABLE list_X_max (
schema_id TEXT PRIMARY KEY UNIQUE NOT NULL,
id_people TEXT NOT NULL,
type TEXT NOT NULL,
point0 REAL,
point1 REAL,
point2 REAL,
point3 REAL,
point4 REAL,
point5 REAL,
point6 REAL,
point7 REAL,
point8 REAL,
point9 REAL,
point10 REAL,
point11 REAL,
point12 REAL,
point13 REAL,
point14 REAL,
point15 REAL,
point16 REAL,
point17 REAL,
point18 REAL,
point19 REAL,
point20 REAL,
point21 REAL,
point22 REAL,
point23 REAL,
point24 REAL,
point25 REAL,
point26 REAL,
point27 REAL,
point28 REAL,
point29 REAL,
point30 REAL
);
'''
create_table_perc_points_y_min = '''CREATE TABLE list_Y_min (
schema_id TEXT PRIMARY KEY UNIQUE NOT NULL,
id_people TEXT NOT NULL,
type TEXT NOT NULL,
point0 REAL,
point1 REAL,
point2 REAL,
point3 REAL,
point4 REAL,
point5 REAL,
point6 REAL,
point7 REAL,
point8 REAL,
point9 REAL,
point10 REAL,
point11 REAL,
point12 REAL,
point13 REAL,
point14 REAL,
point15 REAL,
point16 REAL,
point17 REAL,
point18 REAL,
point19 REAL,
point20 REAL,
point21 REAL,
point22 REAL,
point23 REAL,
point24 REAL,
point25 REAL,
point26 REAL,
point27 REAL,
point28 REAL,
point29 REAL,
point30 REAL
);
'''
create_table_perc_points_y_max = '''CREATE TABLE list_Y_max (
schema_id TEXT PRIMARY KEY UNIQUE NOT NULL,
id_people TEXT NOT NULL,
type TEXT NOT NULL,
point0 REAL,
point1 REAL,
point2 REAL,
point3 REAL,
point4 REAL,
point5 REAL,
point6 REAL,
point7 REAL,
point8 REAL,
point9 REAL,
point10 REAL,
point11 REAL,
point12 REAL,
point13 REAL,
point14 REAL,
point15 REAL,
point16 REAL,
point17 REAL,
point18 REAL,
point19 REAL,
point20 REAL,
point21 REAL,
point22 REAL,
point23 REAL,
point24 REAL,
point25 REAL,
point26 REAL,
point27 REAL,
point28 REAL,
point29 REAL,
point30 REAL
);
'''

# FOREIGN KEY (id_people, schema_id, type) REFERENCES schemas(id_people, id, type) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED

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