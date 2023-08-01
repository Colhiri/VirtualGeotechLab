import sqlite3
import datetime
import random

import database_short

conn = sqlite3.connect('geofvck.db')

cursor = conn.cursor()

def OBJID():
    OBJID = (''.join([random.choice(list('1234567890ABCDEF'))
                      for x in range(32)]))
    return OBJID

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