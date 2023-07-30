import sqlite3
import random
import datetime


def OBJID():
    OBJID = (''.join([random.choice(list('1234567890ABCDEF'))
                      for x in range(32)]))
    return OBJID


class DataDitributor:
    def __init__(self, ip_people, path_to_data=None):
        if path_to_data is None:
            self.path_to_data = ".\\geofvck.db"
        else:
            self.path_to_data = path_to_data

        self.conn = sqlite3.connect(self.path_to_data)
        self.cursor = self.conn.cursor()

        self.ip_people = ip_people

        self.cursor.execute('SELECT name_company FROM peoples WHERE ip = ?', (self.ip_people,))
        self.name_company = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT id FROM peoples WHERE ip = ?', (self.ip_people,))
        self.id_people = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT id_company FROM peoples WHERE ip = ?', (self.ip_people,))
        self.id_org = self.cursor.fetchone()[0]

    def check_schemas_people(self):
        check = self.cursor.execute('SELECT id FROM schemas WHERE id_people = ?', (self.id_people,)).fetchone()
        if not check:
            self.data = {
                "id_people": self.id_people,
                "id_org": self.id_org,
                "ip_people": self.ip_people,
                "traxial":
                    {
                        "scheme_now": "test",
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
                            },
                    },

                "volume_traxial":
                    {
                        "scheme_now": "test",
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
                            },
                    },

                "unaxial":
                    {
                        "scheme_now": "test",
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
            "ip_people": self.ip_people,
            "traxial": None,
            "volume_traxial": None,
            "unaxial": None,
                    }

        # Получить используемые схемы
        schemas_uses = {key: value for key, value in zip(('traxial', 'volume_traxial', 'unaxial'), self.cursor.execute(f'SELECT traxial, volume_traxial, unaxial FROM peoples WHERE id = ?',
                                            (self.id_people,)).fetchall()[0])}

        for id, name, type, interp, lim_X, lim_Y in zip(IDs_schemas, names_schemas, types_schemas, methods_interpolation, limits_axe_X, limits_axe_Y):
            for name_table in ['point_values_X', 'point_values_Y', 'list_X_min', 'list_X_max', 'list_Y_min', 'list_Y_max']:
                point_values_X = 1
                point_values_Y = 1
                list_X_min = 1
                list_X_max = 1
                list_Y_min = 1
                list_Y_max = 1
                new_data_type = {
                        "scheme_now": schemas_uses.get(type),
                        "test":
                            {
                                "point_values_X": [0.0, 0.1, 0.2, 0.3],
                                "point_values_Y": [0.0, 0.4, 0.8, 1.6],
                                "method_interpolate": "PchipInterpolator",
                                # Лимиты п осям
                                "limit_axe_X": lim_X,
                                "limit_axe_Y": lim_Y,
                                # App
                                "list_X_min": [0 for x in range(4)],
                                "list_X_max": [0 for x in range(4)],
                                "list_Y_min": [0 for x in range(4)],
                                "list_Y_max": [0 for x in range(4)],
                            },
                    },

        print()

    def write_use_schemas_people(self, name_traxial, name_volume_traxial, name_unaxial):
        self.cursor.execute(f'UPDATE peoples SET traxial = ?, volume_traxial = ?, unaxial = ? WHERE id = ?',
                            (name_traxial, name_volume_traxial, name_unaxial, self.id_people, ))
        self.conn.commit()


    def write_data_in_database(self):
        # Обновить текущие схемы в базе из временного словаря
        self.write_use_schemas_people(self.data.get('traxial').get("scheme_now"),
                                      self.data.get('volume_traxial').get("scheme_now"),
                                      self.data.get('unaxial').get("scheme_now"))

        for type_schema in ('traxial', 'volume_traxial', 'unaxial'):
            """Пройтись по схемам в словаре"""

            name_schemas = list(self.data.get(type_schema).keys())
            name_schemas.remove("scheme_now")

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

    def add_new_points_in_database(self, name_table, schema_id, type_schema):
        self.cursor.execute(
            f'INSERT OR REPLACE INTO {name_table} (schema_id, id_people, type) VALUES (?, ?, ?)',
            (schema_id, self.id_people, type_schema))
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
            f'INSERT OR REPLACE INTO schemas (id, name_schema, id_people, type, interpolation, limit_axe_X, limit_axe_Y) '
            f'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (OBJID() if not check else check, name_schema, self.id_people, type_schema,
             self.data.get(type_schema).get(name_schema).get('method_interpolate'),
             self.data.get(type_schema).get(name_schema).get('limit_axe_X'),
             self.data.get(type_schema).get(name_schema).get('limit_axe_Y')))
        self.conn.commit()

        return self.cursor.execute('SELECT id FROM schemas WHERE id_people = ? AND type = ? AND name_schema = ?',
                                    (self.id_people, type_schema, name_schema, )).fetchone()[0]

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

    def write_people_company(self):
        self.cursor.execute(f'INSERT INTO peoples (id, id_company, ip, name_company) VALUES (?, (SELECT id FROM clients WHERE company = "{self.name_company}", ?, ?)',
                            (OBJID(), None, self.ip_people, self.name_company,))
        self.conn.commit()



    def write_first_data_points(self):
        check = self.cursor.execute('SELECT id FROM schemas WHERE id_people = ?', (self.id_people,)).fetchone()
        if not check:
            self.add_new_schema('schema_1', 'traxial')


    def write_temporary_user(self):
        pass


    # Получить данные по id и типу схемы
    def get_data_points(self, id_user, type_schema):
        """
        Возможные типы в точках:
        traxial
        unaxial
        volume_traxial
        """
        if type_schema in ['', None]:
            print('Ошибка данных по схеме')
        if id_user in ['', None]:
            print('Ошибка данных по пользователю')

        if type_schema == 'traxial':
            pass
        if type_schema == 'unaxial':
            pass
        if type_schema == 'volume_traxial':
            pass

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

    def data_save(self, name_schema, type_schema):
        """
        Сохранение даты в файл
        :return:
        """
        check = self.cursor.execute('SELECT id FROM schemas WHERE id_people = ? and name_schema = ?', (self.id_people, name_schema,)).fetchone()
        if not check:
            if type_schema in ['traxial', 'volume_traxial']:
                self.cursor.execute(
                    f'INSERT INTO schemas (id, name_schema, id_people, type, interpolation, limit_axe_X, limit_axe_Y) '
                    f'VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (OBJID(), name_schema, self.id_people, 'traxial',
                     self.data.get(type_schema).get(name_schema).get('method_interpolate'),
                     self.data.get(type_schema).get(name_schema).get('limit_axe_X'),
                     self.data.get(type_schema).get(name_schema).get('limit_axe_Y')))
                self.conn.commit()

                self.cursor.execute(
                    f'INSERT INTO schemas (id, name_schema, id_people, type, interpolation, limit_axe_X, limit_axe_Y) '
                    f'VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (OBJID(), name_schema, self.id_people, 'volume_traxial',
                     self.data.get(type_schema).get(name_schema).get('method_interpolate'),
                     self.data.get(type_schema).get(name_schema).get('limit_axe_X'),
                     self.data.get(type_schema).get(name_schema).get('limit_axe_Y')))
                self.conn.commit()

            if type_schema in ['unaxial']:
                self.cursor.execute(
                    f'INSERT INTO schemas (id, name_schema, id_people, type, interpolation, limit_axe_X, limit_axe_Y) '
                    f'VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (OBJID(), name_schema, self.id_people, 'unaxial',
                     self.data.get(type_schema).get(name_schema).get('method_interpolate'),
                     self.data.get(type_schema).get(name_schema).get('limit_axe_X'),
                     self.data.get(type_schema).get(name_schema).get('limit_axe_Y')))
                self.conn.commit()

        else:
            if type_schema in ['traxial', 'volume_traxial']:
                self.cursor.execute('UPDATE schemas SET '
                                    'method_interpolate = ?, '
                                    'limit_axe_X = ?, '
                                    'limit_axe_Y = ?, '
                                    'WHERE id_people = ? AND type = ?',
                                    (self.data.get('traxial').get(name_schema).get('method_interpolate'),
                                     self.data.get('traxial').get(name_schema).get('limit_axe_X'),
                                     self.data.get('traxial').get(name_schema).get('limit_axe_Y'),
                                     self.id_people,
                                     'traxial',
                                     ))
                self.conn.commit()

                self.cursor.execute('UPDATE schemas SET '
                                    'method_interpolate = ?, '
                                    'limit_axe_X = ?, '
                                    'limit_axe_Y = ?, '
                                    'WHERE id_people = ? AND type = ?',
                                    (self.data.get('volume_traxial').get(name_schema).get('method_interpolate'),
                                     self.data.get('volume_traxial').get(name_schema).get('limit_axe_X'),
                                     self.data.get('volume_traxial').get(name_schema).get('limit_axe_Y'),
                                     self.id_people,
                                     'volume_traxial',
                                     ))
                self.conn.commit()

            if type_schema in ['unaxial']:
                self.cursor.execute('UPDATE schemas SET '
                                    'method_interpolate = ?, '
                                    'limit_axe_X = ?, '
                                    'limit_axe_Y = ?, '
                                    'WHERE id_people = ? AND type = ?',
                                    (self.data.get('unaxial').get(name_schema).get('method_interpolate'),
                                     self.data.get('unaxial').get(name_schema).get('limit_axe_X'),
                                     self.data.get('unaxial').get(name_schema).get('limit_axe_Y'),
                                     self.id_people,
                                     'unaxial',
                                     ))
                self.conn.commit()

        print('Данные сохранены')

    def data_load(self):
        """
        Загрузка даты из сохраненного файла
        :return:
        """
        print('Данные загружены')

    def add_new_schema(self, name: str, type_schema: str):
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
                })

    def delete_schema(self, schema, type_schema):
        if type_schema in ['traxial', 'volume_traxial']:
            self.data.get('traxial').pop(schema)
            self.data.get('volume_traxial').pop(schema)
        if type_schema in ['unaxial']:
            self.data.get('unaxial').pop(schema)

test = DataDitributor('192.168.86')
test.check_schemas_people()
test.write_data_in_database()