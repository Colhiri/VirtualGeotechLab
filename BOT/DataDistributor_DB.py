import sqlite3
import random
import datetime


def OBJID():
    OBJID = (''.join([random.choice(list('1234567890ABCDEF'))
                      for x in range(32)]))
    return OBJID


class DataDitributor:
    def __init__(self, id_people, path_to_data=None):
        if path_to_data is None:
            self.path_to_data = ".\\geofvck.db"
        else:
            self.path_to_data = path_to_data

        self.conn = sqlite3.connect(self.path_to_data)
        self.cursor = self.conn.cursor()

        self.id_people = id_people

        self.cursor.execute('SELECT name_company FROM peoples WHERE id = ?', (self.id_people,))
        self.name_company = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT id_company FROM peoples WHERE id = ?', (self.id_people,))
        self.id_org = self.cursor.fetchone()[0]

        self.data = None

    """
    Связь с базой данных
    """
    def check_schemas_people(self):
        check = self.cursor.execute('SELECT id FROM schemas WHERE id_people = ?', (self.id_people,)).fetchone()
        if not check:
            self.data = {
                "id_people": self.id_people,
                "id_org": self.id_org,
                "traxial_scheme_now": 'test',
                "volume_traxial_scheme_now": 'test',
                "unaxial_scheme_now": 'test',
                "traxial":
                    {
                        "test":
                            {
                                "point_values_X": [0.1, 0.1 * 1.6, (0.25 - 0.1 * 1.6) / 2 + 0.1 * 1.6, 0.25],
                                "point_values_Y": [0.0, 0.4, 0.8, 1.6],
                                "method_interpolate": "PchipInterpolator",
                                "limit_axe_X": None,
                                "limit_axe_Y": 11.4,
                                "list_X_min": [0 for x in range(4)],
                                "list_X_max": [0 for x in range(4)],
                                "list_Y_min": [0 for x in range(4)],
                                "list_Y_max": [0 for x in range(4)],
                                "count_points_min": 200,
                                "count_points_max": 200,
                                "random_percent_min": 1,
                                "random_percent_max": 1,
                            },
                    },

                "volume_traxial":
                    {
                        "test":
                            {
                                "point_values_X": [0.0, 0.1, 0.2, 0.3],
                                "point_values_Y": [0.0, 0.4, 0.8, 1.6],
                                "method_interpolate": "PchipInterpolator",
                                # Лимиты п осям
                                "limit_axe_X": None,
                                "limit_axe_Y": 11.4,
                                # App
                                "list_X_min": [0 for x in range(4)],
                                "list_X_max": [0 for x in range(4)],
                                "list_Y_min": [0 for x in range(4)],
                                "list_Y_max": [0 for x in range(4)],
                                "count_points_min": 200,
                                "count_points_max": 200,
                                "random_percent_min": 1,
                                "random_percent_max": 1,
                            },
                    },

                "unaxial":
                    {
                        "test":
                            {
                                "point_values_X": [0.0, 0.1, 0.2, 0.3],
                                "point_values_Y": [0.0, 0.4, 0.8, 1.6],
                                "method_interpolate": "PchipInterpolator",
                                # Лимиты п осям
                                "limit_axe_X": None,
                                "limit_axe_Y": 11.4,
                                # App
                                "list_X_min": [0 for x in range(4)],
                                "list_X_max": [0 for x in range(4)],
                                "list_Y_min": [0 for x in range(4)],
                                "list_Y_max": [0 for x in range(4)],
                                "count_points_min": 200,
                                "count_points_max": 200,
                                "random_percent_min": 1,
                                "random_percent_max": 1,
                            },
                    },
            }

        else:
            """
            Загрузить схемы из database
            """
            self.get_data_in_database()

    def get_data_in_database(self):
        """Зайти в базу и получить ID всех схем пользователя"""
        IDs_schemas = [x[0] for x in self.cursor.execute(f'SELECT id FROM schemas WHERE id_people = ?',
                                    (self.id_people,)).fetchall()]

        names_schemas = [self.cursor.execute(f'SELECT name_schema FROM schemas WHERE id = ?',
                                            (ID,)).fetchall()[0][0] for ID in IDs_schemas]

        types_schemas = [self.cursor.execute(f'SELECT type FROM schemas WHERE id = ?',
                                    (ID,)).fetchall()[0][0] for ID in IDs_schemas]

        methods_interpolation = [self.cursor.execute(f'SELECT interpolation FROM schemas WHERE id = ?',
                                    (ID,)).fetchall()[0][0] for ID in IDs_schemas]

        limits_axe_X = [self.cursor.execute(f'SELECT limit_axe_X FROM schemas WHERE id = ?',
                                    (ID,)).fetchall()[0][0] for ID in IDs_schemas]

        limits_axe_Y = [self.cursor.execute(f'SELECT limit_axe_Y FROM schemas WHERE id = ?',
                                           (ID,)).fetchall()[0][0] for ID in IDs_schemas]

        self.data = {
            "id_people": self.id_people,
            "id_org": self.id_org,
            "traxial_scheme_now": self.cursor.execute('SELECT traxial FROM peoples WHERE id = ?', (self.id_people,)).fetchone()[0],
            "volume_traxial_scheme_now": self.cursor.execute('SELECT volume_traxial FROM peoples WHERE id = ?', (self.id_people,)).fetchone()[0],
            "unaxial_scheme_now": self.cursor.execute('SELECT unaxial FROM peoples WHERE id = ?', (self.id_people,)).fetchone()[0],
            "traxial": {},
            "volume_traxial": {},
            "unaxial": {},
                    }

        for id, name, type, interp, lim_X, lim_Y in zip(IDs_schemas, names_schemas, types_schemas, methods_interpolation, limits_axe_X, limits_axe_Y):
            new_data_type = {
                "point_values_X": [value for value in self.cursor.execute('SELECT * FROM point_values_X WHERE schema_id = ?', (id, )).fetchone()[5:] if value is not None],
                "point_values_Y": [value for value in self.cursor.execute('SELECT * FROM point_values_Y WHERE schema_id = ?', (id, )).fetchone()[5:] if value is not None],
                "method_interpolate": self.cursor.execute('SELECT interpolation FROM schemas WHERE id = ?', (id,)).fetchone()[0],
                # Лимиты п осям
                "limit_axe_X": lim_X,
                "limit_axe_Y": lim_Y,
                # App
                "list_X_min": [value for value in self.cursor.execute('SELECT * FROM list_X_min WHERE schema_id = ?', (id, )).fetchone()[5:] if value is not None],
                "list_X_max": [value for value in self.cursor.execute('SELECT * FROM list_X_max WHERE schema_id = ?', (id, )).fetchone()[5:] if value is not None],
                "list_Y_min": [value for value in self.cursor.execute('SELECT * FROM list_Y_min WHERE schema_id = ?', (id, )).fetchone()[5:] if value is not None],
                "list_Y_max": [value for value in self.cursor.execute('SELECT * FROM list_Y_max WHERE schema_id = ?', (id, )).fetchone()[5:] if value is not None],
                "count_points_min": self.cursor.execute(f'SELECT count_points_min FROM schemas WHERE id = ?', (id, )).fetchone()[0],
                "count_points_max": self.cursor.execute(f'SELECT count_points_max FROM schemas WHERE id = ?', (id, )).fetchone()[0],
                "random_percent_min": self.cursor.execute(f'SELECT random_percent_min FROM schemas WHERE id = ?', (id, )).fetchone()[0],
                "random_percent_max": self.cursor.execute(f'SELECT random_percent_max FROM schemas WHERE id = ?', (id, )).fetchone()[0],
                    }
            self.data.get(type).update({name: new_data_type})

    def write_use_schemas_people(self, name_traxial, name_volume_traxial, name_unaxial):
        if isinstance(name_traxial, tuple):
            name_traxial = name_traxial[0]
        if isinstance(name_traxial, tuple):
            name_volume_traxial = name_volume_traxial[0]
        if isinstance(name_traxial, tuple):
            name_unaxial = name_unaxial[0]
        self.cursor.execute(f'UPDATE peoples SET traxial = ?, volume_traxial = ?, unaxial = ? WHERE id = ?',
                            (name_traxial, name_volume_traxial, name_unaxial, self.id_people, ))
        self.conn.commit()

    def write_data_in_database(self):
        for type_schema in ('traxial', 'volume_traxial', 'unaxial'):
            """Пройтись по схемам в словаре"""
            name_schemas = list(self.data.get(type_schema).keys())
            try:
                name_schemas.remove("scheme_now")
            except:
                pass

            for name in name_schemas:
                """Пройтись по именам схем в словаре"""
                number_point = [f'point{count}' for count in (range(len(self.data.get(type_schema).get(name).get("point_values_X"))))]

                point_values_X = {point: value for point, value in zip(number_point, self.data.get(type_schema).get(name).get("point_values_X"))}
                point_values_Y = {point: value for point, value in zip(number_point, self.data.get(type_schema).get(name).get("point_values_Y"))}
                list_X_min = {point: value for point, value in zip(number_point, self.data.get(type_schema).get(name).get("list_X_min"))}
                list_X_max = {point: value for point, value in zip(number_point, self.data.get(type_schema).get(name).get("list_X_max"))}
                list_Y_min = {point: value for point, value in zip(number_point, self.data.get(type_schema).get(name).get("list_Y_min"))}
                list_Y_max = {point: value for point, value in zip(number_point, self.data.get(type_schema).get(name).get("list_Y_max"))}

                data_points = {name: lst for name, lst in zip(['point_values_X', 'point_values_Y', 'list_X_min', 'list_X_max', 'list_Y_min', 'list_Y_max'],
                                                              [point_values_X, point_values_Y, list_X_min, list_X_max, list_Y_min, list_Y_max])}

                OBJ_schemas = self.add_new_schema_in_database(name, type_schema)

                for name_lst, lst in data_points.items():
                    """Пройтись по именам и значениям таблиц с точками схем в словаре"""
                    """Добавить схему, если ее нет."""
                    self.add_new_points_in_database(name_lst, OBJ_schemas, type_schema)

                    for key, value in lst.items():
                        self.cursor.execute(f'UPDATE {name_lst} SET {key} = ? WHERE schema_id = ?', (value, OBJ_schemas,))
                        self.conn.commit()

        # Обновить текущие схемы в базе из временного словаря
        self.write_use_schemas_people(self.data.get('traxial_scheme_now'),
                                      self.data.get('volume_traxial_scheme_now'),
                                      self.data.get('unaxial_scheme_now'))

        print('Данные сохранены')

    def add_new_points_in_database(self, name_table, schema_id, type_schema):
        name_schema = self.cursor.execute(f'SELECT name_schema FROM schemas WHERE id = ?', (schema_id, )).fetchone()[0]
        interpolation = self.cursor.execute(f'SELECT interpolation FROM schemas WHERE id = ?', (schema_id, )).fetchone()[0]
        self.cursor.execute(
            f'INSERT OR REPLACE INTO {name_table} (schema_id, name_schema, interpolation, id_people, type) '
            f'VALUES (?, ?, ?, ?, ?)',
            (schema_id, name_schema, interpolation, self.id_people, type_schema))
        self.conn.commit()

    def add_new_schema_in_database(self, name_schema, type_schema):
        """
        Добавляет новую схему и возвращает ее идентификационный номер после добавления в базу.
        :param name_schema:
        :param type_schema:
        :return:
        """
        check = self.cursor.execute('SELECT id FROM schemas WHERE id_people = ? AND type = ? AND name_schema = ?',
                                    (self.id_people, type_schema, name_schema, )).fetchone()
        # Проверка на наличие id точек, если оно есть, то возвращается именно id, а не turple
        if check:
            check = check[0]

        self.cursor.execute(
            f'INSERT OR REPLACE INTO schemas (id, name_schema, id_people, type, interpolation, limit_axe_X, limit_axe_Y,'
            f'count_points_min, count_points_max, random_percent_min, random_percent_max) '
            f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (OBJID() if not check else check, name_schema, self.id_people, type_schema,
             self.data.get(type_schema).get(name_schema).get('method_interpolate'),
             self.data.get(type_schema).get(name_schema).get('limit_axe_X'),
             self.data.get(type_schema).get(name_schema).get('limit_axe_Y'),
             self.data.get(type_schema).get(name_schema).get('count_points_min'),
             self.data.get(type_schema).get(name_schema).get('count_points_max'),
             self.data.get(type_schema).get(name_schema).get('random_percent_min'),
             self.data.get(type_schema).get(name_schema).get('random_percent_max')))
        self.conn.commit()

        return self.cursor.execute('SELECT id FROM schemas WHERE id_people = ? AND type = ? AND name_schema = ?',
                                    (self.id_people, type_schema, name_schema, )).fetchone()[0]

    def delete_schema_in_database(self, name_schema, type_schema):
        print(name_schema)
        print(type_schema)

        # Получить ID схемы
        id_schema = self.cursor.execute('SELECT id FROM schemas WHERE name_schema = ? AND type = ?', (name_schema, type_schema, )).fetchone()[0]
        # Удалить в схемах
        self.cursor.execute('DELETE FROM schemas WHERE id = ?', (id_schema, ))
        # Удалить в точках
        for table in ['point_values_X', 'point_values_Y', 'list_X_min', 'list_X_max', 'list_Y_min', 'list_Y_max']:
            self.cursor.execute(f'DELETE FROM {table} WHERE schema_id = ?', (id_schema, ))
            self.conn.commit()

    # Получить данные о пользователях
    def get_company_data(self):
        pass

    def get_user_parameters(self, id_user):
        pass

    # Записать данные о пользователях
    def write_company(self, name_company, ip_prefix, ):
        self.cursor.execute('INSERT INTO company (id, name_client, ip_prefix, joining_date) VALUES (?, ?, ?, ?)',
                            (OBJID(), name_company, ip_prefix, datetime.date.today(),))
        self.conn.commit()

        self.name_company = name_company
        print('Данные о компании записаны в базу данных')


    def write_people_company(self, id_user):
        self.cursor.execute(f'INSERT INTO peoples (id, id_company, name_company) VALUES (?, (SELECT id FROM clients WHERE company = "{self.name_company}", ?, ?)',
                            (id_user, None, self.name_company,))
        self.conn.commit()
        print('Данные пользователя записаны в базу данных')


    def write_temporary_user(self, user_id: int, user_name: str, user_surname: str, username: str):
        self.cursor.execute('INSERT INTO temp_user (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                       (user_id, user_name, user_surname, username))
        self.conn.commit()

    """
    Связь с временным словарем
    """

    def data_update(self, name_schema, dct: dict):
        """
        Обновление данных
        :param name_scheme:
        :param dct:
        :return:
        """
        pass

    def data_give(self):
        return self.data

    def add_new_schema_in_dct(self, name: str, type_schema: str):
        """
        Добавление новой схемы со стартовыми параметрами
        :param name:
        :return:
        """
        if name in self.data.get(type_schema).keys():
            print("Имя схемы уже существует! Задайте другое имя.")
            return
        if type_schema in ['traxial', 'volume_traxial']:
            self.data.get('traxial').setdefault(
                name,
                {
                    "point_values_X": [0.1, 0.1 * 1.6, (0.25 - 0.1 * 1.6) / 2 + 0.1 * 1.6, 0.25],
                    "point_values_Y": [0.0, 0.4, 0.8, 1.6],
                    "method_interpolate": "PchipInterpolator",
                    "limit_axe_X": None,
                    "limit_axe_Y": 11.4,
                    "list_X_min": [0 for x in range(4)],
                    "list_X_max": [0 for x in range(4)],
                    "list_Y_min": [0 for x in range(4)],
                    "list_Y_max": [0 for x in range(4)],
                    "count_points_min": 200,
                    "count_points_max": 200,
                    "random_percent_min": 1,
                    "random_percent_max": 1,
                })
            self.data.get('volume_traxial').setdefault(
                name,
                {
                    "point_values_X": [0.0, 0.1, 0.2, 0.3],
                    "point_values_Y": [0.0, 0.4, 0.8, 1.6],
                    "method_interpolate": "PchipInterpolator",
                    "limit_axe_X": None,
                    "limit_axe_Y": 11.4,
                    "list_X_min": [0 for x in range(4)],
                    "list_X_max": [0 for x in range(4)],
                    "list_Y_min": [0 for x in range(4)],
                    "list_Y_max": [0 for x in range(4)],
                    "count_points_min": 200,
                    "count_points_max": 200,
                    "random_percent_min": 1,
                    "random_percent_max": 1,
                })
        if type_schema in ['unaxial']:
            self.data.get('unaxial').setdefault(
                name,
                {
                    "point_values_X": [0.0, 0.1, 0.2, 0.3],
                    "point_values_Y": [0.0, 0.4, 0.8, 1.6],
                    "method_interpolate": "PchipInterpolator",
                    # Лимиты п осям
                    "limit_axe_X": None,
                    "limit_axe_Y": 11.4,
                    # App
                    "list_X_min": [0 for x in range(4)],
                    "list_X_max": [0 for x in range(4)],
                    "list_Y_min": [0 for x in range(4)],
                    "list_Y_max": [0 for x in range(4)],
                    "count_points_min": 200,
                    "count_points_max": 200,
                    "random_percent_min": 1,
                    "random_percent_max": 1,
                })

        self.write_data_in_database()
        print('Схема добавлена в базу данных')

    def delete_schema_in_dct(self, name_schema, type_schema):
        # Удалить из временного словаря
        if type_schema in ['traxial', 'volume_traxial']:
            self.data.get('traxial').pop(name_schema)
            self.data.get('volume_traxial').pop(name_schema)
            self.delete_schema_in_database(name_schema, 'traxial')
            self.delete_schema_in_database(name_schema, 'volume_traxial')
        if type_schema in ['unaxial']:
            self.data.get('unaxial').pop(name_schema)
            self.delete_schema_in_database(name_schema, 'unaxial')

        # Удалить из базы данных
        print('Схема удалена')
