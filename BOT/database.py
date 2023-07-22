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
create_table_schemas_trip = '''CREATE TABLE schemas_traxial (
id TEXT PRIMARY KEY,
name_schema TEXT,
id_ip TEXT,
FOREIGN KEY (id_ip) REFERENCES organisation_ip(id));
'''
create_table_schemas_s = '''CREATE TABLE schemas_uniaxial (
id TEXT PRIMARY KEY,
name_schema TEXT,
id_ip TEXT,
FOREIGN KEY (id_ip) REFERENCES organisation_ip(id));
'''
for command in [create_main_table,
                create_people_in_clients,
                create_table_schemas_trip,
                create_table_schemas_s]:
    cursor.execute(command)

### Схемы по трехосники
create_table_main_points = '''CREATE TABLE control_points_x_triax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_main_points_y = '''CREATE TABLE control_points_y_triax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_perc_points_x_min = '''CREATE TABLE perc_points_x_min_triax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_perc_points_x_max = '''CREATE TABLE perc_points_x_max_triax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_perc_points_y_min = '''CREATE TABLE perc_points_y_min_triax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_perc_points_y_max = '''CREATE TABLE perc_points_y_max_triax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
for command in [create_table_main_points,
                create_table_main_points_y,
                create_table_perc_points_x_min,
                create_table_perc_points_x_max,
                create_table_perc_points_y_min,
                create_table_perc_points_y_max]:
    cursor.execute(command)

### Схемы по однооснику
create_table_main_points_uniax = '''CREATE TABLE control_points_x_uniax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_uniaxial(id)
);
'''
create_table_main_points_y_uniax = '''CREATE TABLE control_points_y_uniax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_uniaxial(id)
);
'''
create_table_perc_points_x_min_uniax = '''CREATE TABLE perc_points_x_min_uniax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_uniaxial(id)
);
'''
create_table_perc_points_x_max_uniax = '''CREATE TABLE perc_points_x_max_uniax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_uniaxial(id)
);
'''
create_table_perc_points_y_min_uniax = '''CREATE TABLE perc_points_y_min_uniax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_uniaxial(id)
);
'''
create_table_perc_points_y_max_uniax = '''CREATE TABLE perc_points_y_max_uniax (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_uniaxial(id)
);
'''
for command in [create_table_main_points_uniax,
                create_table_main_points_y_uniax,
                create_table_perc_points_x_min_uniax,
                create_table_perc_points_x_max_uniax,
                create_table_perc_points_y_min_uniax,
                create_table_perc_points_y_max_uniax]:
    cursor.execute(command)

create_table_temporary_user = '''CREATE TABLE temp_user (
id INTEGER PRIMARY KEY,
user_id INTEGER,
user_name TEXT,
user_surname TEXT,
username STRING
);
'''

# Удаление таблиц
# delete_table = '''DROP TABLE schemas'''



### Схемы по трехосники
create_table_main_points_volume = '''CREATE TABLE control_points_x_volume (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_main_points_y_volume = '''CREATE TABLE control_points_y_volume (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_perc_points_x_min_volume = '''CREATE TABLE perc_points_x_min_volume (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_perc_points_x_max_volume = '''CREATE TABLE perc_points_x_max_volume (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_perc_points_y_min_volume = '''CREATE TABLE perc_points_y_min_volume (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
create_table_perc_points_y_max_volume = '''CREATE TABLE perc_points_y_max_volume (
id TEXT PRIMARY KEY,
schema_id TEXT,
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
FOREIGN KEY (schema_id) REFERENCES schemas_traxial(id)
);
'''
for command in [create_table_main_points_volume,
                create_table_main_points_y_volume,
                create_table_perc_points_x_min_volume,
                create_table_perc_points_x_max_volume,
                create_table_perc_points_y_min_volume,
                create_table_perc_points_y_max_volume]:
    cursor.execute(command)

for command in []:
    cursor.execute(command)

conn.commit()

cursor.close()