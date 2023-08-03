import numpy as np
from scipy import interpolate
from scipy.stats import stats

import json
import random

"""
Необходимо сделать выбор кол-ва точек на графике в функции интерполяции
"""

class AnalyzeGraph:
    def __init__(self, organise_values, control_points, data, type_grunt_dct,):
        """
        Загрузка данных с файла по сохраненным схемам
        :param type_grunt: Н данный момент это является сохраненной схемой
        :param path_to_data:
        :param data:
        """
        self.organise_values = organise_values
        self.control_points = control_points
        self.data = data
        self.type_grunt_dct = type_grunt_dct

        # Параметры пробы для включения схем
        self.We = self.organise_values.get('We')
        self.p = self.organise_values.get('p')
        self.ps = self.organise_values.get('ps')
        self.e = self.organise_values.get('e')
        self.IL = self.organise_values.get('IL')
        self.IP = self.organise_values.get('IP')


        # Контрольные точки для заданных значений
        y_press16 = self.control_points.get("y_press16")
        y_pressE50 = self.control_points.get("y_pressE50")
        endE1 = self.control_points.get("endE1")

        pressStart1 = self.control_points.get("pressStart1")
        press16 = self.control_points.get("press16")
        pressE50 = self.control_points.get("pressE50")
        pressEnd1 = self.control_points.get("pressEnd1")

        press_rzg_END = self.control_points.get("press_rzg_END")
        y_pressR_RZG = self.control_points.get("y_pressR_RZG")

        if press_rzg_END:
            self.point_x = [pressStart1, press16, pressE50, press_rzg_END, pressEnd1]
            self.point_y = [0, y_press16, y_pressE50, y_pressR_RZG]
        else:
            self.point_x = [pressStart1, press16, pressE50, pressEnd1]
            self.point_y = [0, y_press16, y_pressE50]

        # Существующие схемы
        self.get_type_grunt()
        self.schema = self.type_grunt_dct.get('traxial').get(self.grunt)

        self.point_values_X = self.data.get('traxial').get(self.schema).get("point_values_X")
        self.point_values_Y = self.data.get('traxial').get(self.schema).get("point_values_Y")
        self.method_interpolate = self.data.get('traxial').get(self.schema).get("method_interpolate")
        self.limit_axe_X = self.data.get('traxial').get(self.schema).get("limit_axe_X")
        self.limit_axe_Y = self.data.get('traxial').get(self.schema).get("limit_axe_Y")
        self.list_X_min = self.data.get('traxial').get(self.schema).get("list_X_min")
        self.list_X_max = self.data.get('traxial').get(self.schema).get("list_X_max")
        self.list_Y_min = self.data.get('traxial').get(self.schema).get("list_Y_min")
        self.list_Y_max = self.data.get('traxial').get(self.schema).get("list_Y_max")

        ### Проценты с APP
        self.count_points_min = int(self.data.get('traxial').get(self.schema).get("count_points_min"))
        self.count_points_max = int(self.data.get('traxial').get(self.schema).get("count_points_max"))
        self.random_percent_min = float(self.data.get('traxial').get(self.schema).get("random_percent_min"))
        self.random_percent_max = float(self.data.get('traxial').get(self.schema).get("random_percent_max"))

    def random_percent(self):
        """
        Функция рандомного процента
        :return:
        """
        perc_min = int((100 - float(self.random_percent_min)) * 100)
        perc_max = int((100 + float(self.random_percent_max)) * 100)
        return random.randint(perc_min, perc_max) / 10000

    def get_type_grunt(self):
        """
        Поменяй на нормальный обработчик
        Поменяй на нормальный обработчик
        Поменяй на нормальный обработчик
        Поменяй на нормальный обработчик
        :return:
        """
        if str(self.IP) in ['nan', 'None'] or str(self.IL) in ['nan', 'None']:
            self.grunt = 'sand'
        else:
            if self.IP < 7:
                self.grunt = 'sandy_loam'
            elif self.IP < 17:
                self.grunt = 'loam'
            elif self.IP < 27:
                self.grunt = 'clay'

    def calculate_perc(self):
        """
        Считает проценты отхождения от опорных точек графика
        :return:
        """

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
            if count in [0, 1, 2]:
                self.new_percents_min_x[count] = 100
                self.new_percents_max_x[count] = 100

    def points_reload(self):
        """
        Создает новые точки на основе контрольных и опорных точек и отхождений.
        :return:
        """
        max_x_real = max(self.point_x) - self.point_x[0]

        percents_x = [random.randint(int(perc_min * 100), int(perc_max * 100)) / 10000 for perc_min, perc_max in
                      zip(self.new_percents_min_x, self.new_percents_max_x)]

        self.max_point_Y = max(self.point_values_Y) - self.point_values_Y[2]

        # Получили проценты расчетом
        self.new_percents_min_y = []
        self.new_percents_max_y = []
        for count, val in enumerate(self.point_values_Y, 0):
            val_new_min_y = ((val / (self.max_point_Y)) * 100 - self.list_Y_min[count])
            val_new_max_y = ((val / (self.max_point_Y)) * 100 + self.list_Y_max[count])
            self.new_percents_min_y.append(val_new_min_y)
            self.new_percents_max_y.append(val_new_max_y)

        # Убрали проценты с тех ячеек, что меньше или равно максимальной точке
        for count in range(len(self.new_percents_max_y)):
            if count in [0,1,2]:
                self.new_percents_min_y[count] = 100
                self.new_percents_max_y[count] = 100

        percents_y = [(random.randint(int(perc_min * 100), int(perc_max * 100)) / 10000) for perc_min, perc_max in
                      zip(self.new_percents_min_y, self.new_percents_max_y)]

        new_point_x = []
        for count, perc in enumerate(percents_x, 0):
            if count in [0,1,2]:
                new_point_x.append(self.point_x[count])
                continue
            if count in [self.point_values_X.index(max(self.point_values_X))]:
                new_point_x.append(self.point_x[-1])
                continue
            new_point_x.append(perc * max_x_real + self.point_x[0])

        new_point_y = []
        for count, perc in enumerate(percents_y, 0):
            if count in [0,1,2]:
                new_point_y.append(self.point_y[count])
                continue
            new_point_y.append(perc * self.max_point_Y + max(self.point_y))

        self.new_point_x = new_point_x
        self.new_point_y = new_point_y

        return self.new_point_x, self.new_point_y

    def interpolation(self):
        """
        Применяет метод интерполяции к выбранным точкам
        :return:
        """
        yfit = np.linspace(min(self.new_point_y), max(self.new_point_y), num=random.randint(int(self.count_points_min), int(self.count_points_max)))

        if self.method_interpolate == "interp1d":
            pchip = interpolate.interp1d(self.new_point_y, self.new_point_x, kind='linear')

        if self.method_interpolate == "CubicSpline":
            pchip = interpolate.CubicSpline(self.new_point_y, self.new_point_x)

        if self.method_interpolate == "PchipInterpolator":
            pchip = interpolate.PchipInterpolator(self.new_point_y, self.new_point_x)

        if self.method_interpolate == "Akima1DInterpolator":
            pchip = interpolate.Akima1DInterpolator(self.new_point_y, self.new_point_x)

        if self.method_interpolate == "BarycentricInterpolator":
            pchip = interpolate.BarycentricInterpolator(self.new_point_y, self.new_point_x)

        if self.method_interpolate == "KroghInterpolator":
            pchip = interpolate.KroghInterpolator(self.new_point_y, self.new_point_x)

        if self.method_interpolate == "make_interp_spline":
            pchip = interpolate.make_interp_spline(self.new_point_y, self.new_point_x)

        if self.method_interpolate == "nearest":
            pchip = interpolate.interp1d(self.new_point_y, self.new_point_x, kind='nearest')

        if self.method_interpolate == "quadratic":
            pchip = interpolate.interp1d(self.new_point_y, self.new_point_x, kind='quadratic')

        if self.method_interpolate == "cubic":
            pchip = interpolate.interp1d(self.new_point_y, self.new_point_x, kind='cubic')

        xnew = pchip(yfit)

        if type(yfit) != list:
            yfit = yfit.tolist()
        if type(xnew) != list:
            xnew = xnew.tolist()

        if type(xnew) == list:
            pass

        xnew = [self.random_percent() * x_value for x_value in xnew]

        return xnew, yfit
