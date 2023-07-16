import json
import random

import scipy.stats as stats

class AnalyzeGraph:
    def __init__(self, type_grunt, path_to_data=None, data=None):
        """
        Загрузка данных с файла по сохраненным схемам
        :param type_grunt: Н данный момент это является сохраненной схемой
        :param path_to_data:
        :param data:
        """
        self.type_grunt = type_grunt

        if path_to_data is None:
            self.path_to_data = "..\\ENGGEO_program\\BOT\\data.json"
        else:
            self.path_to_data = path_to_data

        try:
            with open(self.path_to_data, "r") as f:
                self.data = json.load(f)
            # print('Данные загружены')
        except FileNotFoundError:
            print('Файл данных отсутствует')

    def get_first_data(self):

        self.point_values_X = self.data.get(self.type_grunt).get("point_values_X")
        self.point_values_Y = self.data.get(self.type_grunt).get("point_values_Y")
        self.method_interpolate = self.data.get(self.type_grunt).get("method_interpolate")
        self.limit_axe_X = self.data.get(self.type_grunt).get("limit_axe_X")
        self.limit_axe_Y = self.data.get(self.type_grunt).get("limit_axe_Y")
        self.last_save_values_X = self.data.get(self.type_grunt).get("last_save_values_X")
        self.last_save_values_Y = self.data.get(self.type_grunt).get("last_save_values_Y")
        self.list_X_min = self.data.get(self.type_grunt).get("list_X_min")
        self.list_X_max = self.data.get(self.type_grunt).get("list_X_max")
        self.list_Y_min = self.data.get(self.type_grunt).get("list_Y_min")
        self.list_Y_max = self.data.get(self.type_grunt).get("list_Y_max")

    def calculate_perc(self):
        """
        ### Мы считаем в графпике процент от точки, а не от максимальной точки...
        Либо перерасчет, либо нужно привязываться к максимальной точке.

        :return:
        """

        self.index_max = self.point_values_X.index(max(self.point_values_X))
        self.max_point = max(self.point_values_X)

        # Получили проценты расчетом
        self.new_percents_min_x = []
        self.new_percents_max_x = []
        for count, val in enumerate(self.point_values_X, 0):
            val_new_min_x = ((val / self.max_point) * 100 - self.list_X_min[count])
            val_new_max_x = ((val / self.max_point) * 100 + self.list_X_max[count])
            self.new_percents_min_x.append(val_new_min_x)
            self.new_percents_max_x.append(val_new_max_x)



        # Убрали проценты с тех ячеек, что меньше или равно максимальной точке
        for count in range(len(self.new_percents_min_x)):
            if count in [0, 1, 2, self.point_values_X.index(max(self.point_values_X))]:
                self.new_percents_min_x[count] = 100
                self.new_percents_max_x[count] = 100
            if count in [self.point_values_X.index(max(self.point_values_X))]:
                self.new_percents_min_x[self.point_values_X.index(max(self.point_values_X))] = 100
                self.new_percents_max_x[self.point_values_X.index(max(self.point_values_X))] = 100

    def points_reload(self, point_x, point_y):

        max_x_real = max(point_x)

        percents_x = [random.randint(int(perc_min * 100), int(perc_max * 100)) / 10000 for perc_min, perc_max in
                      zip(self.new_percents_min_x, self.new_percents_max_x)]

        """
        ####
        ####
        ####
        ####
        ####
        Сюда нужно поставлять словарь со значениями . Как минимум максимального Y
        """

        # -1 потому что это индекс E50, так как точка максимального давления непостоянна и контролируется от E50
        self.max_point_Y = max(point_y)

        # Получили проценты расчетом
        self.new_percents_min_y = []
        self.new_percents_max_y = []
        for count, val in enumerate(self.point_values_Y, 0):
            val_new_min_y = (((val) / (11.4 - self.max_point_Y * 1.5)) * 100 - self.list_Y_min[count])
            val_new_max_y = (((val) / (11.4 - self.max_point_Y * 1.5)) * 100 + self.list_Y_max[count])
            self.new_percents_min_y.append(val_new_min_y)
            self.new_percents_max_y.append(val_new_max_y)

        # Убрали проценты с тех ячеек, что меньше или равно максимальной точке
        for count in range(len(self.new_percents_max_y)):
            if count in [0, 1, 2]:
                self.new_percents_min_y[count] = 100
                self.new_percents_max_y[count] = 100
            if count in [self.point_values_X.index(max(self.point_values_X))]:
                self.new_percents_min_y[self.point_values_X.index(max(self.point_values_X))] = 100
                self.new_percents_max_y[self.point_values_X.index(max(self.point_values_X))] = 100


        percents_y = [(random.randint(int(perc_min * 100), int(perc_max * 100)) / 10000) for perc_min, perc_max in
                      zip(self.new_percents_min_y, self.new_percents_max_y)]


        new_point_x = []
        for count, perc in enumerate(percents_x, 0):
            if count in [0, 1, 2]:
                new_point_x.append(point_x[count])
                continue
            if count in [self.point_values_X.index(max(self.point_values_X))]:
                new_point_x.append(point_x[-1])
                continue
            new_point_x.append(perc * max_x_real)

        new_point_y = []
        for count, perc in enumerate(percents_y, 0):
            if count in [0, 1, 2]:
                new_point_y.append(point_y[count])
                continue
            if count in [self.point_values_X.index(max(self.point_values_X))]:
                if point_y[-1] < self.point_values_Y[self.point_values_X.index(max(self.point_values_X))]:
                    if self.point_values_Y[self.point_values_X.index(max(self.point_values_X))] <= new_point_y[-1]:
                        new_point_y.append(new_point_y[-1] * 1.01)
                    else:
                        new_point_y.append(self.point_values_Y[self.point_values_X.index(max(self.point_values_X))])
                else:
                    new_point_y.append(point_y[-1])
                continue
            new_point_y.append((perc) * (11.4-max(point_y)))

        return new_point_x, new_point_y
