import sqlite3

class DataDitributor:
    def __init__(self, path_to_data=None):
        if path_to_data is None:
            self.path_to_data = ".\\geofvck.db"
        else:
            self.path_to_data = path_to_data

        self.conn = sqlite3.connect(self.path_to_data)

        self.cursor = self.conn.cursor()

    # Получить данные о пользователях
    def get_company_data(self):
        pass

    def get_user_parameters(self, id_user):
        pass

    # Записать данные о пользователях
    def write_company(self, id_company, ip, name_company):
        pass


    def write_people_company(self):
        pass

    def write_first_data_points(self):
        pass

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







