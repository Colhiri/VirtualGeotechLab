import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
import scipy.stats as stats

from GEOF.main_part.main_tools.main_functions import interpolation, nearest, bezier_curve, random_values, Bezier

def return_index(lst, lst2, target):
    try:
        pressMAX = lst.tolist().index(max(lst))

    except:
        pressMAX = lst.index(max(lst))

    index = lst.index(min(lst[:pressMAX], key=lambda x: abs(x - target)))

    # Рассчитаем функцию
    res = stats.linregress([lst[index], lst[index + 1]], [lst2[index], lst2[index + 1]])
    new_value = target * res.slope + res.intercept

    return new_value

class CustomLine:
    def __init__(self, slope, const):
        self.m = slope
        self.c = const

def findSolution(L1, L2):
    if L1.c > L2.c:
        x = 10**(abs((L1.c - L2.c) / (L2.m - L1.m)))
        x_1 = 10 ** ((L1.c - L2.c) / abs(L2.m - L1.m))
        x_2 = 10 ** ((L1.c - L2.c) / abs(L2.m - L1.m))
        y_1 = L1.m * math.log10(x) + L1.c
        y = L1.m * math.log10(x) + L1.c
    else:
        x = 10**((L1.c - L2.c) / abs(L2.m - L1.m))
        y = L1.m * math.log10(x) + L1.c

    return x, y


