import numpy as np
from scipy import interpolate
import customtkinter

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import LineCollection

import tkinter as tk
from tkinter import Listbox
import json
import sys

from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer

def dist_point_to_segment(p, s0, s1):
    """
    Get the distance from the point *p* to the segment (*s0*, *s1*), where
    *p*, *s0*, *s1* are ``[x, y]`` arrays.
    """
    s01 = s1 - s0
    s0p = p - s0
    if (s01 == 0).all():
        return np.hypot(*s0p)
    # Project onto segment, without going past segment ends.
    p1 = s0 + np.clip((s0p @ s01) / (s01 @ s01), 0, 1) * s01
    return np.hypot(*(p - p1))

def update_value_in_distibutor(method):
    def wrapper(*args, **kwargs):
        self = args[0]
        save_dct = {
            "point_values_X": self.point_values_X,
            "point_values_Y": self.point_values_Y,
            "limit_axe_X": self.limit_axe_X,
            "limit_axe_Y": self.limit_axe_Y,
            "last_save_values_X": self.last_save_values_X,
            "last_save_values_Y": self.last_save_values_Y,
                    }
        for key, value in save_dct.items():
            distribut.data.get(self.schema).update({key: value})

        return method(*args, **kwargs)

    return wrapper

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
                        },
                }
                self.data_save()
                print(f"Файл данных отсутствует. Создаю новый файл данных по пути: {self.path_to_data}")
        else:
            self.data = data

    def data_update(self, name_scheme, dct: dict):
        """
        Обновление данных

        №№№ Вохможно этот метод стоит использовать чаще
        №№№ Вохможно этот метод стоит использовать чаще
        №№№ Вохможно этот метод стоит использовать чаще
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
        })


distribut = DataDistributor()


class Graph:
    showverts = True
    epsilon = 5

    def __init__(self, ax, dct: dict):
        """
        Инициализация и создание первичных данных.

        :param ax: subplot
        :param poly: координаты точек
        :param name: имя шаблона
        :param method_interpolate:
        :param args: лимит по X, лимит по Y, инвертирования оси X, инвертирования оси Y
        """
        ### Распаковка элементов
        self.schema = dct.get("scheme_now")
        ### Точки для основной кривой
        self.point_values_X = dct.get(self.schema).get("point_values_X")
        self.point_values_Y = dct.get(self.schema).get("point_values_Y")
        ### Лимиты
        self.limit_axe_X = max(self.point_values_X) + 0.05
        self.limit_axe_Y = dct.get(self.schema).get("limit_axe_Y")
        ### Интерполяция
        self.method_interpolate = dct.get(self.schema).get("method_interpolate")
        ### Точки для дополнительных кривых
        self.last_save_values_X = dct.get(self.schema).get("last_save_values_X")
        self.last_save_values_Y = dct.get(self.schema).get("last_save_values_Y")

        ### Проценты с APP
        self.list_X_min = dct.get(self.schema).get("list_X_min")
        self.list_X_max = dct.get(self.schema).get("list_X_max")
        self.list_Y_min = dct.get(self.schema).get("list_Y_min")
        self.list_Y_max = dct.get(self.schema).get("list_Y_max")

        ### Инициализация переменных для нормальной работы
        self.ax = ax
        canvas = self.ax.figure.canvas

        self.background = None
        self._ind = None  # the active vert
        self.position_mouse_X = None
        self.position_mouse_Y = None
        self.drag = False

        canvas.mpl_connect('draw_event', self.on_draw)
        canvas.mpl_connect('button_press_event', self.on_button_press)
        canvas.mpl_connect('button_release_event', self.on_button_release)
        canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas = canvas

        ### Параметры оси по лимитам
        self.ax.set_xlim(0.1, self.limit_axe_X)
        self.ax.set_ylim(0, self.limit_axe_Y)

        ### Инвертирование оси Y
        self.axes_y = plt.gca()
        self.axes_y.invert_yaxis()

        # Линия с маркером
        self.line = Line2D(self.point_values_X, self.point_values_Y, linestyle="",
                           marker='o', markerfacecolor='r',
                           animated=True)
        # Интерполяция (стартовая) по линии с маркером
        self.line_without_marker = Line2D(self.point_values_X, self.point_values_Y, animated=True, color='green')
        self.line_without_marker.set_data(self.interpolation_line(self.point_values_X, self.point_values_Y))


        ###### Должно уйти в прослойку, т.к. при старте не загружает последние значения
        # Минимальная линия показывающая расхождения между оригиналом и возможным максимальным отклонением в отрицательную сторону
        self.line_minimum = Line2D(self.calculate(AXES=self.point_values_X, percents=self.list_X_min, symbol='-'), self.point_values_Y, animated=True, linestyle="",
                                   marker='.', color='blue')
        self.line_without_marker_minimum = Line2D(self.calculate(AXES=self.point_values_X, percents=self.list_X_min, symbol='-'), self.point_values_Y,
                                                  linestyle="--",
                                                  animated=True, color='blue')
        self.line_without_marker_minimum.set_data(self.interpolation_line(self.calculate(AXES=self.point_values_X, percents=self.list_X_min, symbol='-'), self.point_values_Y))

        # Макксимальная линия показывающая расхождения между оригиналом и возможным максимальным отклонением в положительную сторону
        self.line_maximum = Line2D(self.calculate(AXES=self.point_values_X, percents=self.list_X_max, symbol='+'),
                                   self.point_values_Y,
                                   animated=True, linestyle="",
                                   marker='.', color='red')
        self.line_without_marker_maximum = Line2D(self.calculate(AXES=self.point_values_X, percents=self.list_X_max, symbol='+'),
                                                  self.point_values_Y,
                                                  linestyle="--",
                                                  animated=True, color='red')
        self.line_without_marker_maximum.set_data(self.interpolation_line(self.calculate(AXES=self.point_values_X, percents=self.list_X_max, symbol='+'), self.point_values_Y))


        #### Несколько линий сразу для максимума и минимума по оси Y
        self.line_segments = LineCollection(self.Y_boundaries(), color='black', linestyle='solid')


        #### Добавление линий на оси
        #### Добавление линий на оси
        self.ax.add_line(self.line)
        self.ax.add_line(self.line_without_marker)
        self.ax.add_line(self.line_minimum)
        self.ax.add_line(self.line_without_marker_minimum)
        self.ax.add_line(self.line_maximum)
        self.ax.add_line(self.line_without_marker_maximum)
        self.ax.add_collection(self.line_segments)

    def Y_boundaries(self):

        segs = []
        for index in range(len(self.point_values_X)):
            line_ = [(self.point_values_X[index], self.point_values_Y[index] * ((100 - self.list_Y_min[index]) / 100)),
                     (self.point_values_X[index], self.point_values_Y[index] * ((100 + self.list_Y_max[index]) / 100))]
            segs.append(line_)
        return segs



    def calculate(self, AXES, percents, symbol):
        """
        Возвращает новые данные по X
        :param AXES: опорные точки (средняя линия)
        :param percents: отхождения от опорных точек
        :param symbol: "+" или "-"
        :return:
        """
        try:
            if symbol == '-':
                return [AX * ((100 - perc) / 100) for AX, perc in zip(AXES, percents[0])]
            if symbol == '+':
                return [AX * ((100 + perc) / 100) for AX, perc in zip(AXES, percents[0])]
        except:
            if symbol == '-':
                return [AX * ((100 - perc) / 100) for AX, perc in zip(AXES, percents)]
            if symbol == '+':
                return [AX * ((100 + perc) / 100) for AX, perc in zip(AXES, percents)]

    def instant_update_lines(self):
        """
        Обновляет значения линий при отсутствии ошибки интерполяции
        :return:
        """
        if len(distribut.data.get(self.schema).get("list_X_min")) < len(self.point_values_X):
            self.list_X_min = (distribut.data.get(self.schema).get("list_X_min"))[0]
        else:
            self.list_X_min = (distribut.data.get(self.schema).get("list_X_min"))

        if len(distribut.data.get(self.schema).get("list_X_max")) < len(self.point_values_X):
            self.list_X_max = (distribut.data.get(self.schema).get("list_X_max"))[0]
        else:
            self.list_X_max = (distribut.data.get(self.schema).get("list_X_max"))

        if len(distribut.data.get(self.schema).get("list_Y_min")) < len(self.point_values_X):
            self.list_Y_min = (distribut.data.get(self.schema).get("list_Y_min"))[0]
        else:
            self.list_Y_min = (distribut.data.get(self.schema).get("list_Y_min"))

        if len(distribut.data.get(self.schema).get("list_Y_max")) < len(self.point_values_X):
            self.list_Y_max = (distribut.data.get(self.schema).get("list_Y_max"))[0]
        else:
            self.list_Y_max = (distribut.data.get(self.schema).get("list_Y_max"))

        self.line_segments.set_segments(self.Y_boundaries())

        self.line_minimum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_min, symbol='-'),
                                self.point_values_Y)
        self.line_maximum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_max, symbol='+'),
                                self.point_values_Y)
        self.canvas.draw_idle()


    def on_draw(self, event):

        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

        self.ax.draw_artist(self.line)
        self.ax.draw_artist(self.line_minimum)
        self.ax.draw_artist(self.line_maximum)


        try:
            self.line_without_marker.set_data(self.interpolation_line(self.point_values_X, self.point_values_Y))
        except TypeError:
            pass
        self.ax.draw_artist(self.line_without_marker)

        try:
            self.line_without_marker_minimum.set_data(self.interpolation_line(self.line_minimum.get_xdata(), self.line_minimum.get_ydata()))
        except TypeError:
            pass

        self.ax.draw_artist(self.line_without_marker_minimum)

        try:
            self.line_without_marker_maximum.set_data(self.interpolation_line(self.line_maximum.get_xdata(),
                                                                              self.line_maximum.get_ydata()))
        except TypeError:
            pass
        self.ax.draw_artist(self.line_without_marker_maximum)



        self.line_segments.set_segments(self.Y_boundaries())# .set_data()
        self.ax.draw_artist(self.line_segments)




    def interpolation_line(self, X, Y):
        """
        Интерполяция по контрольным предоставляемым откуда угодно точкам в соответствии с выбранным методом интерполяции
        :param X:
        :param Y:
        :return:
        """
        ##### Добавь еще несколько видов интерполяции из другой библиотеки
        ##### Добавь еще несколько видов интерполяции из другой библиотеки
        ##### Добавь еще нескольков идов интерполяции из другой библиотеки

        yfit = np.linspace(min(Y), max(Y), num=25)

        try:
            for index in range(len(Y) - 1):
                if Y[index] + 0.05 >= Y[index + 1]:
                    raise ValueError

            if self.method_interpolate == "linear":
                pchip = interpolate.interp1d(Y, X, kind='linear')

            if self.method_interpolate == "CubicSpline":
                pchip = interpolate.CubicSpline(Y, X)

            if self.method_interpolate == "PchipInterpolator":
                pchip = interpolate.PchipInterpolator(Y, X)

            if self.method_interpolate == "Akima1DInterpolator":
                pchip = interpolate.Akima1DInterpolator(Y, X)

            if self.method_interpolate == "BarycentricInterpolator":
                pchip = interpolate.BarycentricInterpolator(Y, X)

            if self.method_interpolate == "KroghInterpolator":
                pchip = interpolate.KroghInterpolator(Y, X)

            if self.method_interpolate == "make_interp_spline":
                pchip = interpolate.make_interp_spline(Y, X)

            if self.method_interpolate == "nearest":
                pchip = interpolate.interp1d(Y, X,kind='nearest')

            if self.method_interpolate == "quadratic":
                pchip = interpolate.interp1d(Y, X, kind='quadratic')

            if self.method_interpolate == "cubic":
                pchip = interpolate.interp1d(Y, X, kind='cubic')

            if self.method_interpolate == "gaussian":
                new_f = interpolate.Rbf(Y, X, kind='gaussian')
                xnew = new_f(yfit)
                return xnew, yfit

            if self.method_interpolate == "multiquadric":
                new_f = interpolate.Rbf(Y, X, kind='multiquadric')
                xnew = new_f(yfit)
                return xnew, yfit

            if self.method_interpolate == "inverse":
                new_f = interpolate.Rbf(Y, X, kind='inverse')
                xnew = new_f(yfit)
                return xnew, yfit

            if self.method_interpolate == "cubic1":
                new_f = interpolate.Rbf(Y, X, kind='cubic')
                xnew = new_f(yfit)
                return xnew, yfit

            if self.method_interpolate == "quintic":
                new_f = interpolate.Rbf(Y, X, kind='quintic')
                xnew = new_f(yfit)
                return xnew, yfit

            if self.method_interpolate == "thin_plate":
                new_f = interpolate.Rbf(Y, X, kind='thin_plate')
                xnew = new_f(yfit)
                return xnew, yfit


        except:
            return
        xnew = pchip(yfit)

        return xnew, yfit

    @update_value_in_distibutor
    def add_point(self):

        self.limit_axe_X = max(self.point_values_X) + 0.05

        self.point_values_X.append(max(self.point_values_X) + 0.05)
        self.point_values_Y.append(self.limit_axe_Y)

        self.ax.set_xlim(0.1, self.limit_axe_X + 0.05)

        self.line.set_data(self.point_values_X, self.point_values_Y)

        self.line_minimum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_min, symbol='-'), self.point_values_Y)

        self.line_maximum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_max, symbol='+'), self.point_values_Y)

        self.canvas.draw_idle()

    @update_value_in_distibutor
    def delete_point(self, X, Y):
        self.point_values_X.pop(self.point_values_X.index(X))
        self.point_values_Y.pop(self.point_values_Y.index(Y))
        self.line_without_marker.set_data(self.interpolation_line(self.point_values_X, self.point_values_Y))

    @update_value_in_distibutor
    def choice_main_interpolation(self, new_method):
        """
        Изменение метода интерполяции всей линий (вызывается из GUI)
        :param new_method:
        :return:
        """
        self.method_interpolate = new_method


    @update_value_in_distibutor
    def reset(self, schema):

        distribut.data_load()

        distribut.data.update({"scheme_now": schema})

        self.schema = schema

        dct = distribut.data_give()

        self.point_values_X = dct.get(self.schema).get("point_values_X")
        self.point_values_Y = dct.get(self.schema).get("point_values_Y")
        ### Лимиты
        self.limit_axe_X = max(self.point_values_X) + 0.05
        self.limit_axe_Y = dct.get(self.schema).get("limit_axe_Y")
        ### Интерполяция
        self.method_interpolate = dct.get(self.schema).get("method_interpolate")
        ### Точки для дополнительных кривых
        self.last_save_values_X = dct.get(self.schema).get("last_save_values_X")
        self.last_save_values_Y = dct.get(self.schema).get("last_save_values_Y")

        ### Проценты с APP
        self.list_X_min = dct.get(self.schema).get("list_X_min")
        self.list_X_max = dct.get(self.schema).get("list_X_max")
        self.list_Y_min = dct.get(self.schema).get("list_Y_min")
        self.list_Y_max = dct.get(self.schema).get("list_Y_max")

        """
        Сброс точек в исходное состояние, которое контролируется последними сохраненными точками
        :return:
        """
        self.line.set_data(self.point_values_X, self.point_values_Y)
        self.line_minimum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_min, symbol='-'), self.point_values_Y)
        self.line_maximum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_max, symbol='+'), self.point_values_Y)

        self.line_segments.set_segments(self.Y_boundaries())

        self.limit_axe_X = max(self.point_values_X) + 0.05
        self.ax.set_xlim(0.1, self.limit_axe_X)

        self.canvas.draw_idle()


    def get_ind_under_point(self, event):
        """
        Return the index of the point closest to the event position or *None*
        if no point is within ``self.epsilon`` to the event position.
        """
        # display coords
        xy = np.asarray(self.line.get_xydata())
        xyt = self.line.get_transform().transform(xy)
        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.hypot(xt - event.x, yt - event.y)
        indseq, = np.nonzero(d == d.min())
        ind = indseq[0]
        if d[ind] >= self.epsilon:
            ind = None
        self._ind = ind
        return ind

    def on_button_press(self, event):
        """
        Действие при нажатой кнопке на графике
        :param event:
        :return:
        """
        if not self.showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)
        if self._ind:
            self.drag = True

    def on_button_release(self, event):
        """
        Действие при отжатии кнопки (остановка двжинеия точек на графике)
        :param event:
        :return:
        """
        if not self.showverts:
            return
        if event.button != 1:
            return
        self._ind = None

    @update_value_in_distibutor
    def on_mouse_move(self, event):
        """
        Предоставление координат и движение точек на графике при отсутствии ошибок
        :param event:
        :return:
        """
        self.position_mouse_X = event.xdata
        self.position_mouse_Y = event.ydata

        if self._ind in [0, 1, 2]:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        self.limit_axe_X = max(self.point_values_X) + 0.05

        # Точку максимального давления можно двигать только по оси Y
        if self._ind not in [self.point_values_X.index(max(self.point_values_X))]: # [3]:
            self.point_values_X[self._ind] = self.position_mouse_X
            self.point_values_Y[self._ind] = self.position_mouse_Y
        else:
            self.point_values_Y[self._ind] = self.position_mouse_Y

        self.line.set_data(self.point_values_X, self.point_values_Y)
        self.line_minimum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_min, symbol='-'), self.point_values_Y)
        self.line_maximum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_max, symbol='+'), self.point_values_Y)

        self.canvas.draw_idle()

        # Движение точки в координатах в GUI
        app.update_listbox()

    def install_max_Y_limit(self):
        """
        Устанавливает значения максимального Y и сдвигает точки по оси Y до лимита.
        :param event:
        :return:
        """
        self.limit_axe_Y = distribut.data.get(self.schema).get("limit_axe_Y")

        self.ax.set_ylim(0, self.limit_axe_Y)
        self.axes_y.invert_yaxis()

        self.update_max_Y_points()

        self.canvas.draw_idle()

    @update_value_in_distibutor
    def update_max_Y_points(self):
        """
        Изменяет положение точек с Y, который больше, чем лимит по оси Y
        :return:
        """
        for count, val in enumerate(self.point_values_Y, 0):
            self.point_values_Y[count] = (self.point_values_Y[count] if self.point_values_Y[count] < self.limit_axe_Y
                                          else self.limit_axe_Y)
        self.line_minimum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_min, symbol='-'), self.point_values_Y)
        self.line_maximum.set_data(self.calculate(AXES=self.point_values_X, percents=self.list_X_max, symbol='+'), self.point_values_Y)
        self.line.set_data(self.point_values_X, self.point_values_Y)


class Coordinats(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        """
        Инициализация окна для координат
        :param master:
        :param kwargs:
        """
        super().__init__(master, **kwargs)

        self.add("Координаты точек")

class ShowGraph(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        """
        Инициализация окна для графика
        :param master:
        :param kwargs:
        """
        super().__init__(master, **kwargs)

        self.add("График")

class App(customtkinter.CTk):
    def __init__(self, dct):
        super().__init__()

        ### Распаковка элементов
        self.schema = dct.get("scheme_now")
        ### Точки для основной кривой
        self.point_values_X = dct.get(self.schema).get("point_values_X")
        self.point_values_Y = dct.get(self.schema).get("point_values_Y")
        ### Лимиты
        self.limit_axe_X = max(self.point_values_X) + 0.05
        self.limit_axe_Y = dct.get(self.schema).get("limit_axe_Y")
        ### Интерполяция
        self.method_interpolate = dct.get(self.schema).get("method_interpolate")
        ### Точки для дополнительных кривых
        self.last_save_values_X = dct.get(self.schema).get("last_save_values_X")
        self.last_save_values_Y = dct.get(self.schema).get("last_save_values_Y")

        ### Проценты с APP
        self.list_X_min = dct.get(self.schema).get("list_X_min")
        self.list_X_max = dct.get(self.schema).get("list_X_max")
        self.list_Y_min = dct.get(self.schema).get("list_Y_min")
        self.list_Y_max = dct.get(self.schema).get("list_Y_max")

        self.x = 1500
        self.y = 900

        self.title("GeoF")
        self.geometry(f"{self.x}x{self.y}")

        ##### Все что идет в архивирование
        self.maximum_Y_point = tk.Variable(value=self.limit_axe_Y)

        self.interactive_graph = ShowGraph(master=self, command=self.update_listbox)
        self.interactive_graph.grid(sticky="NEWS")  # NEWS
        self.interactive_graph.grid_rowconfigure(0, weight=1)
        self.interactive_graph.grid_columnconfigure(0, weight=1)

        #######
        ####### Выгрузка точек
        self.coor_points = Coordinats(master=self)
        self.coor_points.grid(sticky="NEWS")  # NEWS
        self.coor_points.grid_rowconfigure(1, )
        self.coor_points.grid_columnconfigure(1, )

        #### Для изменения объекта
        self.item_lb = customtkinter.StringVar()
        self.choicing_item_lb = customtkinter.CTkEntry(master=self, textvariable=self.item_lb, width=20)
        self.choicing_item_lb.grid(row=2, column=0, ipadx=50)
        self.choicing_item_lb.bind('<Return>', self.update_select_value)

        ### Координаты X
        ### Координаты X
        ### Координаты X
        self.list_X = tk.Variable(value=self.point_values_X)

        self.list_X_min = tk.Variable(value=self.list_X_min)

        customtkinter.CTkLabel(master=self.coor_points.tab("Координаты точек"),
                               text="X_MIN", fg_color="transparent").grid(row=0, column=0, padx=20, pady=1)
        self.list_box_X_min = Listbox(master=self.coor_points.tab("Координаты точек"), listvariable=self.list_X_min,
                                      fg='black')
        self.list_box_X_min.grid(row=1, column=0, padx=20, pady=20)
        self.list_box_X_min.bind('<<ListboxSelect>>', self.select_value)

        customtkinter.CTkLabel(master=self.coor_points.tab("Координаты точек"),
                               text="X_NOW", fg_color="transparent").grid(row=0, column=1, padx=20, pady=1)
        self.list_box_X = Listbox(master=self.coor_points.tab("Координаты точек"), listvariable=self.list_X, fg='black')
        self.list_box_X.grid(row=1, column=1, padx=20, pady=20)

        self.list_X_max = tk.Variable(value=self.list_X_max)
        customtkinter.CTkLabel(master=self.coor_points.tab("Координаты точек"),
                               text="X_MAX", fg_color="transparent").grid(row=0, column=2, padx=20, pady=1)
        self.list_box_X_max = Listbox(master=self.coor_points.tab("Координаты точек"), listvariable=self.list_X_max,
                                      fg='black')
        self.list_box_X_max.grid(row=1, column=2, padx=20, pady=20)
        self.list_box_X_max.bind('<<ListboxSelect>>', self.select_value)

        ### Координаты Y
        ### Координаты Y
        ### Координаты Y
        self.list_Y = tk.Variable(value=self.point_values_Y)

        self.list_Y_min = tk.Variable(value=self.list_Y_min)

        customtkinter.CTkLabel(master=self.coor_points.tab("Координаты точек"),
                               text="Y_MIN", fg_color="transparent").grid(row=0, column=3, padx=20, pady=1)
        self.list_box_Y_min = Listbox(master=self.coor_points.tab("Координаты точек"), listvariable=self.list_Y_min,
                                      fg='black')
        self.list_box_Y_min.grid(row=1, column=3, padx=20, pady=20)
        self.list_box_Y_min.bind('<<ListboxSelect>>', self.select_value)

        customtkinter.CTkLabel(master=self.coor_points.tab("Координаты точек"),
                               text="Y_NOW", fg_color="transparent").grid(row=0, column=4, padx=20, pady=1)
        self.list_box_Y = Listbox(master=self.coor_points.tab("Координаты точек"), listvariable=self.list_Y, fg='black')
        self.list_box_Y.grid(row=1, column=4, padx=20, pady=20)

        ### Регулировка по оси Y
        ### Регулировка по оси Y
        ### Регулировка по оси Y
        self.list_Y_max = tk.Variable(value=self.list_Y_max)
        customtkinter.CTkLabel(master=self.coor_points.tab("Координаты точек"),
                               text="Y_MAX", fg_color="transparent").grid(row=0, column=5, padx=20, pady=1)
        self.list_box_Y_max = Listbox(master=self.coor_points.tab("Координаты точек"), listvariable=self.list_Y_max,
                                      fg='black')
        self.list_box_Y_max.grid(row=1, column=5, padx=20, pady=20)
        self.list_box_Y_max.bind('<<ListboxSelect>>', self.select_value)

        # Сбросить точки
        self.button_RESET = customtkinter.CTkButton(master=self, text="RESET", command=self.reset_points)
        self.button_RESET.grid(row=0, column=1, padx=20, pady=20, sticky='N')

        # Добавление точки
        self.button_ADD_POINT = customtkinter.CTkButton(master=self, text="ADD", command=self.add_point)
        self.button_ADD_POINT.grid(row=0, column=1, padx=20, pady=60, sticky='N')

        # Выбор метода интерполяции
        self.main_interp = customtkinter.StringVar(value='PchipInterpolator')
        self.method_interpolation = customtkinter.CTkOptionMenu(master=self,
                                                                values=["linear", "CubicSpline", "PchipInterpolator",
                                                                        "Akima1DInterpolator",
                                                                        "BarycentricInterpolator",
                                                                        "KroghInterpolator", "make_interp_spline",
                                                                        "nearest", "quadratic", "cubic", "gaussian",
                                                                        "multiquadric", "inverse", "cubic1", "quintic",
                                                                        "thin_plate",
                                                                        ],
                                                                command=self.change_interpolation,
                                                                variable=self.main_interp,
                                                                )
        self.method_interpolation.grid(row=0, column=1, padx=20, pady=100, sticky='N')

        # Регулировка оси Y
        customtkinter.CTkLabel(master=self, text="Введите максимальный Y").grid(row=0, column=2, padx=20, pady=140,
                                                                                sticky='N')
        self.maximum_Y_ENTRY = tk.Entry(master=self,
                                        textvariable=self.maximum_Y_point,
                                        )
        self.maximum_Y_ENTRY.grid(row=0, column=1, padx=20, pady=140, sticky='N')
        self.maximum_Y_ENTRY.bind('<Return>', self.update_limit_Y)

        # Выбор сохраненной схемы
        # Выбор сохраненной схемы
        # Выбор сохраненной схемы
        self.scheme_now = customtkinter.StringVar(value=distribut.data.get("scheme_now"))
        self.schemes_choice = customtkinter.CTkOptionMenu(master=self,
                                                          values=[schem for schem in distribut.data.keys() if
                                                                  schem not in ["scheme_now"]],
                                                          command=self.change_scheme,
                                                          variable=self.scheme_now,
                                                          )
        self.schemes_choice.grid(row=0, column=1, padx=20, pady=180, sticky='N')
        self.schemes_choice.bind('<ButtonRelease>', self.change_scheme)

        # Кнопка сохранения схемы графика
        self.save_graph = customtkinter.CTkButton(master=self, text="SAVE_SCHEMA", command=self.save_graph_on_json)
        self.save_graph.grid(row=0, column=1, padx=20, pady=220, sticky='N')

        # Добавить новую схему
        customtkinter.CTkLabel(master=self, text="Добавьте схему").grid(row=0, column=2, padx=20, pady=260,
                                                                                sticky='N')
        self.name_new_schema = customtkinter.CTkEntry(master=self)
        self.name_new_schema.grid(row=0, column=1, padx=20, pady=260, sticky='N')
        self.name_new_schema.bind('<Return>', self.add_new_scheme_to_distributor)


    def add_new_scheme_to_distributor(self, event):

        distribut.add_new_schema(self.name_new_schema.get())

        distribut.data_save()

        self.schemes_choice.configure(values=[schem for schem in distribut.data.keys() if schem not in ["scheme_now"]])

        self.name_new_schema.configure(textvariable="")

    def change_scheme(self, event):
        new_schema = self.scheme_now.get()
        distribut.data.update({"scheme_now": new_schema})

        self.schema = self.scheme_now.get()
        print(self.schema)

        self.limit_axe_Y = distribut.data.get(self.schema).get("limit_axe_Y")
        self.maximum_Y_point.set(value=self.limit_axe_Y)
        self.maximum_Y_ENTRY.configure(textvariable=self.maximum_Y_point)


        self.reset_points()

    def update_limit_Y(self, event):

        self.limit_axe_Y = float(self.maximum_Y_point.get())

        distribut.data.get(self.schema).update({"limit_axe_Y": self.limit_axe_Y})

        p.install_max_Y_limit()

    def updating_scheme_update_graph(self):

        distribut.data_update(self.scheme_now.get(),
        {
            "list_X_min": list(self.list_box_X_min.get(0, len(p.point_values_X))[:]),
            "list_X_max": list(self.list_box_X_max.get(0, len(p.point_values_X))[:]),
            "list_Y_min": list(self.list_box_Y_min.get(0, len(p.point_values_X))[:]),
            "list_Y_max": list(self.list_box_Y_max.get(0, len(p.point_values_X))[:]),
        })

    def save_graph_on_json(self):

        distribut.data_save()

    def select_value(self, event):
        """
        Позволяет выбирать значения и обновлять строку с выбранным полем ниже значения координат и процнетов отступа
        :param event:
        :return:
        """

        try:
            if event.widget._name == '!listbox':
                self.index_lb = self.list_box_X_min.curselection()[0]
                self.item_lb.set(self.list_box_X_min.get(0, len(p.point_values_X))[self.index_lb])
        except IndexError:
            return
        try:
            if event.widget._name == '!listbox3':
                self.index_lb = self.list_box_X_max.curselection()[0]
                self.item_lb.set(self.list_box_X_max.get(0, len(p.point_values_X))[self.index_lb])
        except IndexError:
            return
        try:
            if event.widget._name == '!listbox4':
                self.index_lb = self.list_box_Y_min.curselection()[0]
                self.item_lb.set(self.list_box_Y_min.get(0, len(p.point_values_X))[self.index_lb])
        except IndexError:
            return

        try:
            if event.widget._name == '!listbox6':
                self.index_lb = self.list_box_Y_max.curselection()[0]
                self.item_lb.set(self.list_box_Y_max.get(0, len(p.point_values_X))[self.index_lb])
        except IndexError:
            return

        self.name_lb = event.widget._name

        self.updating_scheme_update_graph()

        p.instant_update_lines()


    def update_select_value(self, event):
        """
        Позволяет обновлять значения процентов в листбоксах минимальных и максимальных значений по Y

        А также значения линий при помощи функции instant_update_lines
        :param event:
        :return:
        """
        if self.index_lb in [0, 1, 2, 3] and self.name_lb not in ('!listbox4', '!listbox6'):
            return

        if self.name_lb == '!listbox':
            values_now_X_min = list(self.list_X_min.get())
            values_now_X_min[self.index_lb] = float(self.item_lb.get())
            self.list_X_min = tk.Variable(value=values_now_X_min)
            self.list_box_X_min.configure(listvariable=self.list_X_min)

        if self.name_lb == '!listbox3':
            values_now_X_max = list(self.list_X_max.get())
            values_now_X_max[self.index_lb] = float(self.item_lb.get())
            self.list_X_max = tk.Variable(value=values_now_X_max)
            self.list_box_X_max.configure(listvariable=self.list_X_max)

        if self.name_lb == '!listbox4':
            values_now_Y_min = list(self.list_Y_min.get())
            values_now_Y_min[self.index_lb] = float(self.item_lb.get())
            self.list_Y_min = tk.Variable(value=values_now_Y_min)
            self.list_box_Y_min.configure(listvariable=self.list_Y_min)

        if self.name_lb == '!listbox6':
            values_now_Y_max = list(self.list_Y_max.get())
            values_now_Y_max[self.index_lb] = float(self.item_lb.get())
            self.list_Y_max = tk.Variable(value=values_now_Y_max)
            self.list_box_Y_max.configure(listvariable=self.list_Y_max)

        self.updating_scheme_update_graph()

        p.instant_update_lines()


    def update_listbox(self):
        """
        Обновляет листбоксы на основе изменения в графике

        А также значения линий при помощи функции instant_update_lines
        :return:
        """
        ### Для координат в реальном времени
        self.list_X.set(value=distribut.data.get(self.schema).get("point_values_X"))
        self.list_Y.set(value=distribut.data.get(self.schema).get("point_values_Y"))
        self.list_box_X.configure(listvariable=self.list_X)
        self.list_box_Y.configure(listvariable=self.list_Y)
        values_now_X_min = distribut.data.get(self.schema).get("list_X_min")
        values_now_X_max = distribut.data.get(self.schema).get("list_X_max")
        values_now_Y_min = distribut.data.get(self.schema).get("list_Y_min")
        values_now_Y_max = distribut.data.get(self.schema).get("list_Y_max")

        ### Для контроля процентов
        for x in range(abs(len(values_now_X_min) - len(self.list_X.get()))):
            if len(values_now_X_min) < len(self.list_X.get()):
                values_now_X_min.append(0)
            if len(values_now_X_min) > len(self.list_X.get()):
                values_now_X_min.pop()
        self.list_X_min.set(value=values_now_X_min)
        self.list_X_min.set(values_now_X_min)
        self.list_box_X_min.configure(listvariable=self.list_X_min)

        for x in range(abs(len(values_now_X_max) - len(self.list_X.get()))):
            if len(values_now_X_max) < len(self.list_X.get()):
                values_now_X_max.append(0)
            if len(values_now_X_max) > len(self.list_X.get()):
                values_now_X_max.pop()
        self.list_X_max.set(value=values_now_X_max)
        self.list_box_X_max.configure(listvariable=self.list_X_max)

        for x in range(abs(len(values_now_Y_min) - len(self.list_Y.get()))):
            if len(values_now_Y_min) < len(self.list_Y.get()):
                values_now_Y_min.append(0)
            if len(values_now_Y_min) > len(self.list_Y.get()):
                values_now_Y_min.pop()
        self.list_Y_min.set(value=values_now_Y_min)
        self.list_box_Y_min.configure(listvariable=self.list_Y_min)

        for x in range(abs(len(values_now_Y_max) - len(self.list_Y.get()))):
            if len(values_now_Y_max) < len(self.list_Y.get()):
                values_now_Y_max.append(0)
            if len(values_now_Y_max) > len(self.list_Y.get()):
                values_now_Y_max.pop()
        self.list_Y_max.set(value=values_now_Y_max)
        self.list_box_Y_max.configure(listvariable=self.list_Y_max)

        p.instant_update_lines()


    def add_point(self):
        """
        Добавляет точку на график и обновляет его линии, а также листбоксы в GUI

        Обновляет также значения линий при помощи функции instant_update_lines
        :return:
        """
        p.add_point()

        self.update_listbox()

        self.updating_scheme_update_graph()

        p.instant_update_lines()

    def reset_points(self):
        """
        Сбрасывает точки до первоначального состояния

        Обновляет также значения линий при помощи функции instant_update_lines
        :return:
        """
        p.reset(self.schema)

        self.update_listbox()

        self.update_limit_Y(True)

        p.instant_update_lines()

    def change_interpolation(self, choice):
        """
        Изменение метода интерполяции всех линий на графике

        Обновляет также значения линий при помощи функции instant_update_lines1
        :param choice:
        :return:
        """
        self.updating_scheme_update_graph()

        p.choice_main_interpolation(choice)

        p.instant_update_lines()

"""
Требования:

