import json

class DataDistributor:
    def __init__(self, path_to_data=None, data=None):
        """
        Инициализирует файл с пути при отстутсвии передачи самой информации
        :param path_to_data: путь до файла с информацией
        :param data: да понятно же...
        """
        if path_to_data is None:
            self.path_to_data = ".\\data.json"
        else:
            self.path_to_data = path_to_data

        if data == None:
            try:
                with open(self.path_to_data, "r") as f:
                    self.data = json.load(f)
                print('Данные загружены')
            except:
                self.data = {
                    "scheme_now": "test",
                    "test":
                        {
                            "point_values_X": [0. , 0.1 * 1.6, (0.25 - 0.1 * 1.6) / 2 + 0.1 * 1.6, 0.25],
                            "point_values_Y": [0.0, 0.4, 0.8, 1.6],
                            "method_interpolate": "PchipInterpolator",
                            # Лимиты п осям
                            "limit_axe_X": None,
                            "limit_axe_Y": 11.4,
                            # Последние сохраненные значения основных точек
                            "last_save_values_X": [0.1, 0.1 * 1.6, (0.25 - 0.1 * 1.6) / 2 + 0.1 * 1.6, 0.25],
                            "last_save_values_Y": [0.0, 0.4, 0.8, 1.6],

                            # App
                            "list_X_min": [0 for x in range(4)],
                            "list_X_max": [0 for x in range(4)],
                            "list_Y_min": [0 for x in range(4)],
                            "list_Y_max": [0 for x in range(4)],
                            # Лимит уже есть по оси Y
                            "volume_list_x": [0, 0.05, 0.1, 0.15],
                            "volume_list_y": [0, 0, 0, 0],

                        },
                }
                self.data_save()
                print(f"Файл данных отсутствует. Создаю новый файл данных по пути: {self.path_to_data}")
        else:
            self.data = data

    def data_update(self, name_scheme, dct: dict):
        """
        Обновление данных

        №№№ Возможно этот метод стоит использовать чаще
        №№№ Возможно этот метод стоит использовать чаще
        №№№ Возможно этот метод стоит использовать чаще
        :param name_scheme:
        :param dct:
        :return:
        """
        for par, val in (dct.items()):
            self.data.get(name_scheme).update({par: val})

    def data_give(self):
        return self.data

    def data_save(self):
        """
        Сохранение даты в файл
        :return:
        """
        with open(self.path_to_data, "w") as f:
            json.dump(self.data, f)
        print('Данные сохранены')

    def data_load(self):
        """
        Загрузка даты из сохраненного файла
        :return:
        """
        with open(self.path_to_data, "r") as f:
            self.data = json.load(f)
        print('Данные загружены')

    def add_new_schema(self, name):
        """
        Добавление новой схемы со стартовыми параметрами
        :param name:
        :return:
        """
        if name in self.data.keys():
            print("Имя схемы уже существует! Задайте другое имя.")
            return
        self.data.setdefault(
        name,
        {
            "point_values_X": [0.1, 0.1 * 1.6, (0.25 - 0.1 * 1.6) / 2 + 0.1 * 1.6, 0.25],
            "point_values_Y": [0.0, 0.4, 0.8, 1.6],
            "method_interpolate": "PchipInterpolator",
            # Лимиты п осям
            "limit_axe_X": None,
            "limit_axe_Y": 11.4,
            # Последние сохраненные значения основных точек
            "last_save_values_X": [0.1, 0.1 * 1.6, (0.25 - 0.1 * 1.6) / 2 + 0.1 * 1.6, 0.25],
            "last_save_values_Y": [0.0, 0.4, 0.8, 1.6],

            # App
            "list_X_min": [0 for x in range(4)],
            "list_X_max": [0 for x in range(4)],
            "list_Y_min": [0 for x in range(4)],
            "list_Y_max": [0 for x in range(4)],
            # Лимит уже есть по оси Y
            "volume_list_x": [0, 0.05, 0.1, 0.15],
            "volume_list_y": [0, 0, 0, 0],
        })

    def delete_schema(self, schema):
        self.data.pop(schema)