def OCR_start(organise_dct: dict):
    IP = organise_dct.get('IP')
    IL = organise_dct.get('IL')
    e = organise_dct.get('e')
    p = organise_dct.get('p')
    g = 9.80665
    depth = organise_dct.get('depth')

    OCR = organise_dct.get('OCR')
    effective_press = organise_dct.get('effective_press')

    # Для глинистых грунтов
    if IP:
        if IL >= 1:
            press_spd_bekker = [0, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4,
                         8]
        if 1 > IL >= 0.75:
            press_spd_bekker = [0, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
        if 0.75 > IL >= 0.5:
            press_spd_bekker = [0, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
        if 0.5 > IL >= 0.25:
            press_spd_bekker = [0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
        if IL < 0.25:
            press_spd_bekker = [0, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
    else:
        if e >= 1:
            press_spd_bekker = [0, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4,
                         8]
        if 1 > e >= 0.75:
            press_spd_bekker = [0, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
        if 0.75 > e > 0.6:
            press_spd_bekker = [0, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]
        if e <= 0.6:
            press_spd_bekker = [0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 8]

    # Природное эффективное напряжение
    if str(effective_press) in ["None", "nan"]:
        effective_press = (p * g * depth) / 1000
    press_zg = effective_press

    #### Беккер
    #### Беккер
    #### Беккер

    # Узнаем давление переулотнения на основе OCR
    Sigma_Beccer = press_zg * OCR

    # Узнаем POP
    POP = Sigma_Beccer - press_zg

    # Предскажем Y min и Y max для того, чтобы рассчитать среднюю контрольную точку
    ocr_diap = [0.1, 21]

    y_min = [1, 12]
    y_max = [2, 24]
    res_min = stats.linregress(ocr_diap, y_min)
    res_max = stats.linregress(ocr_diap, y_max)

    Y_MIN = int(OCR * res_min.slope + res_min.intercept)
    Y_MAX = int(OCR * res_max.slope + res_max.intercept)

    # Проведем касательную из нижней части
    y_middle_cp = random.randint(Y_MIN, Y_MAX) / 10000  # средняя точка по оси Y

    # Уравнение нижней прямой (необходимо для нахождения Y последней точки
    res_2 = stats.linregress([min(press_spd_bekker), Sigma_Beccer], [0, y_middle_cp])
    y_last_cp = max(press_spd_bekker) * res_2.slope + res_2.intercept

    # Нижняя прямая
    x2 = [min(press_spd_bekker), Sigma_Beccer, max(press_spd_bekker)]
    y2 = [0, y_middle_cp, y_last_cp]

    # Предсказываем последний Y
    y1_last_regress = [0.25, 0.5]
    res = stats.linregress(ocr_diap, y1_last_regress)
    y1_last = press_spd_bekker[-1] * res.slope + res.intercept

    # Верхняя прямая
    x1 = [Sigma_Beccer, max(press_spd_bekker)]
    y1 = [y_middle_cp, y1_last]

    # Залоченное значение посередине -- средняя точка между конечным давлением и Сигмой Беккера по X и Y
    control_points = np.asarray([(min(press_spd_bekker), 0.0),
                                 (Sigma_Beccer, y_middle_cp),
                                 (max(press_spd_bekker), y1_last)
                                 ])

    t_points = np.arange(0, 1, 0.05)
    points1 = control_points

    curve1 = Bezier.Curve(t_points, points1)

    x = curve1[:, 0].tolist()  # press в МПа
    y = curve1[:, 1].tolist()  # W в кДж
    x.append(max(press_spd_bekker))
    y.append(y1_last)

    # Прореживание значений по Х и Y
    new_W = []
    for press in press_spd_bekker[1:len(press_spd_bekker) - 1]:
        new_y = return_index(x, y, press)
        new_W.append(new_y)
    new_W.insert(0, 0)
    new_W.append(y1_last)

    # Восттановление исходных данных по дельта W, относительной вертикальной деформации
    W_DJ = [val * 1000 for val in new_W]
    delta_W = [(W_DJ1 - W_DJ_past) for (W_DJ_past, W_DJ1) in zip(W_DJ[0:len(W_DJ) - 1], W_DJ[1:len(W_DJ)])]
    delta_W.insert(0, 0)

    calc_otn_vert_def = [(del_W / (500 * (press_1 + press_2))) for del_W, press_2, press_1 in
                         zip(delta_W[1:], press_spd_bekker[1:len(press_spd_bekker)],
                             press_spd_bekker[0:len(press_spd_bekker) - 1])]
    calc_otn_vert_def.insert(0, 0)

    calc_otn_vert_def = [calc_otn_vert_def[x] + sum(calc_otn_vert_def[:x]) for x in range(len(calc_otn_vert_def))]

    por_list = [(e - (otn_vert * (1 + e))) for otn_vert in calc_otn_vert_def]

    # plt.plot(press_spd, new_W,  '.')
    # plt.plot(press_spd, new_W)
    # plt.plot(Sigma_Beccer, y_middle_cp, '*')
    # plt.plot(x1, y1)
    # plt.plot(x2, y2)
    # plt.grid()
    # plt.show()

    #### Казагранде
    #### Казагранде
    #### Казагранде
    #### Казагранде
    press_spd = press_spd_bekker[1:]
    por_list = por_list[1:]

    log_scale_X = [math.log10(x) for x in press_spd]

    # Проводим касательную из двух последних точек
    res_CAS_1 = stats.linregress(log_scale_X[(len(log_scale_X) - 2):], por_list[(len(por_list) - 2):])
    CAS_1_Y = [
        math.log10(min(press_spd)) * res_CAS_1.slope + res_CAS_1.intercept,
        por_list[len(por_list) - 2],
        por_list[len(por_list) - 1],
    ]
    CAS_1_X = [
        min(press_spd),
        press_spd[-2],
        press_spd[-1],
    ]

    # Проводим касательную из двух первых точек
    res_CAS_2 = stats.linregress(log_scale_X[:2], por_list[:2])
    CAS_2_Y = [
        math.log10(max(press_spd)) * res_CAS_2.slope + res_CAS_2.intercept,
        por_list[0],
        por_list[1],
    ]
    CAS_2_X = [
        max(press_spd),
        press_spd[0],
        press_spd[1],
    ]

    # Находим точку пересечения двух касательных разных концов компрессионной кривой

    point_X_CASS = (10**(abs((res_CAS_1.intercept - res_CAS_2.intercept) / (res_CAS_1.slope - res_CAS_2.slope)))
                    if res_CAS_1.intercept > res_CAS_2.intercept
                    else 10**(
        ((res_CAS_1.intercept - res_CAS_2.intercept) / abs(res_CAS_1.slope - res_CAS_2.slope))))

    point_Y_CASS = math.log10(point_X_CASS) * res_CAS_2.slope + res_CAS_2.intercept


    # Построение прямой, соединяющей две крайние точки графика
    res_START_END_LINE = stats.linregress([log_scale_X[0], log_scale_X[-1]], [(por_list[0]), (por_list[-1])])
    START_END_LINE_X = [(press_spd[0]), (press_spd[-1])]
    START_END_LINE_Y = [(por_list[0]), (por_list[-1])]


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
    from sympy import Point, Line
    p1, p2, p3 = Point(press_spd[index_1], por_list[index_1]), Point(press_spd[index_2], por_list[index_2]), Point((point_X_CASS),
                                                                                                 point_Y_CASS)
    l1 = Line(p1, p2)
    # using perpendicular_line() method
    l2 = l1.perpendicular_line(p3)
    l2s = l2.bounds
    l2 = l1.perpendicular_line(p3).points
    point_X_COMP, point_Y_COMP = list(abs(float(x.evalf())) for x in l2[0].coordinates)
    point_X_COMP1, point_Y_COMP1 = list(abs(float(x.evalf())) for x in l2[1].coordinates)

    res_PERPENDICULAR = stats.linregress([math.log10(point_X_COMP), math.log10(point_X_COMP1)], [point_Y_COMP, point_Y_COMP1])


    L1 = CustomLine(res_diap_COMPLINE.slope, res_diap_COMPLINE.intercept)  # Equation of line y=3x+5
    L2 = CustomLine(res_PERPENDICULAR.slope, res_PERPENDICULAR.intercept)
    point_X_COMP, point_Y_COMP = findSolution(L1, L2)

    # Провести три угловые линии
    first_line_x = [point_X_COMP, press_spd[index_2], max(press_spd)]
    LOG_first_line_x = [math.log10(point_X_COMP), math.log10(press_spd[index_2]), math.log10(max(press_spd))]
    first_line_y = [point_Y_COMP, point_Y_COMP, point_Y_COMP]

    third_line_x = [point_X_COMP, press_spd[index_2],]
    LOG_third_line_x = [math.log10(point_X_COMP), math.log10(press_spd[index_2]),]
    third_line_y = [point_Y_COMP, por_list[index_2],]
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

    # # Компрессионная кривая
    # plt.xscale('log')
    # plt.plot(press_spd, por_list, '.')
    # plt.plot(press_spd, por_list)
    # # Нижняя касательная
    # plt.plot(CAS_1_X, CAS_1_Y)
    # # Угловые линии к точке пересечения перпендикуляра и компрессионной кривой
    # plt.plot(first_line_x, first_line_y)
    # plt.plot(second_line_x, second_line_y)
    # plt.plot(third_line_x, third_line_y)
    # # Точка пересечения биссетрисы и нижней касательной
    # plt.plot(point_X_GG, point_Y_GG, '*')
    # # Перпендикуляр от точки GG
    # plt.plot(perp_GG_X, perp_GG_Y)
#
    # plt.plot(xrange, line(xrange, x1, y1), 'C1--', linewidth=2)

    # # Тестовый перпендикуляр
    # plt.plot([x_test, x_test1], perpendicular_START_END_Y)
    # plt.plot(point_X_CASS, point_Y_CASS , '*')

    # # Верхняя касательная
    # plt.plot(CAS_2_X, CAS_2_Y)
    # #Перпендикуляр
    # plt.plot((l2[0], l2[2]), (l2[1], l2[3]))
    # #Прямая конечных точек
    # plt.plot(START_END_LINE_X, START_END_LINE_Y)
    # #Точка пересечения перпендикуляра и прямой конечных точек
    # plt.plot(point_X_COMP, point_Y_COMP, '*')
    # plt.grid()
    # plt.show()

    # Основной датафрейм для Казагранде
    prepare_df = np.asarray([(press, otn, por) for press, otn, por in
                             zip(press_spd, calc_otn_vert_def, por_list)])
    NewDF_CASAGRANDE = pd.DataFrame(prepare_df)
    NewDF_CASAGRANDE.reset_index(drop=True, inplace=True)

    # Основной датафрейм для Беккера
    prepare_df = np.asarray([(press1, del_W, W_) for press1, del_W, W_ in
                             zip(press_spd_bekker, delta_W, W_DJ)])
    NewDF_BEKKER = pd.DataFrame(prepare_df)
    NewDF_BEKKER.reset_index(drop=True, inplace=True)

    # Метод Беккера
    prepare_BECCER = [(x_1, y_1, x_2, y_2, sig_x, sig_y) for x_1, y_1, x_2, y_2, sig_x, sig_y
                      in zip(x1, [x * 1000 for x in y1], x2, [x * 1000 for x in y2], [Sigma_Beccer, Sigma_Beccer, Sigma_Beccer], [y_middle_cp * 1000,y_middle_cp * 1000,y_middle_cp * 1000,])]
    BECCER = pd.DataFrame(prepare_BECCER)
    BECCER.reset_index(drop=True, inplace=True)

    # Метод Казагранде
    point_X_GG_l, point_Y_GG_l = [point_X_GG, point_X_GG, point_X_GG],[point_Y_GG, point_Y_GG, point_Y_GG]
    prepare_VALUES_LINES = [(c1_x, c1_y, fir_x, fir_y, sec_x, sec_y, thir_x, thir_y, p_gg_x, p_gg_y, perp_x, perp_y, x_CAS_B, y_CAS_B)
                                       for c1_x, c1_y, fir_x, fir_y, sec_x, sec_y, thir_x, thir_y, p_gg_x, p_gg_y, perp_x, perp_y, x_CAS_B, y_CAS_B
                                       in zip(CAS_1_X, CAS_1_Y, first_line_x, first_line_y, second_line_x, second_line_y, third_line_x, third_line_y, point_X_GG_l, point_Y_GG_l, perp_GG_X, perp_GG_Y, xrange_CAS_B, yrange_CAS_B)]
    VALUES_LINES = pd.DataFrame(prepare_VALUES_LINES)
    VALUES_LINES.reset_index(drop=True, inplace=True)

    values_for_Excel = {
        #### Беккер
        'a2': res_2.slope,
        'b2': res_2.intercept,

        'effective_press': effective_press,

        'Sigma_Beccer': Sigma_Beccer,
        'Y_Beccer': y_middle_cp * 1000,
        'OCR': OCR,
        'POP': POP,

        'BECCER': BECCER,
        'DATA_BEKKER': NewDF_BEKKER,

        #### Казагранде
        'VALUES_LINES': VALUES_LINES,
        'Sigma_CASAGRANDE': point_X_GG,
        'Y_CASAGRANDE': point_Y_GG,
        'OCR_CASAGRANDE': point_X_GG / effective_press,
        'POP_CASAGRANDE': point_X_GG - effective_press,
        'DATA_CASAGRANDE': NewDF_CASAGRANDE,
    }

    return values_for_Excel