##### Первостепенные

Добавить легенду к кривым линиям на сам график

Почистить код

Добавить функционал по удалению схем

Добавить функционал по распределению схем по типам грунта

Определиться с видом прочности (привести в единый вид с деформацией -- или сделать отдельный от деформации

Продумать дополнительные функции настройки графиков

Кривые консолидации



##### Требуется уточнение и обсуждение путей решения проблем

К0 должен быть полностью расчетный, но что делать с давлением после К0 менее 50 КПа

Опираемся на ГОСТ в плане расчетов противодавления и К0

Будет ли идти к протоколу для определенных по ГОСТу типов грунта -- протокол OCR



##### Второстепенные

Подумать о введении в действие перпендикуляров точек по осям, чтобы было наиболее наглядно.

Подумать о введенении в действие отображения графика по оси Y

Разобраться с ошибкой получения неправильных данных процентов при пути ЛИСТБОКС -- РАСПРЕДЕЛИТЕЛЬ -- ГРАФИК

Добавить логирование для отслеживания пути кода

Рассмотреть возможность добавления глобальной переменной класса которая будет являться объектом который хватает
в себя прописанный лог того, что происходит в программе (рукописный лог на основе функций)

Возможно можно добавить больше декораторов, которые являются обновляющими значения или перехватывающими логи и тд

Разобраться в дескрипторах

Рассмотреть возможность использования сеттеров и геттеров

Посмотреть паттерны проектирования
"""

fig, ax = plt.subplots()

p = Graph(ax, distribut.data)

app = App(distribut.data)
p.canvas = FigureCanvasTkAgg(plt.gcf(), master=app.interactive_graph.tab("График"))
p.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
app.mainloop()
