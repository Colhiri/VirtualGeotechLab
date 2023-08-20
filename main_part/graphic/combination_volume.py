import numpy as np
from scipy import interpolate
from scipy.stats import stats

import json
import random
import math

from GEOF.main_part.main_tools.main_functions import interpolation, nearest, bezier_curve, random_values

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

        y_pressR_RZG = self.control_points.get("y_pressR_RZG")

        self.koef_puasson = self.control_points.get("Puasson")
        self.angle_dilatanci = self.control_points.get("Dilatanci")

        self.delta_EV_E0 = self.control_points.get("delta_EV_E0")

        self.yfit = self.control_points.get("y_done")

        # Существующие схемы
        self.get_type_grunt()
        self.schema = self.type_grunt_dct.get('traxial').get(self.grunt)

        if y_pressR_RZG:
            self.points_press = self.data.get('traxial').get(self.schema).get("point_values_X")
        else:
            self.points_press = self.data.get('traxial').get(self.schema).get("point_values_X")

        self.point_values_X = self.data.get('volume_traxial').get(self.schema).get("point_values_X")
        self.point_values_Y = self.data.get('volume_traxial').get(self.schema).get("point_values_Y")
        self.method_interpolate = self.data.get('volume_traxial').get(self.schema).get("method_interpolate")
        self.limit_axe_X = self.data.get('volume_traxial').get(self.schema).get("limit_axe_X")
        self.limit_axe_Y = self.data.get('volume_traxial').get(self.schema).get("limit_axe_Y")
        self.list_X_min = self.data.get('volume_traxial').get(self.schema).get("list_X_min")
        self.list_X_max = self.data.get('volume_traxial').get(self.schema).get("list_X_max")
        self.list_Y_min = self.data.get('volume_traxial').get(self.schema).get("list_Y_min")
        self.list_Y_max = self.data.get('volume_traxial').get(self.schema).get("list_Y_max")

        ### Проценты с APP
        self.count_points_min = int(self.data.get('volume_traxial').get(self.schema).get("count_points_min"))
        self.count_points_max = int(self.data.get('volume_traxial').get(self.schema).get("count_points_max"))
        self.random_percent_min = float(self.data.get('volume_traxial').get(self.schema).get("random_percent_min"))
        self.random_percent_max = float(self.data.get('volume_traxial').get(self.schema).get("random_percent_max"))

        self.multiple_percent = 3

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
        self.max_point = min(self.point_values_X)

        # Получили проценты расчетом
        self.new_percents_min_x = []
        self.new_percents_max_x = []
        for count, val in enumerate(self.point_values_X, 0):
            val_new_min_x = ((val / self.max_point) * 100 - self.list_X_min[count] * self.multiple_percent)
            val_new_max_x = ((val / self.max_point) * 100 + self.list_X_max[count] * self.multiple_percent)
            self.new_percents_min_x.append(val_new_min_x)
            self.new_percents_max_x.append(val_new_max_x)

    def points_reload(self):
        """
        Создает новые точки на основе контрольных и опорных точек и отхождений.
        :return:
        """

        max_index_press = self.points_press.index(max(self.points_press))

        EV_END_1 = self.point_values_X[max_index_press]

        self.otnVertDef = [x / 76 for x in self.point_values_Y]

        if self.points_press[max_index_press] == self.points_press[-1]:

            if self.angle_dilatanci > 0:
                EV_END_2 = EV_END_1 + (
                (-(2 * (self.otnVertDef[max_index_press - 1] - self.otnVertDef[
                    max_index_press]) * math.sin(math.radians(self.angle_dilatanci))) / (
                         1 - math.sin(math.radians(self.angle_dilatanci)))))
            if self.angle_dilatanci <= 0:
                EV_END_2 = EV_END_1 - (
                    (-(2 * (self.otnVertDef[max_index_press - 1] - self.otnVertDef[
                        max_index_press]) * math.sin(math.radians(self.angle_dilatanci))) / (
                             1 - math.sin(math.radians(self.angle_dilatanci)))))

            max_index_press -= 1


        else:

            if self.angle_dilatanci > 0:
                EV_END_2 = EV_END_1 + ((-(2 * (self.otnVertDef[max_index_press] - self.otnVertDef[
                    max_index_press + 1]) * math.sin(math.radians(self.angle_dilatanci))) / (
                         1 - math.sin(math.radians(self.angle_dilatanci)))))
            if self.angle_dilatanci <= 0:
                EV_END_2 = EV_END_1 - ((-(2 * (self.otnVertDef[max_index_press] - self.otnVertDef[
                    max_index_press + 1]) * math.sin(math.radians(self.angle_dilatanci))) / (
                         1 - math.sin(math.radians(self.angle_dilatanci)))))

        # print(self.angle_dilatanci)
        # print(max_index_press)
        # print(EV_END_1)
        # print(EV_END_2)

        self.point_x = [0, -self.delta_EV_E0, EV_END_1, EV_END_2]


        max_x_real = min(self.point_values_X) # min(self.point_x)

        percents_x = [random.randint(int(perc_min * 100), int(perc_max * 100)) / 10000 for perc_min, perc_max in
                      zip(self.new_percents_min_x, self.new_percents_max_x)]

        new_point_x = []
        for count, perc in enumerate(percents_x, 0):
            if count in [1]:
                new_point_x.append(self.point_x[count])
                continue
            if count in [max_index_press]:
                new_point_x.append(self.point_x[-2])
                continue
            if count in [max_index_press + 1]:
                new_point_x.append(self.point_x[-1])
                continue
            if count > max_index_press + 1:
                new_point_x.append(perc * max_x_real + abs(EV_END_2))
                continue
            new_point_x.append(perc * max_x_real + self.point_x[0])

        self.new_point_x = new_point_x

        return self.new_point_x, self.yfit, EV_END_1, EV_END_2

    def get_parameters_points(self):
        return {'method_interpolate': self.method_interpolate,
                'count_point': random.randint(int(self.count_points_min), int(self.count_points_max)),
                'random_percent_min': self.random_percent_min,
                'random_percent_max': self.random_percent_max,
                }
