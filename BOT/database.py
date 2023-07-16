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
FOREIGN KEY (id_ip) REFERENCES organisation_ip(id));
'''

create_table_main_points = '''CREATE TABLE main_points (
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
FOREIGN KEY (schema_id) REFERENCES schemas(id)
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

# cursor.execute(create_main_table)
# cursor.execute(create_people_in_clients)
# cursor.execute(create_table_schemas)
# cursor.execute(create_table_main_points)
# cursor.execute(create_table_temporary_user)

conn.commit()

cursor.close()