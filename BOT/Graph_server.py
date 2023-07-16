from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (MultiLine, CustomJS, IntEditor, TextInput, Button, ColumnDataSource, PointDrawTool, Select, DateFormatter, Line, TableColumn, DataTable, NumberFormatter)
from bokeh.plotting import figure
from scipy import interpolate
import numpy as np
from bokeh.events import ButtonClick

from DataDistibutor import DataDistributor as DD

class Graph:
    def __init__(self, dct: dict):

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

        ### Инициализация графика и графических утилит
        self.plot = figure(width=800, height=800, y_range=(self.limit_axe_Y, 0))

        self.interpolation_methods = ["linear", "CubicSpline", "PchipInterpolator", "Akima1DInterpolator",
                                      "BarycentricInterpolator", "KroghInterpolator", "make_interp_spline",
                                      "nearest", "quadratic", "cubic"]
        self.interpolation_select = Select(title='Interpolation Method',
                                           value='PchipInterpolator',
                                           options=self.interpolation_methods)

        self.schemas = [schem for schem in distribut.data.keys() if schem not in ["scheme_now"]]
        self.schema_select = Select(title='Choice schema',
                                           value=distribut.data.get("scheme_now"),
                                           options=self.schemas)

        ### Создание значений для линий
        # Основная линия
        self.mid_line_values = ColumnDataSource(data=dict(x=self.point_values_X, y=self.point_values_Y),)
        # Интерполяция точек по основной линии
        self.mid_line_interpolate_values = ColumnDataSource(data=dict(self.interpolation_line(self.mid_line_values.data['x'],
                                                                                              self.mid_line_values.data['y'])))

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

        # Создание глифа для линии между точками
        self.min_line_glyph = Line(x='x', y='y', line_color='blue', line_width=1)
        self.plot.add_glyph(self.min_line_interpolate_values, self.min_line_glyph)

        self.max_line_glyph = Line(x='x', y='y', line_color='red', line_width=1)
        self.plot.add_glyph(self.max_line_interpolate_values, self.max_line_glyph)

        # Создание таблицы со значениями линий
        self.table_values = ColumnDataSource(dict(x=self.mid_line_values.data['x'], y=self.mid_line_values.data['y'],))

        self.columns_table = [
            TableColumn(field="x", title="X", formatter=NumberFormatter(format="0.00"), editor=IntEditor()),
            TableColumn(field="y", title="Y", formatter=NumberFormatter(format="0.00"), editor=IntEditor()),
        ]
        self.data_table = DataTable(source=self.table_values, columns=self.columns_table, editable=True,
                                    selectable=False, width=800,
                               index_position=-1, index_header="row index", index_width=60)



        self.table_values_perc = ColumnDataSource(dict(
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
        self.calculate()

        # Отображение точек на графике
        self.glyph = self.plot.circle('x', 'y', size=10, color='blue', alpha=0.5, source=self.mid_line_values)

        # Создание инструмента для перемещения точек
        self.draw_tool = PointDrawTool(renderers=[self.glyph], empty_value='black')
        self.plot.add_tools(self.draw_tool)

        # Создание глифа для линии между точками
        self.line_glyph = Line(x='x', y='y', line_color='gray', line_width=1)
        self.plot.add_glyph(self.mid_line_interpolate_values, self.line_glyph)

        # Текстовое поле для того, чтобы написать имя новой схемы
        self.name_new_shema = TextInput(title="Name new schema", value="")

        # Кнопка для добавления схемы
        self.button_add_schema = Button(label="Add schema", button_type='success')
        self.button_add_schema.on_click(self.add_new_schema)

        # Кнопка для удаления схемы
        self.button_delete_schema = Button(label="Delete schema", button_type='success')
        self.button_delete_schema.on_click(self.delete_schema)

        # Кнопка для сохранения схемы
        self.button_save_schema = Button(label="Save schema", button_type='success', height=40)
        self.button_save_schema.on_click(self.save_schema)

        self.y_max_min_values = ColumnDataSource(dict(xs=self.Y_boundaries()[0],
                                                 ys=self.Y_boundaries()[1]))

        self.y_max_min_glyph = MultiLine(xs="xs", ys="ys", line_color="#8073ac", line_width=2)

        self.plot.add_glyph(self.y_max_min_values, self.y_max_min_glyph)

    def Y_boundaries(self):

        segs_x = []
        segs_y = []
        for index in range(len(self.table_values_perc.data['y_max'])):
            value_x = [self.mid_line_values.data['x'][index], self.mid_line_values.data['x'][index]]
            value_y = [self.mid_line_values.data['y'][index] * ((100 + self.table_values_perc.data['y_max'][index]) / 100),
                       self.mid_line_values.data['y'][index] * ((100 - self.table_values_perc.data['y_min'][index]) / 100)
                       ]

            segs_x.append(value_x)
            segs_y.append(value_y)

        return (segs_x, segs_y)

    def update_Y_bound(self):
        self.y_max_min_values.data = dict(xs=self.Y_boundaries()[0], ys=self.Y_boundaries()[1])


    def add_point_table_perc(self):
        self.list_X_min.append(0)
        self.list_X_max.append(0)
        self.list_Y_min.append(0)
        self.list_Y_max.append(0)

    def add_new_schema(self):
        distribut.add_new_schema(self.name_new_shema.value)
        self.schema_select.options = [schem for schem in distribut.data.keys() if schem not in ["scheme_now"]]

    def delete_schema(self):
        distribut.delete_schema(self.schema_select.value)
        self.schema_select.options = [schem for schem in distribut.data.keys() if schem not in ["scheme_now"]]
        self.schema_select_handler(1, 1, self.schema_select.options[0])
        self.schema_select.value, self.schema = self.schema_select.options[0]

    def save_schema(self):
        distribut.data_update(self.schema_select.value,
                              {
                                  "limit_axe_Y": max(self.point_values_Y),
                                  "point_values_X": self.point_values_X,
                                  "point_values_Y": self.point_values_Y,
                                  "list_X_min": self.list_X_min,
                                  "list_X_max": self.list_X_max,
                                  "list_Y_min": self.list_Y_min,
                                  "list_Y_max": self.list_Y_max,
                              })
        distribut.data_save()

    # Обработчик события нажатия кнопки добавления точки
    def add_point_handler(self, event):
        x = event.x
        y = event.y

        self.mid_line_values.data['x'].append(x)
        self.mid_line_values.data['y'].append(y)

        self.update_plot()

    # Обработчик события перемещения точки
    def move_point_handler(self, event):
        # Сделай обработку точек, которые нельзя изменять
        self.mid_line_values.data = dict(x=event.x, y=event.y)
        self.update_plot()

    def interpolation_select_handler(self, attr, old, new):
        self.method_interpolate = new
        self.update_plot()

    def schema_select_handler(self, attr, old, new):
        self.schema = new
        distribut.data.update({"scheme_now": self.schema})

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

        self.mid_line_values.data = dict(x=self.point_values_X, y=self.point_values_Y)

        self.table_values.data = dict(x=self.mid_line_values.data['x'], y=self.mid_line_values.data['y'],)

        self.table_values_perc.data = dict(x_min=self.list_X_min, x_max=self.list_X_max,
                                            y_min=self.list_Y_min, y_max=self.list_Y_max)

        self.calculate()

        self.Y_boundaries()

        self.save_schema()

        self.update_plot()

    def calculate(self):
        self.min_line_values.data['x'] = [AX * ((100 - perc) / 100) for AX, perc in zip(self.mid_line_values.data['x'], self.table_values_perc.data['x_min'])]
        self.max_line_values.data['x'] = [AX * ((100 + perc) / 100) for AX, perc in zip(self.mid_line_values.data['x'], self.table_values_perc.data['x_max'])]

    def handle_table_edit(self, event):
        edited_item = event.column.field
        edited_row = event.row
        new_value = event.new

        self.table_values.data[edited_item][edited_row] = new_value
        self.table_values.change.emit()

    def update_plot(self):

        self.mid_line_interpolate_values.data = self.interpolation_line(self.mid_line_values.data['x'],
                                                                        self.mid_line_values.data['y'])

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

        self.update_Y_bound()

        self.point_values_X = self.mid_line_values.data['x']
        self.point_values_Y = self.mid_line_values.data['y']


    def interpolation_line(self, X, Y):
        """
        Интерполяция по контрольным предоставляемым откуда угодно точкам в соответствии с выбранным методом интерполяции
        :param X:
        :param Y:
        :return:
        """

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

        return {'x': xnew, 'y': yfit}

    def run(self):
        # Подключение обработчика события изменения выбранного метода интерполяции
        self.interpolation_select.on_change('value', self.interpolation_select_handler)
        self.schema_select.on_change('value', self.schema_select_handler)
        self.table_values_perc.js_on_change('patching', CustomJS(code="console.log(cb_obj);"))

        # Подключение обработчиков событий
        curdoc().add_root(row(self.plot, column(self.name_new_shema, self.button_add_schema, self.button_delete_schema)))
        curdoc().add_root(row(self.interpolation_select, self.schema_select, self.button_save_schema))

        curdoc().add_root(column(row(self.data_table, self.data_table_perc)))
        curdoc().add_periodic_callback(self.update_plot, 100)  # Обновление графика каждые 100 мс

        self.plot.on_event('tap', self.add_point_handler)  # Обработчик нажатия на график
        self.plot.on_event('pan', self.move_point_handler)  # Обработчик перемещения точки

distribut = DD()
graphs = Graph(distribut.data)
graphs.run()