import random
import sys

import numpy as np
from scipy import interpolate

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (CheckboxButtonGroup, CustomJS, IntEditor, TextInput, Button, ColumnDataSource, PointDrawTool, Select, TableColumn, DataTable, NumberFormatter)
from bokeh.plotting import figure

from DataDistributor_DB import DataDitributor as DD

from Graph_server import Graph_traxial

class ConsolidationGraph(Graph_traxial):
    def __init__(self, dct: dict):
        self.global_schema = 'consolidation'

        ### Распаковка элементов
        self.schema = dct.get(f"{self.global_schema}_scheme_now")

        ### Точки для основной кривой
        self.point_values_X = dct.get(self.global_schema).get(self.schema).get("point_values_X")
        self.point_values_Y = [y / 76 for y in dct.get(self.global_schema).get(self.schema).get("point_values_Y")]

        ### Лимит
        self.limit_axe_X = max(self.point_values_X) + 0.05
        self.limit_axe_Y = dct.get(self.global_schema).get(self.schema).get("limit_axe_Y") / 76
        ### Интерполяция
        self.method_interpolate = dct.get(self.global_schema).get(self.schema).get("method_interpolate")
        ### Проценты с APP
        self.list_X_min = dct.get(self.global_schema).get(self.schema).get("list_X_min")
        self.list_X_max = dct.get(self.global_schema).get(self.schema).get("list_X_max")
        self.list_Y_min = dct.get(self.global_schema).get(self.schema).get("list_Y_min")
        self.list_Y_max = dct.get(self.global_schema).get(self.schema).get("list_Y_max")
        ### Проценты с APP
        self.count_points_min = str(dct.get(self.global_schema).get(self.schema).get("count_points_min"))
        self.count_points_max = str(dct.get(self.global_schema).get(self.schema).get("count_points_max"))
        self.random_percent_min = str(dct.get(self.global_schema).get(self.schema).get("random_percent_min"))
        self.random_percent_max = str(dct.get(self.global_schema).get(self.schema).get("random_percent_max"))

        ### Инициализация графика и графических утилит
        self.plot = figure(width=1000, height=1000, y_range=(self.limit_axe_Y, 0))
        self.plot.y_range.start = 0.15
        self.plot.y_range.end = 0
        ### Создание значений для линий
        # Основная линия
        self.mid_line_values = ColumnDataSource(data=dict(x=self.point_values_X, y=self.point_values_Y), )

        # Интерполяция точек по основной линии
        self.mid_line_interpolate_values = ColumnDataSource(
            data=dict(self.interpolation_line(self.mid_line_values.data['x'],
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
        self.table_values = ColumnDataSource(dict(x=self.mid_line_values.data['x'], y=self.mid_line_values.data['y'], ))

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
        self.interpolation_select = Select(title='Interpolation Method',
                                           value=distribut.data.get(self.global_schema).get(self.schema).get(
                                               "method_interpolate"),
                                           options=self.interpolation_methods)

        # Список схем
        self.schemas = [schem for schem in distribut.data.get(self.global_schema).keys() if
                        schem not in [f"{self.global_schema}_scheme_now"]]

        self.schema_select = Select(title='Choice schema',
                                    value=distribut.data.get(f"{self.global_schema}_scheme_now"),
                                    options=self.schemas)

    def schema_select_handler(self, attr, old, new):
        """
        Выбор схемы, ее загрузка, и отображение
        :param attr:
        :param old:
        :param new:
        :return:
        """
        distribut.write_data_in_database()

        self.schema = new

        distribut.data.update({f"{self.global_schema}_scheme_now": self.schema})
        if self.global_schema in ['traxial']:
            distribut.data.update({"volume_traxial_scheme_now": self.schema})

        dct = distribut.data_give()

        ### Распаковка элементов
        ### Точки для основной кривой
        self.point_values_X = dct.get(self.global_schema).get(self.schema).get("point_values_X")
        self.point_values_Y = [y / 76 for y in dct.get(self.global_schema).get(self.schema).get("point_values_Y")]
        ### Лимиты
        self.limit_axe_X = max(self.point_values_X) + 0.05
        self.limit_axe_Y = dct.get(self.global_schema).get(self.schema).get("limit_axe_Y") / 76
        ### Интерполяция
        self.method_interpolate = dct.get(self.global_schema).get(self.schema).get("method_interpolate")
        ### Проценты с APP
        self.list_X_min = dct.get(self.global_schema).get(self.schema).get("list_X_min")
        self.list_X_max = dct.get(self.global_schema).get(self.schema).get("list_X_max")
        self.list_Y_min = dct.get(self.global_schema).get(self.schema).get("list_Y_min")
        self.list_Y_max = dct.get(self.global_schema).get(self.schema).get("list_Y_max")
        ### Проценты с APP
        self.count_points_min = str(dct.get(self.global_schema).get(self.schema).get("count_points_min"))
        self.count_points_max = str(dct.get(self.global_schema).get(self.schema).get("count_points_max"))
        self.random_percent_min = str(dct.get(self.global_schema).get(self.schema).get("random_percent_min"))
        self.random_percent_max = str(dct.get(self.global_schema).get(self.schema).get("random_percent_max"))

        self.count_points_min_text.value = self.count_points_min
        self.count_points_max_text.value = self.count_points_max
        self.random_percent_min_text.value = self.random_percent_min
        self.random_percent_max_text.value = self.random_percent_max

        self.mid_line_values.data = dict(x=self.point_values_X, y=self.point_values_Y)

        self.table_values.data = dict(x=self.mid_line_values.data['x'], y=self.mid_line_values.data['y'], )

        self.table_values_perc.data = dict(x=self.point_values_X, y=self.point_values_Y,
                                           x_min=self.list_X_min, x_max=self.list_X_max,
                                           y_min=self.list_Y_min, y_max=self.list_Y_max)

        self.interpolation_select.value = self.method_interpolate

        self.calculate()

        self.Y_boundaries()

        self.save_schema()

        self.update_plot()

    def interpolation_line(self, X, Y):
        """
        Интерполяция по контрольным предоставляемым откуда угодно точкам в соответствии с выбранным методом интерполяции
        :param X:
        :param Y:
        :return:
        """
        Y = [y * 7600 for y in Y]

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

        return {'x': xnew, 'y': [y / 7600 for y in yfit]}

    def save_schema(self):
        """
        Переопределить для другого класса
        :return:
        """
        distribut.data.get(self.global_schema)[self.schema] = {
                                  "method_interpolate": self.method_interpolate,
                                  "limit_axe_X": self.limit_axe_X,
                                  "limit_axe_Y": max(self.point_values_Y) * 76,

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

        distribut.write_data_in_database()

distribut = DD(id_people='356379915') # sys.argv[1])
distribut.check_schemas_people()
distribut.write_data_in_database()
graphs = ConsolidationGraph(distribut.data)
graphs.run()
"""


distribut = DD(id_people=sys.argv[1]) # sys.argv[1])
distribut.check_schemas_people()
distribut.write_data_in_database()
if sys.argv[2] == 'consolidation':
    graphs = ConsolidationGraph(distribut.data)
    graphs.run()
"""
