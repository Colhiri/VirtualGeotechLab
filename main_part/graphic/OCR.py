import math
import random
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
from sympy import Point, Line

from GEOF.main_part.main_tools.main_functions import nearest, return_index, bezier_curve

class CustomLine:
    def __init__(self, slope, const):
        self.m = slope
        self.c = const

def findSolution(L1, L2):
    if L1.c > L2.c:
        x = 10**(abs((L1.c - L2.c) / (L2.m - L1.m)))
        y = L1.m * math.log10(x) + L1.c
    else:
        x = 10**((L1.c - L2.c) / abs(L2.m - L1.m))
        y = L1.m * math.log10(x) + L1.c

    return x, y

class compression_OCR:
    def __init__(self, organise_dct):
        self.organise_dct = organise_dct

        self.IP = self.organise_dct.get('IP')
        self.IL = self.organise_dct.get('IL')
        self.e = self.organise_dct.get('e')
        self.p = self.organise_dct.get('p')
        self.g = 9.80665
        self.depth = self.organise_dct.get('depth')

        self.OCR = self.organise_dct.get('OCR')

        self.plot_value = False

        logging.basicConfig(level=logging.INFO, filename="OCR_isp.log", filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

        if not self.IP or not self.IL or not self.e or not self.p or not self.depth:
            logging.warning(f"Multiple parameters without value")
        logging.info(
            f"Initialize successful: Depth: {self.depth}, IP: {self.IP}, IL: {self.IL}, e: {self.e}, p: {self.p}.")

    def definition_press(self):
        if self.IP:
            if self.IL >= 1:
                press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
            if 1 > self.IL >= 0.75:
                press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
            if 0.75 > self.IL >= 0.5:
                press_spd = [0, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
            if 0.5 > self.IL >= 0.25:
                press_spd = [0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
            if self.IL < 0.25:
                press_spd = [0, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
        else:
            if self.e >= 1:
                press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
            if 1 > self.e >= 0.75:
                press_spd = [0, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
            if 0.75 > self.e > 0.6:
                press_spd = [0, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
            if self.e <= 0.6:
                press_spd = [0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]

        logging.info(f"Press graph - {press_spd}.")

        return press_spd

    def definition_q_zg(self) -> float:
        """
        Определяет природное эффективное напряжение
        :return:
        """
        try:
            press_zg = (self.p * self.g * self.depth) / 1000
        except TypeError:
            logging.error(f"Calculation error. The standard pressure is taken.")
            press_zg = 0.05
        logging.info(f"Effective press - {press_zg}.")
        return press_zg

    def parameters_beccer(self):
        # Узнаем давление переулотнения на основе OCR
        Sigma_Beccer = self.press_zg * self.OCR

        # Предскажем Y min и Y max для того, чтобы рассчитать среднюю контрольную точку
        ocr_diap = [0.1, 21]

        y_min = [1, 12]
        y_max = [2, 24]
        res_min = stats.linregress(ocr_diap, y_min)
        res_max = stats.linregress(ocr_diap, y_max)

        Y_MIN = int(self.OCR * res_min.slope + res_min.intercept)
        Y_MAX = int(self.OCR * res_max.slope + res_max.intercept)

        # Проведем касательную из нижней части
        y_middle_cp = random.randint(Y_MIN, Y_MAX) / 10000  # средняя точка по оси Y

        # Уравнение нижней прямой (необходимо для нахождения Y последней точки
        res_2 = stats.linregress([min(self.press_spd), Sigma_Beccer], [0, y_middle_cp])
        y_last_cp = max(self.press_spd) * res_2.slope + res_2.intercept

        # Нижняя прямая
        x2 = [min(self.press_spd), max(self.press_spd)]
        y2 = [0, y_last_cp]

        # Предсказываем последний Y
        y1_last_regress = [0.25, 0.5]
        res = stats.linregress(ocr_diap, y1_last_regress)
        y1_last = self.press_spd[-1] * res.slope + res.intercept

        # Верхняя прямая
        x1 = [Sigma_Beccer, max(self.press_spd)]
        y1 = [y_middle_cp, y1_last]

        # Залоченное значение посередине -- средняя точка между конечным давлением и Сигмой Беккера по X и Y
        control_points = np.asarray([(min(self.press_spd), 0.0), (Sigma_Beccer, y_middle_cp), (max(self.press_spd), y1_last)])
        xnew, ynew = bezier_curve(control_points, 100)

        # Прореживание значений по Х и Y
        new_W = [return_index(xnew, ynew, press) for press in self.press_spd[1:len(self.press_spd) - 1]]
        new_W.insert(0, 0)
        new_W.append(y1_last)

        # Восттановление исходных данных по дельта W, относительной вертикальной деформации
        W_DJ = [val * 1000 for val in new_W]
        delta_W = [(W_DJ1 - W_DJ_past) for (W_DJ_past, W_DJ1) in zip(W_DJ[0:len(W_DJ) - 1], W_DJ[1:len(W_DJ)])]
        delta_W.insert(0, 0)

        calc_otn_vert_def = [(del_W / (500 * (press_1 + press_2))) for del_W, press_2, press_1 in
                             zip(delta_W[1:], self.press_spd[1:len(self.press_spd)],
                                 self.press_spd[0:len(self.press_spd) - 1])]
        calc_otn_vert_def.insert(0, 0)

        calc_otn_vert_def = [calc_otn_vert_def[x] + sum(calc_otn_vert_def[:x]) for x in range(len(calc_otn_vert_def))]

        por_list = [(self.e - (otn_vert * (1 + self.e))) for otn_vert in calc_otn_vert_def]

        logging.info(f"Method Beccer is complete.")

        return Sigma_Beccer, calc_otn_vert_def, y_middle_cp, delta_W, new_W, por_list, x1, y1, x2, y2

    def parameters_casagrande(self):
        press_spd = self.press_spd[1:]
        por_list = self.por_list[1:]

        log_scale_X = [math.log10(x) for x in press_spd]

        # Проводим касательную из двух последних точек
        res_CAS_1 = stats.linregress(log_scale_X[(len(log_scale_X) - 2):], por_list[(len(por_list) - 2):])
        CAS_1_Y = [
            math.log10(min(press_spd)) * res_CAS_1.slope + res_CAS_1.intercept,
            por_list[len(por_list) - 2],
            por_list[len(por_list) - 1],]

        CAS_1_X = [min(press_spd), press_spd[-2], press_spd[-1],]

        # Проводим касательную из двух первых точек
        res_CAS_2 = stats.linregress(log_scale_X[:2], por_list[:2])

        # Находим точку пересечения двух касательных разных концов компрессионной кривой
        point_X_CASS = 10 ** (((res_CAS_1.intercept - res_CAS_2.intercept) / abs(res_CAS_1.slope - res_CAS_2.slope)))
        point_Y_CASS = math.log10(point_X_CASS) * res_CAS_2.slope + res_CAS_2.intercept

        # Найдем точку диапазона Х по компрессионной кривой и найдем Y по уравнению выявленного диапазона
        point_1_diap = nearest(press_spd, point_X_CASS)
        if point_X_CASS > press_spd.index(point_1_diap):
            index_1 = press_spd.index(point_1_diap)
            index_2 = index_1 + 1
        else:
            index_2 = press_spd.index(point_1_diap)
            index_1 = index_2 - 1
        res_diap_COMPLINE = stats.linregress([log_scale_X[index_1], log_scale_X[index_2]],
                                             [(por_list[index_1]), (por_list[index_2])])

        # Перпендикулярная линия к прямой крайних точек
        p1 = Point(press_spd[index_1], por_list[index_1])
        p2 = Point(press_spd[index_2], por_list[index_2])
        p3 = Point((point_X_CASS), point_Y_CASS)

        l1 = Line(p1, p2)
        l2 = l1.perpendicular_line(p3).points
        point_X_COMP, point_Y_COMP = list(abs(float(x.evalf())) for x in l2[0].coordinates)
        point_X_COMP1, point_Y_COMP1 = list(abs(float(x.evalf())) for x in l2[1].coordinates)

        res_PERPENDICULAR = stats.linregress([math.log10(point_X_COMP), math.log10(point_X_COMP1)],
                                             [point_Y_COMP, point_Y_COMP1])

        L1 = CustomLine(res_diap_COMPLINE.slope, res_diap_COMPLINE.intercept)  # Equation of line y=3x+5
        L2 = CustomLine(res_PERPENDICULAR.slope, res_PERPENDICULAR.intercept)
        point_X_COMP, point_Y_COMP = findSolution(L1, L2)

        # Провести три угловые линии
        first_line_x = [point_X_COMP, press_spd[index_2+1], max(press_spd)]
        LOG_first_line_x = [math.log10(point_X_COMP), math.log10(press_spd[index_2+1]), math.log10(max(press_spd))]
        first_line_y = [point_Y_COMP, point_Y_COMP, point_Y_COMP]

        third_line_x = [point_X_COMP, press_spd[index_2+1], ]
        LOG_third_line_x = [math.log10(point_X_COMP), math.log10(press_spd[index_2+1]), ]
        third_line_y = [point_Y_COMP, por_list[index_2+1], ]
        res_third_line = stats.linregress(LOG_third_line_x, third_line_y)
        third_last_y = math.log10(max(press_spd)) * res_third_line.slope + res_third_line.intercept
        third_line_x.append(max(press_spd))
        LOG_third_line_x.append(math.log10(max(press_spd)))
        third_line_y.append(third_last_y)

        second_line_x = first_line_x
        LOG_second_line_x = LOG_first_line_x
        second_line_y = [point_Y_COMP, (first_line_y[1] + third_line_y[1]) / 2, (first_line_y[2] + third_line_y[2]) / 2]
        res_second_line = stats.linregress(LOG_second_line_x, second_line_y)

        # Найти точку пересечения нижней касательной и биссектрисы
        L3 = CustomLine(res_CAS_1.slope, res_CAS_1.intercept)  # Equation of line y=3x+5
        L4 = CustomLine(res_second_line.slope, res_second_line.intercept)
        point_X_GG, point_Y_GG = findSolution(L3, L4)

        # Перпендикуляр от точки
        perp_GG_X = [point_X_GG, point_X_GG, point_X_GG]
        perp_GG_Y = [point_Y_GG, 0, 0]

        # Касательная к точке пересечения касательных,
        xrange_CAS_B = np.linspace(min(press_spd), max(press_spd), 3)
        yrange_CAS_B = [math.log10(x) * res_diap_COMPLINE.slope + res_diap_COMPLINE.intercept for x in xrange_CAS_B]

        logging.info(f"Method Casagrande is complete.")

        return (CAS_1_X, CAS_1_Y, first_line_x, first_line_y, second_line_x, second_line_y,
            third_line_x, third_line_y, point_X_GG, point_Y_GG, perp_GG_X, perp_GG_Y, point_X_COMP, point_Y_COMP,
                xrange_CAS_B, yrange_CAS_B)

    def create_values(self):

        CAS_dct = {'press': self.press_spd,
                   'otn': self.otn_vert_def,
                   'por': self.por_list}
        df_CAS = pd.DataFrame.from_dict(CAS_dct)
        df_CAS.reset_index(drop=True, inplace=True)

        # Основной датафрейм для Беккера
        BEC_dct = {'press': self.press_spd,
                   'delta_W': self.delta_W,
                   'W_DJ': self.W_DJ}
        df_BEC = pd.DataFrame.from_dict(BEC_dct)
        df_BEC.reset_index(drop=True, inplace=True)

        # Метод Беккера
        prepare_BECCER = {'x_1': self.x1,
                          'y_1': [x for x in self.y1],
                          'x_2': self.x2,
                          'y_2': [x for x in self.y2],
                          'sig_x': [self.Sigma_Beccer, self.Sigma_Beccer],
                          'sig_y': [self.y_middle_cp, self.y_middle_cp],
                          }

        BECCER = pd.DataFrame.from_dict(prepare_BECCER)
        BECCER.reset_index(drop=True, inplace=True)

        # Метод Казагранде
        prepare_CASAGRANDE = {'c1_x': self.CAS_1_X,
                              'c1_y': self.CAS_1_Y,
                              'fir_x': self.first_line_x,
                              'fir_y': self.first_line_y,
                              'sec_x': self.second_line_x,
                              'sec_y': self.second_line_y,
                              'thir_x': self.third_line_x,
                              'thir_y': self.third_line_y,
                              'p_gg_x': [self.point_X_GG, self.point_X_GG, self.point_X_GG],
                              'p_gg_y': [self.point_Y_GG, self.point_Y_GG, self.point_Y_GG],
                              'perp_x': self.perp_GG_X,
                              'perp_y': self.perp_GG_Y,
                              'x_CAS_B': self.xrange_CAS_B,
                              'y_CAS_B': self.yrange_CAS_B,
                              }
        VALUES_LINES = pd.DataFrame(prepare_CASAGRANDE)
        VALUES_LINES.reset_index(drop=True, inplace=True)

        values_for_Excel = {
            #### Беккер
            'effective_press': self.press_zg,
            'Sigma_Beccer': self.Sigma_Beccer,
            'Y_Beccer': self.y_middle_cp * 1000,
            'OCR': self.OCR,
            'POP': self.POP,
            'BECCER': BECCER,
            'DATA_BEKKER': df_BEC,
            'image_beccer': self.image_beccer,

            #### Казагранде
            'VALUES_LINES': VALUES_LINES,
            'Sigma_CASAGRANDE': self.point_X_GG,
            'Y_CASAGRANDE': self.point_Y_GG,
            'OCR_CASAGRANDE': self.point_X_GG / self.press_zg,
            'POP_CASAGRANDE': self.point_X_GG - self.press_zg,
            'DATA_CASAGRANDE': df_CAS,
            'image_casagrande': self.image_casagrande,
        }

        logging.info(f"Values to Excel are obtained.")

        return values_for_Excel

    def aggeragation(self):

        self.press_spd = self.definition_press()

        self.press_zg = self.definition_q_zg()

        self.Sigma_Beccer, self.otn_vert_def, self.y_middle_cp, self.delta_W, self.W_DJ, self.por_list, self.x1, self.y1, self.x2, self.y2 = self.parameters_beccer()

        self.POP = self.Sigma_Beccer - self.press_zg

        self.image_beccer = self.plotting_graph_beccer()

        (self.CAS_1_X, self.CAS_1_Y, self.first_line_x, self.first_line_y, self.second_line_x, self.second_line_y,
            self.third_line_x, self.third_line_y, self.point_X_GG, self.point_Y_GG, self.perp_GG_X, self.perp_GG_Y,
            self.point_X_COMP, self.point_Y_COMP, self.xrange_CAS_B, self.yrange_CAS_B) = self.parameters_casagrande()

        self.image_casagrande = self.plotting_graph_casagrande()

        logging.info(f"\n")

    def plotting_graph_beccer(self):
        """
        Формирует график
        :return:f
        """
        plt.gcf().subplots_adjust(left=0.15, bottom=0.15)
        ax = plt.gca()
        ax.set_ylim((0, self.W_DJ[-1] * 1.1))

        plt.xlabel('Вертикальное давление, МПа')
        plt.ylabel('Удельная работа W уд, МДж/м3')

        plt.plot(self.x2, self.y2, color='blue')
        plt.plot(self.x1, self.y1, color='blue')

        # Значения кривой
        plt.plot(self.press_spd, self.W_DJ, color='red')
        plt.plot(self.press_spd, self.W_DJ, 'o', markerfacecolor='black', markeredgecolor='black')
        # Точка пересечения
        plt.plot(self.Sigma_Beccer, self.y_middle_cp, 'o', markerfacecolor='black', markeredgecolor='black')

        plt.grid(color='gray')

        if self.plot_value:
            plt.show()

        logging.info(f"The image was obtained using the Kazagrande method.")

        return True

    def plotting_graph_casagrande(self):
        """
        Формирует график
        :return:f
        """
        plt.gcf().subplots_adjust(left=0.15, bottom=0.15)
        ax = plt.gca()
        ax.set_ylim((0, self.por_list[0] * 1.1))
        plt.xscale('log')

        # Компрессионная кривая
        plt.plot(self.press_spd[1:], self.por_list[1:], color='red')
        plt.plot(self.press_spd[1:], self.por_list[1:], 'o', markerfacecolor='black', markeredgecolor='black')
        # Нижняя касательная
        plt.plot(self.CAS_1_X, self.CAS_1_Y, color='yellow')
        # Угловые линии к точке пересечения перпендикуляра и компрессионной кривой
        plt.plot(self.first_line_x, self.first_line_y, color='black')
        plt.plot(self.second_line_x, self.second_line_y, color='black')
        plt.plot(self.third_line_x, self.third_line_y, color='black')
        # Перпендикуляр от точки GG
        plt.plot(self.perp_GG_X, self.perp_GG_Y, color='green', linestyle='dashed')
        # Касательная
        plt.plot(self.xrange_CAS_B, self.yrange_CAS_B, color='blue', linestyle='dashed')
        # Точка пересечения биссетрисы и нижней касательной
        plt.plot(self.point_X_GG, self.point_Y_GG, 'p', markerfacecolor='yellow', markeredgecolor='black', markersize=7.5)
        # Точка пересечения перпендикуляра и прямой конечных точек
        plt.plot(self.point_X_COMP, self.point_Y_COMP, 'H', markerfacecolor='purple', markeredgecolor='black', markersize=7.5)
        plt.grid()

        if self.plot_value:
            plt.show()

        logging.info(f"The image was obtained using the Beccer method.")

        return True


if __name__ == "__main__":
    organise_dct = {
        'OCR': 5,
        'depth': 10,
        'IP': 10,
        'IL': 0.3,
        'e': 0.7,
        'p': 2,
    }

    test = compression_OCR(organise_dct=organise_dct)
    test.aggeragation()
