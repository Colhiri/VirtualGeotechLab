import random
import sys

import numpy as np
from scipy import interpolate

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (CheckboxButtonGroup, CustomJS, IntEditor, TextInput, Button, ColumnDataSource, PointDrawTool, Select, TableColumn, DataTable, NumberFormatter)
from bokeh.plotting import figure

from DataDistributor_DB import DataDitributor as DD

class Graph_traxial:
    def __init__(self, dct: dict):
        self.global_schema = 'traxial'

        ### Распаковка элементов
        self.schema = dct.get(f"{self.global_schema}_scheme_now")
        ### Точки для основной кривой
        self.point_values_X = dct.get(self.global_schema).get(self.schema).get("point_values_X")
        self.point_values_Y = [y / 76 for y in dct.get(self.global_schema).get(self.schema).get("point_values_Y")]
        self.limit_axe_X = max(self.point_values_X) + 0.05
        self.limit_axe_Y = dct.get(self.global_schema).get(self.schema).get("limit_axe_Y")
        self.method_interpolate = dct.get(self.global_schema).get(self.schema).get("method_interpolate")
        self.list_X_min = dct.get(self.global_schema).get(self.schema).get("list_X_min")
        self.list_X_max = dct.get(self.global_schema).get(self.schema).get("list_X_max")
        self.list_Y_min = dct.get(self.global_schema).get(self.schema).get("list_Y_min")
        self.list_Y_max = dct.get(self.global_schema).get(self.schema).get("list_Y_max")
        self.count_points_min = str(dct.get(self.global_schema).get(self.schema).get("count_points_min"))
        self.count_points_max = str(dct.get(self.global_schema).get(self.schema).get("count_points_max"))
        self.random_percent_min = str(dct.get(self.global_schema).get(self.schema).get("random_percent_min"))
        self.random_percent_max = str(dct.get(self.global_schema).get(self.schema).get("random_percent_max"))

        """
        Объем
        """
        self.multiple_value = 1

        for volume_perc, traxial_perc in zip(dct.get('volume_traxial').get(self.schema).get("list_X_min"), self.list_X_min):
            if volume_perc != traxial_perc:
                self.multiple_value = volume_perc / traxial_perc

        self.multiple_volume = TextInput(title="Set increase percent multiple", value=str(self.multiple_value))

        self.points_volume_X = dct.get('volume_traxial').get(self.schema).get("point_values_X")
        self.limit_volume_axe_X = max(self.points_volume_X) + 0.05
        self.volume_method_interpolate = dct.get('volume_traxial').get(self.schema).get("method_interpolate")
        self.plot_volume = figure(width=1000, height=1000, x_range=(0, self.limit_axe_Y / 76))
        self.plot_volume.x_range.start = 0
        self.plot_volume.x_range.end = 0.2
        self.volume_mid_line_values = ColumnDataSource(data=dict(x=self.points_volume_X, y=self.point_values_Y), )
        # Интерполяция точек по основной линии
        self.volume_mid_line_interpolate_values = ColumnDataSource(
            data=dict(self.volume_interpolation_line(self.volume_mid_line_values.data['x'],
                                              self.volume_mid_line_values.data['y'])), )
        # Отображение точек на графике
        self.volume_glyph = self.plot_volume.circle('y', 'x', size=10, color='blue', alpha=0.5, source=self.volume_mid_line_values)

        # Создание инструмента для перемещения точек
        self.draw_tool_volume = PointDrawTool(renderers=[self.volume_glyph], empty_value='black')
        self.plot_volume.add_tools(self.draw_tool_volume)

        # Отображение точек
        self.plot_volume.line(x='y', y='x', line_color='green', line_width=1, source=self.volume_mid_line_interpolate_values,
                       legend_label='Mid values')
        self.plot_volume.legend.orientation = "vertical"
        self.plot_volume.legend.location = "top_right"

        # Вспомогательная минимальная линия по оси Х
        self.volume_min_line_values = ColumnDataSource(
            data=dict(x=[AX * ((100 - perc) / 100) for AX, perc in
                         zip(self.volume_mid_line_values.data['x'], self.list_X_min)],
                      y=self.volume_mid_line_values.data['y']), )
        self.volume_max_line_values = ColumnDataSource(
            data=dict(x=[AX * ((100 + perc) / 100) for AX, perc in
                         zip(self.volume_mid_line_values.data['x'], self.list_X_max)],
                      y=self.volume_mid_line_values.data['y']), )
        self.volume_min_line_interpolate_values = ColumnDataSource(
            data=dict(self.volume_interpolation_line(self.volume_min_line_values.data['x'],
                                              self.volume_min_line_values.data['y'])))
        self.volume_max_line_interpolate_values = ColumnDataSource(
            data=dict(self.volume_interpolation_line(self.volume_max_line_values.data['x'],
                                              self.volume_max_line_values.data['y'])))
        self.plot_volume.line(x='y', y='x', line_color='blue', line_width=1, source=self.volume_min_line_interpolate_values,
                       legend_label='Min value')
        self.plot_volume.line(x='y', y='x', line_color='red', line_width=1, source=self.volume_max_line_interpolate_values,
                       legend_label='Max value')


        """
        Давление
        """
        ### Инициализация графика и графических утилит
        self.plot = figure(width=1000, height=1000, y_range=(self.limit_axe_Y / 76, 0))
        self.plot.y_range.start = 0.2
        self.plot.y_range.end = 0
        ### Создание значений для линий
        # Основная линия
        self.mid_line_values = ColumnDataSource(data=dict(x=self.point_values_X, y=self.point_values_Y),)
        # Интерполяция точек по основной линии
        self.mid_line_interpolate_values = ColumnDataSource(data=dict(self.interpolation_line(self.mid_line_values.data['x'],
                                                                                              self.mid_line_values.data['y'])), )

        # Вспомогательная минимальная линия по оси Х
        self.min_line_values = ColumnDataSource(
            data=dict(x=[AX * ((100 - perc) / 100) for AX, perc in
                         zip(self.mid_line_values.data['x'], self.list_X_min)],
                      y=self.mid_line_values.data['y']), )
        self.max_line_values = ColumnDataSource(
            data=dict(x=[AX * ((100 + perc) / 100) for AX, perc in
                         zip(self.mid_line_values.data['x'], self.list_X_max)],
                      y=self.mid_line_values.data['y']), )
        self.min_line_interpolate_values = ColumnDataSource(
            data=dict(self.interpolation_line(self.min_line_values.data['x'],
                                              self.min_line_values.data['y'])))
        self.max_line_interpolate_values = ColumnDataSource(
            data=dict(self.interpolation_line(self.max_line_values.data['x'],
                                              self.max_line_values.data['y'])))

        # Создание таблицы со значениями линий
        self.table_values = ColumnDataSource(dict(x=self.mid_line_values.data['x'], y=self.mid_line_values.data['y'],))

        self.columns_table = [
            TableColumn(field="x", title="X", formatter=NumberFormatter(format="0.00"), editor=IntEditor()),
            TableColumn(field="y", title="Y", formatter=NumberFormatter(format="0.00"), editor=IntEditor()),
        ]
        self.data_table = DataTable(source=self.table_values, columns=self.columns_table, editable=True,
                                    selectable=False, width=800,
                               index_position=-1, index_header="row index", index_width=60)

        self.table_values_perc = ColumnDataSource(dict(x=self.point_values_X, y=self.point_values_Y,
                                                  x_min=self.list_X_min, x_max=self.list_X_max,
                                                  y_min=self.list_Y_min, y_max=self.list_Y_max))
        self.columns_table_perc = [
            TableColumn(field="x_min", title="X MIN", formatter=NumberFormatter(format="0"), editor=IntEditor()),
            TableColumn(field="x_max", title="X MAX", formatter=NumberFormatter(format="0"), editor=IntEditor()),
            TableColumn(field="y_min", title="Y MIN", formatter=NumberFormatter(format="0"), editor=IntEditor()),
            TableColumn(field="y_max", title="Y MAX", formatter=NumberFormatter(format="0"), editor=IntEditor()),
        ]
        self.data_table_perc = DataTable(source=self.table_values_perc, columns=self.columns_table_perc, editable=True,
                                    selectable=True, width=800,
                                    index_position=-1, index_header="row index", index_width=60)

        self.y_max_min_values = ColumnDataSource(dict(xs=self.Y_boundaries()[0],
                                                      ys=self.Y_boundaries()[1]))
        self.calculate()

        # Отображение точек на графике
        self.glyph = self.plot.circle('x', 'y', size=10, color='blue', alpha=0.5, source=self.mid_line_values)

        # Создание инструмента для перемещения точек
        self.draw_tool = PointDrawTool(renderers=[self.glyph], empty_value='black')
        self.plot.add_tools(self.draw_tool)

        # Отображение точек
        self.plot.line(x='x', y='y', line_color='green', line_width=1, source=self.mid_line_interpolate_values,
                       legend_label='Mid values')
        self.plot.line(x='x', y='y', line_color='blue', line_width=1, source=self.min_line_interpolate_values,
                       legend_label='Min value')
        self.plot.line(x='x', y='y', line_color='red', line_width=1, source=self.max_line_interpolate_values,
                       legend_label='Max value')
        self.plot.multi_line(xs="xs", ys="ys", line_color="#8073ac", line_width=2, source=self.y_max_min_values)
        self.plot.legend.orientation = "vertical"
        self.plot.legend.location = "top_right"

        # Текстовое поле для того, чтобы написать количество точек и рандом
        self.count_points_min_text = TextInput(title="Set count point min", value=self.count_points_min)
        self.count_points_max_text = TextInput(title="Set count point min", value=self.count_points_max)
        self.random_percent_min_text = TextInput(title="Set random min", value=self.random_percent_min)
        self.random_percent_max_text = TextInput(title="Set random max", value=self.random_percent_max)


        # Кнопка для применения параметров количества точек и рандома
        self.button_update_point_random = Button(label="Update", button_type='success', height=40)
        self.button_update_point_random.on_click(self.update_percents)


        self.random_activate = CheckboxButtonGroup(labels=['Random ON/OFF'], active=[0, 1], button_type='warning')
        self.random_activate.js_on_event("button_click", CustomJS(args=dict(btn=self.random_activate), code="""
            console.log('checkbox_button_group: active=' + btn.active, this.toString())
        """))

        # Текстовое поле для того, чтобы написать имя новой схемы
        self.name_new_shema = TextInput(title="Name new schema", value="")

        # Кнопка для добавления схемы
        self.button_add_schema = Button(label="Add schema", button_type='success', height=40)
        self.button_add_schema.on_click(self.add_new_schema)

        # Кнопка для удаления схемы
        self.button_delete_schema = Button(label="Delete schema", button_type='success', height=40)
        self.button_delete_schema.on_click(self.delete_schema)

        # Кнопка для сохранения схемы
        self.button_save_schema = Button(label="Save schema", button_type='success', height=40)
        self.button_save_schema.on_click(self.save_schema)

        # Кнопка для сброса схемы
        self.button_reset_schema = Button(label="Reset schema", button_type='success', height=40)
        self.button_reset_schema.on_click(self.reset_schema)

        # Список интерполяций
        self.interpolation_methods = ["linear", "CubicSpline", "PchipInterpolator", "Akima1DInterpolator",
                                      "BarycentricInterpolator", "KroghInterpolator", "make_interp_spline",
                                      "nearest", "quadratic", "cubic"]
        self.interpolation_select = Select(title='Interpolation Method Press',
                                           value=distribut.data.get(self.global_schema).get(self.schema).get("method_interpolate"),
                                           options=self.interpolation_methods)

        self.volume_interpolation_select = Select(title='Interpolation Method Volume',
                                           value=distribut.data.get('volume_traxial').get(self.schema).get(
                                               "method_interpolate"),
                                           options=self.interpolation_methods)

        # Список схем
        self.schemas = [schem for schem in distribut.data.get(self.global_schema).keys() if
                        schem not in [f"{self.global_schema}_scheme_now"]]

        self.schema_select = Select(title='Choice schema',
                                    value=distribut.data.get(f"{self.global_schema}_scheme_now"),
                                    options=self.schemas)

    def update_percents(self):
        """
        Обновление значений исходя из значений в текстовых полях
        :return:
        """
        self.count_points_min = int(self.count_points_min_text.value)
        self.count_points_max = int(self.count_points_max_text.value)
        self.random_percent_min = float(self.random_percent_min_text.value)
        self.random_percent_max = float(self.random_percent_max_text.value)
        self.multiple_value = float(self.multiple_volume.value)

        if isinstance(self.count_points_min, tuple):
            self.count_points_min = self.count_points_min[0]
        if isinstance(self.count_points_max, tuple):
            self.count_points_max = self.count_points_max[0]
        if isinstance(self.random_percent_min, tuple):
            self.random_percent_min = self.random_percent_min[0]
        if isinstance(self.random_percent_max, tuple):
            self.random_percent_max = self.random_percent_max[0]
        if isinstance(self.multiple_value, tuple):
            self.multiple_value = self.multiple_value[0]

        self.count_points_min_text.value = str(self.count_points_min)
        self.count_points_max_text.value = str(self.count_points_max)
        self.random_percent_min_text.value = str(self.random_percent_min)
        self.random_percent_max_text.value = str(self.random_percent_max)
        self.multiple_volume.value = str(self.multiple_value)

    def random_percent(self):
        """
        Функция рандомного процента
        :return:
        """
        perc_min = int((100 - float(self.random_percent_min)) * 100)
        perc_max = int((100 + float(self.random_percent_max)) * 100)
        return random.randint(perc_min, perc_max) / 10000

    def update_random_and_count_point(self, value):
        """
        Функция обновления определенной линии графика
        :param value:
        :return:
        """
        points_x, points_y = value['x'], value['y']
        if self.random_activate.active == [1]:
            points_x = [self.random_percent() * x_value for x_value in points_x]
        return {'x': points_x, 'y': points_y}

    def reset_schema(self):
        """
        Сбрасывает схему до последнего сохраненного чекпоинта на локалке в json
        :return:
        """
        self.schema_select_handler(True, True, self.schema)

    def Y_boundaries(self):
        """
        Пересчитывает границы полилинии в процентах отхождения по оси Y
        :return: Значения для всех точек графика по двум точкам
        """
        segs_x = []
        segs_y = []
        for index in range(len(self.mid_line_values.data['y'])):
            value_x = [self.mid_line_values.data['x'][index], self.mid_line_values.data['x'][index]]
            value_y = [self.mid_line_values.data['y'][index] * ((100 + self.table_values_perc.data['y_max'][index]) / 100),
                       self.mid_line_values.data['y'][index] * ((100 - self.table_values_perc.data['y_min'][index]) / 100)
                       ]
            segs_x.append(value_x)
            segs_y.append(value_y)

        return (segs_x, segs_y)

    def add_new_schema(self):
        """
        Добавляет новую схему
        :return:
        """
        distribut.add_new_schema_in_dct(self.name_new_shema.value, self.global_schema)
        self.schema_select.options = [schem for schem in distribut.data.get(self.global_schema).keys() if
                                      schem not in [f"{self.global_schema}_scheme_now"]]

    def delete_schema(self):
        """
        Удаляет открытую в данный момент схему
        :return:
        """
        distribut.delete_schema_in_dct(self.schema_select.value, self.global_schema)
        self.schema_select.options = [schem for schem in distribut.data.get(self.global_schema).keys() if
                                      schem not in [f"{self.global_schema}_scheme_now"]]
        self.schema = self.schema_select.options[0]
        self.schema_select.value = self.schema_select.options[0]
        distribut.data.get(self.global_schema)[f'{self.global_schema}_scheme_now'] = self.schema
        distribut.data.get('volume_traxial')['volume_traxial_scheme_now'] = self.schema
        self.schema_select_handler(True, True, self.schema_select.options[0])

    def save_schema(self):
        """
        Переопределить для другого класса
        :return:
        """
        distribut.data.get(self.global_schema)[self.schema] = {
                                  "method_interpolate": self.method_interpolate,
                                  "limit_axe_X": self.limit_axe_X,
                                  "limit_axe_Y": max(self.point_values_Y),

                                  "point_values_X": self.point_values_X,
                                  "point_values_Y": [y * 76 for y in self.point_values_Y],

                                  "list_X_min": self.list_X_min,
                                  "list_X_max": self.list_X_max,
                                  "list_Y_min": self.list_Y_min,
                                  "list_Y_max": self.list_Y_max,

                                  "count_points_min": int(self.count_points_min_text.value),
                                  "count_points_max": int(self.count_points_max_text.value),
                                  "random_percent_min": float(self.random_percent_min_text.value),
                                  "random_percent_max": float(self.random_percent_max_text.value),
                                                    }
        if self.global_schema in ['traxial']:
            distribut.data.get('volume_traxial').get(self.schema).update({

                                      "method_interpolate": self.volume_method_interpolate,

                                      "point_values_X": self.points_volume_X,
                                      "point_values_Y": [y * 76 for y in self.point_values_Y],

                                      "limit_axe_X": max(self.point_values_X),
                                      "limit_axe_Y": max(self.point_values_Y),

                                      "list_X_min": [perc * self.multiple_value for perc in self.list_X_min],
                                      "list_X_max": [perc * self.multiple_value for perc in self.list_X_max],
                                      "list_Y_min": [perc * self.multiple_value for perc in self.list_Y_min],
                                      "list_Y_max": [perc * self.multiple_value for perc in self.list_Y_max],

                                      "count_points_min": int(self.count_points_min_text.value),
                                      "count_points_max": int(self.count_points_max_text.value),
                                      "random_percent_min": float(self.random_percent_min_text.value),
                                      "random_percent_max": float(self.random_percent_max_text.value),
                                                                          })
        distribut.write_data_in_database()

    # Обработчик события нажатия кнопки добавления точки
    def add_point_handler(self, event):
        """
        Добавляет точку на график
        :param event:
        :return:
        """
        x = event.x
        y = event.y

        self.mid_line_values.data['x'].append(x)
        self.mid_line_values.data['y'].append(y)

        self.update_plot()

    def volume_add_point_handler(self, event):
        pass

    def delete_handler(self):
        """
        Удаляет точку исходя из сравнения индекcов между точками в обновленной средней линии и точками оси X, которые еще не обновлены
        :return:
        """
        _index = None
        if len(self.mid_line_values.data['x']) == len(self.point_values_X):
            return
        # Получаем координаты удаленной точки
        for x_new, x_old in zip(self.mid_line_values.data['x'], self.point_values_X):
            if x_new != x_old:
                _index = self.mid_line_values.data['x'].index(x_new) + 1

        if len(self.mid_line_values.data['x']) != len(self.point_values_X):
            _index = -1

        if not _index:
            return

        self.list_X_min.pop(_index)
        self.list_X_max.pop(_index)
        self.list_Y_min.pop(_index)
        self.list_Y_max.pop(_index)

        self.point_values_X = self.mid_line_values.data['x']
        self.point_values_Y = self.mid_line_values.data['y']

        new_data = {
            'x': self.point_values_X,
            'y': self.point_values_Y,
            'x_min': self.list_X_min,
            'x_max': self.list_X_max,
            'y_min': self.list_Y_min,
            'y_max': self.list_Y_max,
        }
        self.table_values_perc.data = new_data

        _index = None

        self.update_plot()

    def volume_move_point_handler(self, event):
        """
        Двигаем выбранную точку на графике
        :param event:
        :return:
        """
        # Сделай обработку точек, которые нельзя изменять
        self.mid_line_values.data = dict(x=self.mid_line_values.data['x'], y=event.y)

        self.volume_mid_line_values.data = dict(x=self.volume_mid_line_values.data['x'], y=event.y)

        self.update_plot()

    def move_point_handler(self, event):
        """
        Двигаем выбранную точку на графике
        :param event:
        :return:
        """
        print(event.x)
        # Сделай обработку точек, которые нельзя изменять
        self.mid_line_values.data = dict(x=event.x, y=event.y)

        self.volume_mid_line_values.data = dict(x=self.volume_mid_line_values.data['y'], y=event.y)

        self.update_plot()

    def interpolation_select_handler(self, attr, old, new):
        """
        Выбор методы интерполяции в выпадающем списке
        :param attr:
        :param old:
        :param new:
        :return:
        """
        self.interpolation_select.value = new
        self.method_interpolate = new
        self.update_plot()

    def volume_interpolation_select_handler(self, attr, old, new):
        """
        Выбор методы интерполяции в выпадающем списке
        :param attr:
        :param old:
        :param new:
        :return:
        """
        self.volume_interpolation_select.value = new
        self.volume_method_interpolate = new
        self.update_plot()

    def schema_select_handler(self, attr, old, new):
        """
        Выбор схемы, ее загрузка, и отображение
        :param attr:
        :param old:
        :param new:
        :return:
        """

        self.schema = new

        distribut.data.update({f"{self.global_schema}_scheme_now": self.schema})
        if self.global_schema in ['traxial']:
            distribut.data.update({"volume_traxial_scheme_now": self.schema})

        dct = distribut.data_give()

        ### Распаковка элементов
        ### Основная линия
        ### Основная линия
        ### Основная линия
        self.point_values_X = dct.get(self.global_schema).get(self.schema).get("point_values_X")
        self.point_values_Y = [y / 76 for y in dct.get(self.global_schema).get(self.schema).get("point_values_Y")]
        self.limit_axe_X = max(self.point_values_X) + 0.05
        self.limit_axe_Y = dct.get(self.global_schema).get(self.schema).get("limit_axe_Y")
        self.method_interpolate = dct.get(self.global_schema).get(self.schema).get("method_interpolate")
        self.list_X_min = dct.get(self.global_schema).get(self.schema).get("list_X_min")
        self.list_X_max = dct.get(self.global_schema).get(self.schema).get("list_X_max")
        self.list_Y_min = dct.get(self.global_schema).get(self.schema).get("list_Y_min")
        self.list_Y_max = dct.get(self.global_schema).get(self.schema).get("list_Y_max")
        self.count_points_min = str(dct.get(self.global_schema).get(self.schema).get("count_points_min"))
        self.count_points_max = str(dct.get(self.global_schema).get(self.schema).get("count_points_max"))
        self.random_percent_min = str(dct.get(self.global_schema).get(self.schema).get("random_percent_min"))
        self.random_percent_max = str(dct.get(self.global_schema).get(self.schema).get("random_percent_max"))

        self.count_points_min_text.value = self.count_points_min
        self.count_points_max_text.value = self.count_points_max
        self.random_percent_min_text.value = self.random_percent_min
        self.random_percent_max_text.value = self.random_percent_max

        self.mid_line_values.data = dict(x=self.point_values_X, y=self.point_values_Y)

        self.table_values.data = dict(x=self.mid_line_values.data['x'], y=self.mid_line_values.data['y'],)

        self.table_values_perc.data = dict(x=self.point_values_X, y=self.point_values_Y,
                                            x_min=self.list_X_min, x_max=self.list_X_max,
                                            y_min=self.list_Y_min, y_max=self.list_Y_max)

        self.interpolation_select.value = self.method_interpolate

        ### Объемная линия
        ### Объемная линия
        ### Объемная линия
        self.points_volume_X = dct.get('volume_traxial').get(self.schema).get("point_values_X")
        self.limit_volume_axe_X = max(self.points_volume_X) + 0.05
        self.volume_method_interpolate = dct.get('volume_traxial').get(self.schema).get("method_interpolate")

        self.volume_mid_line_values.data = dict(x=self.points_volume_X, y=self.point_values_Y)

        self.calculate()

        self.Y_boundaries()

        self.save_schema()

        self.update_plot()

    def calculate(self):
        """
        Высчитывание отхождения линий по минимальным и максимальным процентам от точек средней линии
        :return:
        """
        self.min_line_values.data['x'] = [AX * ((100 - perc) / 100) for AX, perc in zip(self.mid_line_values.data['x'], self.table_values_perc.data['x_min'])]
        self.max_line_values.data['x'] = [AX * ((100 + perc) / 100) for AX, perc in zip(self.mid_line_values.data['x'], self.table_values_perc.data['x_max'])]

        self.volume_min_line_values.data['x'] = [AX * ((100 - perc * self.multiple_value) / 100) for AX, perc in
                                          zip(self.volume_mid_line_values.data['x'], self.table_values_perc.data['x_min'])]
        self.volume_max_line_values.data['x'] = [AX * ((100 + perc * self.multiple_value) / 100) for AX, perc in
                                          zip(self.volume_mid_line_values.data['x'], self.table_values_perc.data['x_max'])]

    def handle_table_edit(self, event):
        """
        Возможность редактирования точек в таблице процентов
        :param event:
        :return:
        """
        edited_item = event.column.field
        edited_row = event.row
        new_value = event.new

        self.table_values.data[edited_item][edited_row] = new_value
        self.table_values.change.emit()

    def update_plot(self, ):
        """
        Обновляет все отображение каждый заданный фрейм и при вызове из функций
        :return:
        """

        self.delete_handler()

        self.mid_line_interpolate_values.data = self.update_random_and_count_point(self.interpolation_line(self.mid_line_values.data['x'],
                                                                        self.mid_line_values.data['y']))

        """
        Объемные
        """
        self.volume_mid_line_values.data['y'] = self.mid_line_values.data['y']

        if len(self.volume_mid_line_values.data['x']) < len(self.mid_line_values.data['x']):
            self.volume_mid_line_values.data['x'].append(0)
        if len(self.volume_mid_line_values.data['x']) > len(self.mid_line_values.data['x']):
            self.volume_mid_line_values.data['x'].pop(-1)

        self.volume_mid_line_interpolate_values.data = dict(
            self.volume_interpolation_line(self.volume_mid_line_values.data['x'],
                                    self.mid_line_values.data['y']))
        self.volume_min_line_values.data['y'] = self.mid_line_values.data['y']
        self.volume_max_line_values.data['y'] = self.mid_line_values.data['y']

        self.volume_mid_line_interpolate_values.data = self.update_random_and_count_point(
            self.volume_interpolation_line(self.volume_mid_line_values.data['x'],
                                           self.volume_mid_line_values.data['y']))

        """
        Давление
        """
        self.table_values.data['x'] = self.mid_line_values.data['x']
        self.table_values.data['y'] = self.mid_line_values.data['y']

        self.min_line_values.data['y'] = self.mid_line_values.data['y']
        self.max_line_values.data['y'] = self.mid_line_values.data['y']

        if len(self.mid_line_values.data['x']) > len(self.table_values_perc.data['x_min']):
            self.list_X_min.append(0)
            self.list_X_max.append(0)
            self.list_Y_min.append(0)
            self.list_Y_max.append(0)
            # Обновление данных в таблице
            new_data = {
                'x': self.mid_line_values.data['x'],
                'y': self.mid_line_values.data['y'],
                'x_min': self.list_X_min,
                'x_max': self.list_X_max,
                'y_min': self.list_Y_min,
                'y_max': self.list_Y_max,
            }
            self.table_values_perc.data = new_data

        # Обновление данных в таблице
        new_data = {
                'x': self.point_values_X,
                'y': self.point_values_Y,
            }
        self.table_values.data = new_data

        self.calculate()


        self.min_line_interpolate_values.data = dict(self.interpolation_line(self.min_line_values.data['x'],
                                                                             self.mid_line_values.data['y']))

        self.max_line_interpolate_values.data = dict(self.interpolation_line(self.max_line_values.data['x'],
                                                                             self.mid_line_values.data['y']))

        self.y_max_min_values.data = dict(xs=self.Y_boundaries()[0], ys=self.Y_boundaries()[1])

        self.point_values_X = self.mid_line_values.data['x']
        self.point_values_Y = self.mid_line_values.data['y']

        """
        Объемные
        """
        self.volume_min_line_interpolate_values.data = dict(self.volume_interpolation_line(self.volume_min_line_values.data['x'],
                                                                             self.volume_mid_line_values.data['y']))

        self.volume_max_line_interpolate_values.data = dict(self.volume_interpolation_line(self.volume_max_line_values.data['x'],
                                                                             self.volume_mid_line_values.data['y']))

        self.points_volume_X = self.volume_mid_line_values.data['x']

    def interpolation_line(self, X, Y):
        """
        Интерполяция по контрольным предоставляемым откуда угодно точкам в соответствии с выбранным методом интерполяции
        :param X:
        :param Y:
        :return:
        """
        Y = [y * 76 for y in Y]

        yfit = np.linspace(min(Y), max(Y), num=50)

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
                pchip = interpolate.interp1d(Y, X, kind='nearest')

            if self.method_interpolate == "quadratic":
                pchip = interpolate.interp1d(Y, X, kind='quadratic')

            if self.method_interpolate == "cubic":
                pchip = interpolate.interp1d(Y, X, kind='cubic')

        except ValueError:
            print("Невозможно интерполировать значения")
            return

        xnew = pchip(yfit)

        return {'x': xnew, 'y': [y / 76 for y in yfit]}

    def volume_interpolation_line(self, X, Y):
        """
        Интерполяция по контрольным предоставляемым откуда угодно точкам в соответствии с выбранным методом интерполяции
        :param X:
        :param Y:
        :return:
        """
        Y = [y * 76 for y in Y]

        yfit = np.linspace(min(Y), max(Y), num=50)

        try:
            for index in range(len(Y) - 1):
                if Y[index] + 0.05 >= Y[index + 1]:
                    raise ValueError

            if self.volume_method_interpolate == "linear":
                pchip = interpolate.interp1d(Y, X, kind='linear')

            if self.volume_method_interpolate == "CubicSpline":
                pchip = interpolate.CubicSpline(Y, X)

            if self.volume_method_interpolate == "PchipInterpolator":
                pchip = interpolate.PchipInterpolator(Y, X)

            if self.volume_method_interpolate == "Akima1DInterpolator":
                pchip = interpolate.Akima1DInterpolator(Y, X)

            if self.volume_method_interpolate == "BarycentricInterpolator":
                pchip = interpolate.BarycentricInterpolator(Y, X)

            if self.volume_method_interpolate == "KroghInterpolator":
                pchip = interpolate.KroghInterpolator(Y, X)

            if self.volume_method_interpolate == "make_interp_spline":
                pchip = interpolate.make_interp_spline(Y, X)

            if self.volume_method_interpolate == "nearest":
                pchip = interpolate.interp1d(Y, X, kind='nearest')

            if self.volume_method_interpolate == "quadratic":
                pchip = interpolate.interp1d(Y, X, kind='quadratic')

            if self.volume_method_interpolate == "cubic":
                pchip = interpolate.interp1d(Y, X, kind='cubic')

        except ValueError:
            print("Невозможно интерполировать значения")
            return

        xnew = pchip(yfit)

        return {'x': xnew, 'y': [y / 76 for y in yfit]}

    def run(self):
        """
        Запуск программы
        :return:
        """
        # Подключение обработчика события изменения выбранного метода интерполяции
        self.interpolation_select.on_change('value', self.interpolation_select_handler)
        self.volume_interpolation_select.on_change('value', self.volume_interpolation_select_handler)
        self.schema_select.on_change('value', self.schema_select_handler)
        self.table_values_perc.js_on_change('patching', CustomJS(code="console.log(cb_obj);"))

        # Подключение обработчиков событий
        curdoc().add_root(row(self.plot, column(self.name_new_shema, self.button_add_schema, self.button_delete_schema), self.plot_volume))
        curdoc().add_root(row(self.interpolation_select,
                              self.volume_interpolation_select,
                              self.schema_select,
                              self.button_save_schema,
                              self.button_reset_schema,
                              self.count_points_min_text,
                              self.count_points_max_text,
                              self.random_percent_min_text,
                              self.random_percent_max_text,
                              self.multiple_volume,
                              self.button_update_point_random,
                              self.random_activate,
                              ))

        curdoc().add_root(column(row(self.data_table, self.data_table_perc)))
        curdoc().add_periodic_callback(self.update_plot, 100)  # Обновление графика каждые 100 мс

        self.plot.on_event('tap', self.add_point_handler)  # Обработчик нажатия на график
        self.plot.on_event('pan', self.move_point_handler)  # Обработчик перемещения точки


        self.plot_volume.on_event('pan', self.volume_move_point_handler)  # Обработчик перемещения точки

"""

distribut = DD(id_people='356379915') # sys.argv[1])
distribut.check_schemas_people()
distribut.write_data_in_database()
graphs = Graph_traxial(distribut.data)
graphs.run()
"""

distribut = DD(id_people=sys.argv[1]) # sys.argv[1])
distribut.check_schemas_people()
distribut.write_data_in_database()
if sys.argv[2] == 'traxial':
    graphs = Graph_traxial(distribut.data)
    graphs.run()
